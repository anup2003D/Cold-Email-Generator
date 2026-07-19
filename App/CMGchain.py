import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from pathlib import Path
import sys

# Add backend directory to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.append(str(backend_path))

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant"
        )
        # Default portfolio link (fallback only if no resume uploaded)
        self.default_portfolio_link = "https://anup2003d.github.io/portfolio-site/"
        
        # Load resume processor for dynamic portfolio
        try:
            from resume_processor import ResumeProcessor
            self.resume_processor = ResumeProcessor()
        except Exception as e:
            print(f"Warning: Could not load resume processor: {e}")
            self.resume_processor = None
    
    def reload_portfolio(self):
        """Reload portfolio data (called after resume upload)"""
        try:
            if self.resume_processor:
                # Just reload the processor to get latest data
                from resume_processor import ResumeProcessor
                self.resume_processor = ResumeProcessor()
        except Exception as e:
            print(f"Warning: Could not reload portfolio: {e}")
    
    def get_applicant_profile(self) -> str:
        """
        Get applicant profile - either from uploaded resume or default
        
        Returns:
            Formatted applicant profile text
        """
        if self.resume_processor and self.resume_processor.has_resume():
            try:
                return self.resume_processor.get_portfolio_text()
            except Exception as e:
                print(f"Warning: Could not load portfolio from resume: {e}")
        
        # Default portfolio if no resume uploaded
        return """### YOUR PROFILE (ANUP):
Professional Background:
- Data Analyst with 3+ years of experience in business intelligence and analytics
- Strong expertise in Python, SQL, Power BI, Tableau, and advanced Excel
- Experience with machine learning algorithms, predictive modeling, and statistical analysis
- Proven track record of transforming raw data into actionable business insights
- Background in data visualization, dashboard creation, and automated reporting systems
- Experience working with cross-functional teams to drive data-driven decision making

Key Achievements:
- Developed predictive models that improved forecasting accuracy by 30%
- Created automated dashboards that reduced manual reporting time by 60%
- Led data analysis projects that identified cost-saving opportunities worth $200K+
- Built ETL pipelines processing 1M+ records daily with 99.8% accuracy
- Mentored junior analysts and contributed to team knowledge sharing initiatives

Education & Certifications:
- Bachelor's degree in relevant field (Computer Science/Statistics/Engineering)
- Certified in advanced analytics tools and methodologies
- Continuous learner staying updated with latest data science trends"""

    def extract_company_info(self, cleaned_text):
        """
        Extract company information from scraped website text.
        """
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM COMPANY WEBSITE:
{page_data}

### INSTRUCTION:
Extract company information from the scraped website text. Focus on identifying:
- company_name: The name of the company
- company_domain: What industry or field they operate in
- company_highlight: The most impressive thing about them (e.g., funding, user base, key achievement)
- products_services: What they build or offer
- tech_stack: Any technical stack or tools mentioned (if detectable)

Return the information in JSON format with the keys: `company_name`, `company_domain`, `company_highlight`, `products_services`, `tech_stack`.
If any field is not found, use "Not specified" as the value.

### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            # Fallback
            res = {
                "company_name": "Unknown Company",
                "company_domain": "Technology",
                "company_highlight": "Not available",
                "products_services": "Not available",
                "tech_stack": "Not available"
            }
        return res

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
{page_data}

### INSTRUCTION:
Extract job posting information from the scraped career page text. Focus on identifying:
- Specific role requirements and responsibilities
- Required technical skills and tools
- Experience level and qualifications
- Company pain points or challenges mentioned
- Preferred qualifications or nice-to-haves
- Company culture indicators
- Company name (if mentioned)

Return the information in JSON format with the following keys: `role`, `experience`, `skills`, `description`, `requirements`, `company_challenges`, `preferred_skills`, `company_name`.
If any field is not found, use "Not specified" as the value.

### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def _detect_role_level(self, job_data):
        """Detect the seniority level of the role to adjust positioning"""
        if isinstance(job_data, dict):
            role = job_data.get('role', '').lower()
            description = job_data.get('description', '').lower()
            experience = job_data.get('experience', '').lower()
        else:
            role = str(job_data).lower()
            description = role
            experience = role

        # Check for role level indicators
        if any(word in role or word in description for word in ['intern', 'internship', 'trainee']):
            return 'internship'
        elif any(word in role or word in description for word in
                 ['junior', 'entry', 'associate', '0-2 years', 'fresher']):
            return 'junior'
        elif any(word in role or word in description for word in
                 ['senior', 'lead', 'principal', '5+ years', 'experienced']):
            return 'senior'
        else:
            return 'mid'  # Default to mid-level

    def _format_url(self, url: str) -> str:
        """Format URL to ensure it has proper protocol"""
        if not url or url in ['Not specified', 'not specified']:
            return None
        
        url = url.strip()
        
        # If it already starts with http:// or https://, return as is
        if url.startswith('http://') or url.startswith('https://'):
            return url
        
        # Otherwise, add https://
        return f"https://{url}"

    def _get_portfolio_link(self):
        """Helper to safely get portfolio link"""
        has_uploaded_resume = self.resume_processor and self.resume_processor.has_resume()
        
        if has_uploaded_resume:
            try:
                portfolio_data = self.resume_processor.load_portfolio()
                if portfolio_data and portfolio_data.get('portfolio_url') and portfolio_data.get('portfolio_url') != 'Not specified':
                    return self._format_url(portfolio_data.get('portfolio_url'))
            except:
                pass
        return self.default_portfolio_link
        
    def _build_signature(self, portfolio_link=None):
        """Helper to build email signature with contact details"""
        applicant_name = "Applicant"
        applicant_email = "your.email@example.com"
        applicant_linkedin = None
        applicant_github = None
        
        has_uploaded_resume = self.resume_processor and self.resume_processor.has_resume()
        if has_uploaded_resume:
            try:
                portfolio_data = self.resume_processor.load_portfolio()
                if portfolio_data:
                    applicant_name = portfolio_data.get('name', applicant_name)
                    applicant_email = portfolio_data.get('email', applicant_email)
                    
                    linkedin_raw = portfolio_data.get('linkedin', 'Not specified')
                    if linkedin_raw and linkedin_raw not in ['Not specified', 'LinkedIn', 'linkedin']:
                        applicant_linkedin = self._format_url(linkedin_raw)
                    
                    github_raw = portfolio_data.get('github', 'Not specified')
                    if github_raw and github_raw not in ['Not specified', 'GitHub', 'github']:
                        applicant_github = self._format_url(github_raw)
            except:
                pass
        
        signature_lines = [f"Best regards,", applicant_name, f"Email: {applicant_email}"]
        if portfolio_link:
            signature_lines.append(f"Portfolio: {portfolio_link}")
        if applicant_linkedin:
            signature_lines.append(f"LinkedIn: {applicant_linkedin}")
        if applicant_github:
            signature_lines.append(f"GitHub: {applicant_github}")
            
        return "\n".join(signature_lines), applicant_name

    def write_mail_job_posting(self, job, links=None):
        portfolio_link = self._get_portfolio_link()
        if links is None:
            links = [portfolio_link] if portfolio_link else []
        elif isinstance(links, str):
            links = [links]

        company_name = job.get('company_name', 'the company') if isinstance(job, dict) else 'the company'
        role_level = self._detect_role_level(job)
        
        job_description = str(job) if not isinstance(job, dict) else f"""
Role: {job.get('role', 'Not specified')}
Experience: {job.get('experience', 'Not specified')}
Skills: {job.get('skills', 'Not specified')}
Description: {job.get('description', 'Not specified')}
Requirements: {job.get('requirements', 'Not specified')}
Company Challenges: {job.get('company_challenges', 'Not specified')}
Preferred Skills: {job.get('preferred_skills', 'Not specified')}
Role Level Detected: {role_level}
        """
        
        applicant_profile = self.get_applicant_profile()
        signature, applicant_name = self._build_signature(portfolio_link)

        portfolio_section = ("### PORTFOLIO LINKS:\n" + "\n".join([f"- {link}" for link in links])) if links else "### PORTFOLIO LINKS:\nNo portfolio links provided."

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
{job_description}

### COMPANY CONTEXT:
Company Name: {company_name}

{applicant_profile}

{portfolio_section}

### INSTRUCTION:
You are {applicant_name}. Write a cold email for a job application that strictly follows the template structure below. Adapt the bracketed information using the job description and company context.

**TEMPLATE STRUCTURE TO FOLLOW:**
Subject: Application for [Specific Role Title] - {applicant_name}

Hi [Name or Hiring Team],

I came across {company_name} and really liked what you're building around [specific product or feature based on the job description].

I'm a B.Tech CSE student with hands-on experience in Python, backend development, and AI. I've built projects including a voice assistant, an AI-powered cold email generator, and ML applications, and I'm looking for an internship or entry-level software engineering opportunity.

I've attached my resume. If you think my profile could be a good fit, I'd love the opportunity to chat.

Thanks for your time!

{signature}

**Key Elements to Include:**
- Only output the final email starting with the Subject line.
- Do not add any extra paragraphs or fluff outside this structure.
- Ensure the tone matches the provided template precisely.

############# EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": job_description,
            "company_name": company_name,
            "applicant_profile": applicant_profile,
            "applicant_name": applicant_name,
            "portfolio_section": portfolio_section,
            "signature": signature
        })
        return res.content

    def write_mail_company_website(self, company_data, links=None):
        portfolio_link = self._get_portfolio_link()
        if links is None:
            links = [portfolio_link] if portfolio_link else []
        elif isinstance(links, str):
            links = [links]

        company_name = company_data.get('company_name', 'your company') if isinstance(company_data, dict) else 'your company'
        company_domain = company_data.get('company_domain', 'Technology') if isinstance(company_data, dict) else 'Technology'
        company_highlight = company_data.get('company_highlight', 'your recent growth') if isinstance(company_data, dict) else 'your recent growth'
        
        applicant_profile = self.get_applicant_profile()
        signature, applicant_name = self._build_signature(portfolio_link)

        portfolio_section = ("### PORTFOLIO LINKS:\n" + "\n".join([f"- {link}" for link in links])) if links else "### PORTFOLIO LINKS:\nNo portfolio links provided."

        prompt_email = PromptTemplate.from_template(
            """
            ### COMPANY CONTEXT:
Company Name: {company_name}
Domain/Industry: {company_domain}
Company Highlight: {company_highlight}

{applicant_profile}

{portfolio_section}

### INSTRUCTION:
You are {applicant_name}. Write a cold email expressing interest in working at this company, following the template structure below. Adapt the bracketed information using the company context.

**TEMPLATE STRUCTURE TO FOLLOW:**
Subject: Software Engineering Opportunities - {applicant_name}

Hi [Name or Hiring Team],

I came across {company_name} and was really impressed by {company_highlight}. I love what you're doing in the {company_domain} space.

I'm a B.Tech CSE student with hands-on experience in Python, backend development, and AI. I've built projects including a voice assistant, an AI-powered cold email generator, and ML applications. While I didn't see a specific open role, I'd love to be considered for any internship or entry-level software engineering opportunities.

I've attached my resume. If you think my profile could be a good fit, I'd love the opportunity to chat.

Thanks for your time!

{signature}

**Key Elements to Include:**
- Only output the final email starting with the Subject line.
- Do not add any extra paragraphs or fluff outside this structure.
- Ensure the tone matches the provided template precisely.

############# EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "company_name": company_name,
            "company_domain": company_domain,
            "company_highlight": company_highlight,
            "applicant_profile": applicant_profile,
            "applicant_name": applicant_name,
            "portfolio_section": portfolio_section,
            "signature": signature
        })
        return res.content

    def write_mail_generic(self, links=None):
        portfolio_link = self._get_portfolio_link()
        if links is None:
            links = [portfolio_link] if portfolio_link else []
        elif isinstance(links, str):
            links = [links]
        
        applicant_profile = self.get_applicant_profile()
        signature, applicant_name = self._build_signature(portfolio_link)

        portfolio_section = ("### PORTFOLIO LINKS:\n" + "\n".join([f"- {link}" for link in links])) if links else "### PORTFOLIO LINKS:\nNo portfolio links provided."

        prompt_email = PromptTemplate.from_template(
            """
            {applicant_profile}

{portfolio_section}

### INSTRUCTION:
You are {applicant_name}. Write a generic cold email for a job application following the template structure below.

**TEMPLATE STRUCTURE TO FOLLOW:**
Subject: Software Engineering Opportunities - {applicant_name}

Hi [Name or Hiring Team],

I am writing to express my interest in potential software engineering opportunities at your company. 

I'm a B.Tech CSE student with hands-on experience in Python, backend development, and AI. I've built projects including a voice assistant, an AI-powered cold email generator, and ML applications, and I'm looking for an internship or entry-level software engineering opportunity.

I've attached my resume. If you think my profile could be a good fit, I'd love the opportunity to chat.

Thanks for your time!

{signature}

**Key Elements to Include:**
- Only output the final email starting with the Subject line.
- Do not add any extra paragraphs or fluff outside this structure.
- Ensure the tone matches the provided template precisely.

############# EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "applicant_profile": applicant_profile,
            "applicant_name": applicant_name,
            "portfolio_section": portfolio_section,
            "signature": signature
        })
        return res.content

    def write_mail(self, job=None, links=None, company_data=None, page_type="job_posting"):
        """
        Router method for generating emails based on page type.
        Maintains backward compatibility.
        """
        if page_type == "company_website":
            return self.write_mail_company_website(company_data or job or {}, links)
        elif page_type == "generic":
            return self.write_mail_generic(links)
        else:
            # Default to job_posting
            return self.write_mail_job_posting(job or {}, links)

    def generate_cold_email(self, job_data, custom_links=None):
        """
        Convenience method to generate a cold email from job data

        Args:
            job_data: Dictionary containing job information or raw job description string
            custom_links: Optional list of specific portfolio links to include

        Returns:
            Generated cold email as string
        """
        return self.write_mail(job_data, custom_links)


if __name__ == "__main__":
    # Test the code
    print("Testing GROQ API Key:", "✓ Found" if os.getenv("GROQ_API_KEY") else "✗ Not found")

    # Example usage:
    chain = Chain()

    # Sample job data for testing
    sample_job = {
        "role": "Data Analyst",
        "experience": "2-4 years",
        "skills": "Python, SQL, Tableau, Power BI",
        "description": "Looking for a data analyst to help with business intelligence and reporting",
        "requirements": "Strong SQL skills, experience with visualization tools",
        "company_challenges": "Need to improve data-driven decision making",
        "preferred_skills": "Machine learning, cloud platforms",
        "company_name": "TechCorp"
    }

    # Generate email
    try:
        email = chain.generate_cold_email(sample_job)
        print("\n" + "=" * 50)
        print("GENERATED EMAIL:")
        print("=" * 50)
        print(email)
    except Exception as e:
        print(f"Error generating email: {e}")