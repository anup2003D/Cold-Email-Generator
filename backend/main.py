from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
import shutil
from pathlib import Path

# Add parent directory to path to import existing modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'App'))

from CMGchain import Chain
from CMGportfolio import Portfolio
from CMGutils import clean_text
from smtp_service import SMTPService
from resume_processor import ResumeProcessor

app = FastAPI(title="Cold Email Generator API")

# Configure CORS for browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
csv_path = os.path.join(os.path.dirname(__file__), '..', 'App', 'Resource', 'my_portfolio.csv')
chain = Chain()
portfolio = Portfolio(csv_path)
smtp_service = SMTPService()
resume_processor = ResumeProcessor()


# Request/Response models
class JobExtractionRequest(BaseModel):
    text: str

class EmailGenerationRequest(BaseModel):
    job_data: dict
    custom_links: Optional[List[str]] = None

class EmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str


@app.get("/")
async def root():
    return {
        "message": "Cold Email Generator API",
        "version": "1.0.0",
        "endpoints": [
            "/api/extract-job",
            "/api/generate-email",
            "/api/send-email-smtp",
            "/api/smtp-status",
            "/api/upload-resume",
            "/api/resume-status",
            "/api/portfolio"
        ]
    }


@app.post("/api/extract-job")
async def extract_job(request: JobExtractionRequest):
    """Extract job information from scraped text"""
    try:
        cleaned_text = clean_text(request.text)
        if not cleaned_text or len(cleaned_text) < 50:
            raise HTTPException(status_code=400, detail="Text too short or empty")

        jobs = chain.extract_jobs(cleaned_text)
        return {
            "success": True,
            "jobs": jobs,
            "count": len(jobs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting job: {str(e)}")


@app.post("/api/generate-email")
async def generate_email(request: EmailGenerationRequest):
    """Generate personalized cold email based on job data"""
    try:
        job_data = request.job_data

        # Get portfolio links if not provided
        if request.custom_links:
            links = request.custom_links
        else:
            skills = job_data.get('skills', [])
            if isinstance(skills, str):
                skills = [s.strip() for s in skills.split(',')]
            links = portfolio.query_links(skills)

        # Generate email
        email = chain.write_mail(job_data, links)

        # Generate subject line with applicant name from resume
        role = job_data.get('role', 'Position')
        applicant_name = "Applicant"
        if resume_processor.has_resume():
            try:
                portfolio_data = resume_processor.load_portfolio()
                if portfolio_data:
                    applicant_name = portfolio_data.get('name', 'Applicant')
            except Exception:
                pass
        subject = f"Application for {role} - {applicant_name}"

        return {
            "success": True,
            "email": email,
            "subject": subject,
            "job_role": role
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating email: {str(e)}")


@app.post("/api/send-email-smtp")
async def send_email_smtp(payload: EmailRequest):
    """Send email via SMTP (Gmail App Password — no OAuth needed)"""
    try:
        result = smtp_service.send_email(
            to_email=payload.to_email,
            subject=payload.subject,
            body=payload.body
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email via SMTP: {str(e)}")


@app.get("/api/smtp-status")
async def smtp_status():
    """Check SMTP configuration status"""
    is_configured = smtp_service.is_configured()

    if is_configured:
        return {
            "success": True,
            "configured": True,
            "smtp_server": smtp_service.smtp_server,
            "smtp_port": smtp_service.smtp_port,
            "sender_email": smtp_service.sender_email,
            "sender_name": smtp_service.sender_name,
            "message": "SMTP is configured and ready to send emails"
        }
    else:
        return {
            "success": False,
            "configured": False,
            "message": "SMTP not configured. Add SMTP_EMAIL and SMTP_PASSWORD to .env file",
            "instructions": {
                "step1": "Go to https://myaccount.google.com/apppasswords",
                "step2": "Create App Password for Mail",
                "step3": "Add to backend/.env: SMTP_EMAIL=your-email@gmail.com",
                "step4": "Add to backend/.env: SMTP_PASSWORD=your-16-char-app-password"
            }
        }


@app.post("/api/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    applicant_name: str = Form(...)
):
    """Upload PDF resume and generate portfolio"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Save uploaded file
        resume_path = resume_processor.resume_folder / file.filename
        with open(resume_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process resume and generate portfolio
        portfolio_data = resume_processor.process_resume(str(resume_path), applicant_name)

        # Reload chain with new portfolio
        chain.reload_portfolio()

        return {
            "success": True,
            "message": "Resume uploaded and portfolio generated successfully",
            "applicant_name": portfolio_data.get('name', applicant_name),
            "portfolio_data": portfolio_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


@app.get("/api/resume-status")
async def get_resume_status():
    """Check if resume has been uploaded and get applicant info"""
    try:
        status = resume_processor.get_resume_status()
        return {
            "success": True,
            **status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking resume status: {str(e)}")


@app.get("/api/portfolio")
async def get_portfolio():
    """Get the current applicant portfolio"""
    try:
        portfolio_data = resume_processor.load_portfolio()
        if not portfolio_data:
            raise HTTPException(status_code=404, detail="No portfolio found. Please upload a resume first.")

        return {
            "success": True,
            "portfolio": portfolio_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading portfolio: {str(e)}")


@app.delete("/api/resume")
async def delete_resume():
    """Delete current resume and portfolio (for changing resume)"""
    try:
        if resume_processor.portfolio_file.exists():
            resume_processor.portfolio_file.unlink()

        if resume_processor.resume_folder.exists():
            for file in resume_processor.resume_folder.glob("*.pdf"):
                file.unlink()

        chain.reload_portfolio()

        return {
            "success": True,
            "message": "Resume and portfolio deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting resume: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "portfolio_loaded": portfolio.collection.count() > 0,
        "llm_configured": chain.llm is not None,
        "resume_uploaded": resume_processor.has_resume()
    }


if __name__ == "__main__":
    import uvicorn
    print("Starting Cold Email Generator API...")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="localhost", port=8000)
