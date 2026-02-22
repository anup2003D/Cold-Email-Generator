import os
import json
from pathlib import Path
from typing import Dict, Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import PyPDF2

load_dotenv()


class ResumeProcessor:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant"
        )
        self.portfolio_file = Path(__file__).parent / "applicant_portfolio.json"
        self.resume_folder = Path(__file__).parent / "resumes"
        self.resume_folder.mkdir(exist_ok=True)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF resume"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def generate_portfolio_from_resume(self, resume_text: str, applicant_name: str = "Applicant") -> Dict:
        """Use LLM to generate a structured portfolio from resume text"""
        
        prompt = PromptTemplate.from_template(
            """
            ### RESUME TEXT:
{resume_text}

### INSTRUCTION:
Analyze the resume and create a comprehensive professional portfolio profile. Extract and organize:

1. **Professional Background** (2-3 sentences):
   - Current role/title and years of experience
   - Key areas of expertise and technical focus
   - Professional identity and what they do

2. **Technical Skills** (categorized list):
   - Programming languages
   - Tools and technologies
   - Frameworks and platforms
   - Methodologies

3. **Key Achievements** (4-6 bullet points):
   - Quantifiable accomplishments with metrics
   - Project impacts and business results
   - Leadership or mentoring experiences
   - Awards or recognition

4. **Education & Certifications**:
   - Degrees with majors
   - Relevant certifications
   - Professional development

5. **Contact Information**:
   - Extract name, email, phone if present
   - Extract LinkedIn URL (full URL like https://linkedin.com/in/username or linkedin.com/in/username)
   - Extract portfolio/personal website URL (full URL)
   - Extract GitHub URL (full URL like https://github.com/username or github.com/username)
   - IMPORTANT: Extract the actual URLs, not just the words "LinkedIn" or "GitHub"
   - If URL doesn't start with http:// or https://, still extract the domain part (e.g., linkedin.com/in/username)

6. **Professional Summary** (1 paragraph):
   - A compelling summary highlighting their unique value proposition
   - Career highlights and what makes them stand out

Return the information in JSON format with these exact keys:
- name
- email
- phone
- linkedin (full URL or "Not specified" if not found)
- portfolio_url (full URL or "Not specified" if not found)
- github (full URL or "Not specified" if not found)
- professional_background
- technical_skills (object with categories)
- key_achievements (array)
- education (array)
- certifications (array)
- professional_summary

IMPORTANT: For linkedin, portfolio_url, and github fields:
- Extract the actual URL if present (e.g., "https://linkedin.com/in/johndoe" or "linkedin.com/in/johndoe")
- If you only see the word "LinkedIn" or "GitHub" without an actual profile link, use "Not specified"
- Do NOT use just the words "LinkedIn" or "GitHub" as values

If any information is not found, use "Not specified" for strings or empty array [] for lists.

### VALID JSON OUTPUT (NO PREAMBLE, NO MARKDOWN):
            """
        )

        chain = prompt | self.llm
        res = chain.invoke({"resume_text": resume_text})
        
        # Clean the response - remove markdown code blocks if present
        content = res.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        try:
            portfolio_data = json.loads(content)
            # Ensure we have the applicant name
            if portfolio_data.get("name") == "Not specified":
                portfolio_data["name"] = applicant_name
            return portfolio_data
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse portfolio JSON: {str(e)}\nContent: {content}")

    def save_portfolio(self, portfolio_data: Dict) -> None:
        """Save portfolio data to JSON file"""
        with open(self.portfolio_file, 'w') as f:
            json.dump(portfolio_data, f, indent=2)

    def load_portfolio(self) -> Optional[Dict]:
        """Load portfolio data from JSON file"""
        if self.portfolio_file.exists():
            with open(self.portfolio_file, 'r') as f:
                return json.load(f)
        return None

    def process_resume(self, pdf_path: str, applicant_name: str = "Applicant") -> Dict:
        """
        Complete workflow: Extract text from PDF, generate portfolio, and save it
        
        Args:
            pdf_path: Path to the PDF resume file
            applicant_name: Name of the applicant (optional)
            
        Returns:
            Dictionary containing the generated portfolio data
        """
        # Extract text from PDF
        resume_text = self.extract_text_from_pdf(pdf_path)
        
        if not resume_text or len(resume_text) < 50:
            raise Exception("Resume text is too short or empty. Please ensure the PDF is readable.")
        
        # Generate portfolio from resume text
        portfolio_data = self.generate_portfolio_from_resume(resume_text, applicant_name)
        
        # Save portfolio
        self.save_portfolio(portfolio_data)
        
        return portfolio_data

    def get_portfolio_text(self) -> str:
        """
        Get formatted portfolio text for use in email generation
        
        Returns:
            Formatted string containing the applicant's portfolio
        """
        portfolio = self.load_portfolio()
        
        if not portfolio:
            # Return default portfolio if none exists
            return """Professional Background:
- Experienced professional seeking new opportunities
- Strong technical skills and proven track record
- Passionate about delivering results and continuous learning"""
        
        # Format technical skills
        tech_skills = portfolio.get('technical_skills', {})
        skills_text = ""
        if isinstance(tech_skills, dict):
            for category, skills in tech_skills.items():
                if isinstance(skills, list):
                    skills_text += f"- {category}: {', '.join(skills)}\n"
                else:
                    skills_text += f"- {category}: {skills}\n"
        
        # Format achievements
        achievements = portfolio.get('key_achievements', [])
        achievements_text = "\n".join([f"- {ach}" for ach in achievements])
        
        # Format education
        education = portfolio.get('education', [])
        education_text = "\n".join([f"- {edu}" for edu in education])
        
        # Build complete portfolio text
        portfolio_text = f"""### YOUR PROFILE ({portfolio.get('name', 'Applicant').upper()}):

Professional Summary:
{portfolio.get('professional_summary', 'Not specified')}

Professional Background:
{portfolio.get('professional_background', 'Not specified')}

Technical Skills:
{skills_text.strip() if skills_text else 'Not specified'}

Key Achievements:
{achievements_text if achievements_text else '- Not specified'}

Education & Certifications:
{education_text if education_text else '- Not specified'}
"""
        
        # Add certifications if present
        certifications = portfolio.get('certifications', [])
        if certifications:
            cert_text = "\n".join([f"- {cert}" for cert in certifications])
            portfolio_text += f"\nCertifications:\n{cert_text}"
        
        return portfolio_text

    def has_resume(self) -> bool:
        """Check if a portfolio has been generated"""
        return self.portfolio_file.exists()

    def get_resume_status(self) -> Dict:
        """Get the current resume/portfolio status"""
        if not self.portfolio_file.exists():
            return {
                "has_resume": False,
                "message": "No resume uploaded yet"
            }
        
        portfolio = self.load_portfolio()
        return {
            "has_resume": True,
            "applicant_name": portfolio.get('name', 'Unknown'),
            "email": portfolio.get('email', 'Not specified'),
            "message": "Resume processed successfully"
        }


if __name__ == "__main__":
    # Test the resume processor
    processor = ResumeProcessor()
    
    # Test with the uploaded resume
    resume_path = Path(__file__).parent.parent / "Anup Dutta Resume.pdf"
    
    if resume_path.exists():
        print("Processing resume...")
        try:
            portfolio = processor.process_resume(str(resume_path), "Anup Dutta")
            print("\n✅ Portfolio generated successfully!")
            print(json.dumps(portfolio, indent=2))
            
            print("\n" + "="*50)
            print("FORMATTED PORTFOLIO TEXT:")
            print("="*50)
            print(processor.get_portfolio_text())
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"❌ Resume not found at: {resume_path}")
        print("Please ensure 'Anup Dutta Resume.pdf' is in the project root folder.")
