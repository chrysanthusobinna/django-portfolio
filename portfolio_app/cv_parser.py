import re
import logging
from datetime import datetime

# Try to import optional dependencies
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    from dateutil import parser as date_parser
    HAS_DATEUTIL = True
except ImportError:
    HAS_DATEUTIL = False

logger = logging.getLogger(__name__)

class CVParser:
    """Service to parse CV PDFs and extract relevant information"""
    
    def __init__(self):
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4,6}')
        self.linkedin_pattern = re.compile(r'linkedin\.com/in/[\w-]+', re.IGNORECASE)
        self.date_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)[\s\.,]+\d{1,2}[\s\.,]+(?:\d{4})?\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:20\d{2})\b', re.IGNORECASE)
        
        # Common section headers in CVs
        self.section_patterns = {
            'employment': [
                r'(?i)(?:work\s+experience|employment|professional\s+experience|career|job\s+history|work\s+history)',
                r'(?i)(?:experience|professional\s+background)'
            ],
            'education': [
                r'(?i)(?:education|academic|qualification|degree|university|college)',
                r'(?i)(?:educational\s+background|academic\s+background)'
            ],
            'certifications': [
                r'(?i)(?:certifications?|certificates?|professional\s+certifications?|credentials?)',
                r'(?i)(?:licenses?|accreditations?)'
            ],
            'projects': [
                r'(?i)(?:projects?|portfolio|work\s+projects?|personal\s+projects?)',
                r'(?i)(?:key\s+projects|project\s+experience)'
            ],
            'contact': [
                r'(?i)(?:contact|contact\s+info|get\s+in\s+touch|reach\s+me)',
                r'(?i)(?:personal\s+info|details?)'
            ]
        }
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file"""
        if not HAS_PDFPLUMBER:
            logger.error("pdfplumber library not available")
            return None
            
        try:
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return None
    
    def extract_contact_info(self, text):
        """Extract contact information from CV text"""
        contact_info = {
            'email': None,
            'phone': None,
            'linkedin': None
        }
        
        # Extract email
        email_match = self.email_pattern.search(text)
        if email_match:
            contact_info['email'] = email_match.group().strip()
        
        # Extract phone number
        phone_match = self.phone_pattern.search(text)
        if phone_match:
            contact_info['phone'] = phone_match.group().strip()
        
        # Extract LinkedIn URL
        linkedin_match = self.linkedin_pattern.search(text)
        if linkedin_match:
            contact_info['linkedin'] = "https://" + linkedin_match.group().strip()
        
        return contact_info
    
    def extract_employment(self, text):
        """Extract employment information from CV text"""
        employment_entries = []
        
        # Find employment section
        employment_section = self._extract_section(text, 'employment')
        if not employment_section:
            return employment_entries
        
        # Split by common job entry separators
        job_entries = re.split(r'\n(?=[A-Z][a-z]+\s+[A-Z][a-z]+|[A-Z][a-z]+\s+at\s+|\d{4})', employment_section)
        
        for entry in job_entries:
            if len(entry.strip()) < 20:  # Skip very short entries
                continue
                
            job_info = self._parse_job_entry(entry)
            if job_info:
                employment_entries.append(job_info)
        
        return employment_entries
    
    def extract_education(self, text):
        """Extract education information from CV text"""
        education_entries = []
        
        # Find education section
        education_section = self._extract_section(text, 'education')
        if not education_section:
            return education_entries
        
        # Split by common education entry separators
        edu_entries = re.split(r'\n(?=[A-Z][a-z]+\s+(?:University|College|Institute|School)|[A-Z][a-z]+\s+(?:Bachelor|Master|PhD|BSc|MSc|BA|MA))', education_section)
        
        for entry in edu_entries:
            if len(entry.strip()) < 20:  # Skip very short entries
                continue
                
            edu_info = self._parse_education_entry(entry)
            if edu_info:
                education_entries.append(edu_info)
        
        return education_entries
    
    def extract_certifications(self, text):
        """Extract certification information from CV text"""
        certification_entries = []
        
        # Find certifications section
        cert_section = self._extract_section(text, 'certifications')
        if not cert_section:
            return certification_entries
        
        # Split by lines and look for certification patterns
        lines = cert_section.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) < 10:  # Skip very short lines
                continue
            
            cert_info = self._parse_certification_entry(line)
            if cert_info:
                certification_entries.append(cert_info)
        
        return certification_entries
    
    def extract_projects(self, text):
        """Extract project information from CV text"""
        project_entries = []
        
        # Find projects section
        projects_section = self._extract_section(text, 'projects')
        if not projects_section:
            return project_entries
        
        # Split by common project separators
        project_entries_raw = re.split(r'\n(?=[A-Z][a-z]+\s+(?:Project|Application|System|Platform)|\d{4})', projects_section)
        
        for entry in project_entries_raw:
            if len(entry.strip()) < 20:  # Skip very short entries
                continue
                
            project_info = self._parse_project_entry(entry)
            if project_info:
                project_entries.append(project_info)
        
        return project_entries
    
    def extract_about_summary(self, text):
        """Extract about/summary information from CV text"""
        # Look for summary/objective sections at the beginning
        lines = text.split('\n')
        summary_lines = []
        
        # Check first few lines for summary
        for i, line in enumerate(lines[:10]):
            line = line.strip()
            if len(line) > 50 and not any(keyword in line.lower() for keyword in ['experience', 'education', 'employment', 'skills']):
                summary_lines.append(line)
            elif summary_lines and (len(line) < 20 or any(keyword in line.lower() for keyword in ['experience', 'education', 'employment'])):
                break
        
        if summary_lines:
            return ' '.join(summary_lines)[:500]  # Limit to 500 characters
        
        return None
    
    def _extract_section(self, text, section_type):
        """Extract a specific section from CV text"""
        patterns = self.section_patterns.get(section_type, [])
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                start_pos = match.start()
                # Find the next section header
                remaining_text = text[start_pos + len(match.group()):]
                
                # Look for next major section
                next_section_pattern = r'(?i)(' + '|'.join([
                    'work experience', 'employment', 'education', 'certifications', 
                    'projects', 'skills', 'contact', 'summary', 'objective'
                ]) + r')'
                
                next_match = re.search(next_section_pattern, remaining_text)
                if next_match:
                    section_text = remaining_text[:next_match.start()]
                else:
                    section_text = remaining_text
                
                return section_text.strip()
        
        return None
    
    def _parse_job_entry(self, entry):
        """Parse individual job entry"""
        lines = [line.strip() for line in entry.split('\n') if line.strip()]
        if not lines:
            return None
        
        job_info = {
            'employer_name': None,
            'job_title': None,
            'description_of_duties': None,
            'start_date': None,
            'end_date': None
        }
        
        # Try to extract job title and employer from first line
        first_line = lines[0]
        
        # Look for patterns like "Job Title at Company" or "Company - Job Title"
        if ' at ' in first_line.lower():
            parts = first_line.split(' at ')
            job_info['job_title'] = parts[0].strip()
            job_info['employer_name'] = parts[1].strip()
        elif ' - ' in first_line:
            parts = first_line.split(' - ')
            if len(parts) >= 2:
                job_info['employer_name'] = parts[0].strip()
                job_info['job_title'] = parts[1].strip()
        else:
            # Assume first line is job title, look for company in next lines
            job_info['job_title'] = first_line
            for line in lines[1:3]:
                if any(word in line.lower() for word in ['inc', 'ltd', 'llc', 'company', 'corporation']):
                    job_info['employer_name'] = line
                    break
        
        # Extract dates
        dates = self._extract_dates(entry)
        if dates:
            job_info['start_date'] = dates.get('start')
            job_info['end_date'] = dates.get('end')
        
        # Extract description (everything after the first 2-3 lines)
        if len(lines) > 2:
            job_info['description_of_duties'] = ' '.join(lines[2:])[:500]
        
        return job_info if job_info['job_title'] else None
    
    def _parse_education_entry(self, entry):
        """Parse individual education entry"""
        lines = [line.strip() for line in entry.split('\n') if line.strip()]
        if not lines:
            return None
        
        edu_info = {
            'qualification': None,
            'institution_name': None,
            'start_date': None,
            'end_date': None
        }
        
        # Extract qualification and institution
        text = ' '.join(lines[:2])
        
        # Look for degree patterns
        degree_patterns = [
            r'(?:Bachelor|Master|PhD|BSc|MSc|BA|MA|B\.?S\.?|M\.?S\.?|Ph\.?D\.?)\s+(?:of\s+)?(?:Science|Arts|Engineering|Business|Computer\s+Science|Information\s+Technology)',
            r'(?:Bachelor|Master|PhD|BSc|MSc|BA|MA)',
            r'(?:Engineer|Developer|Specialist|Professional)'
        ]
        
        for pattern in degree_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                edu_info['qualification'] = match.group().strip()
                break
        
        # Extract institution (usually contains University, College, etc.)
        for line in lines[:3]:
            if any(word in line.lower() for word in ['university', 'college', 'institute', 'school']):
                edu_info['institution_name'] = line.strip()
                break
        
        # Extract dates
        dates = self._extract_dates(entry)
        if dates:
            edu_info['start_date'] = dates.get('start')
            edu_info['end_date'] = dates.get('end')
        
        return edu_info if edu_info['institution_name'] else None
    
    def _parse_certification_entry(self, line):
        """Parse individual certification entry"""
        cert_info = {
            'name': None,
            'issuer': None,
            'date_issued': None
        }
        
        # Look for certification patterns
        cert_patterns = [
            r'(.+?)\s+(?:by|from|issued\s+by)\s+(.+?)(?:\s+\(|\s+\d{4})',
            r'(.+?)\s+\((.+?)\)',
            r'(.+?)\s+(?:Certified|Professional|Specialist)'
        ]
        
        for pattern in cert_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                groups = match.groups()
                cert_info['name'] = groups[0].strip()
                if len(groups) > 1:
                    cert_info['issuer'] = groups[1].strip()
                break
        
        # Extract date
        dates = self._extract_dates(line)
        if dates and dates.get('end'):
            cert_info['date_issued'] = dates['end']
        
        return cert_info if cert_info['name'] else None
    
    def _parse_project_entry(self, entry):
        """Parse individual project entry"""
        lines = [line.strip() for line in entry.split('\n') if line.strip()]
        if not lines:
            return None
        
        project_info = {
            'title': None,
            'description': None,
            'link': None
        }
        
        # First line is usually the project title
        project_info['title'] = lines[0].strip()
        
        # Rest is description
        if len(lines) > 1:
            project_info['description'] = ' '.join(lines[1:])[:500]
        
        # Look for URLs
        url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`[\]]+')
        url_match = url_pattern.search(entry)
        if url_match:
            project_info['link'] = url_match.group().strip()
        
        return project_info if project_info['title'] else None
    
    def _extract_dates(self, text):
        """Extract date ranges from text"""
        dates = {'start': None, 'end': None}
        
        # Find all date matches
        date_matches = self.date_pattern.findall(text)
        
        if date_matches:
            # Take the first two dates as start and end
            if len(date_matches) >= 1:
                dates['start'] = self._normalize_date(date_matches[0])
            if len(date_matches) >= 2:
                dates['end'] = self._normalize_date(date_matches[1])
            elif len(date_matches) == 1:
                # Single date, assume it's end date
                dates['end'] = self._normalize_date(date_matches[0])
        
        return dates
    
    def _normalize_date(self, date_str):
        """Normalize date string to YYYY-MM-DD format"""
        try:
            if HAS_DATEUTIL:
                parsed_date = date_parser.parse(date_str, fuzzy=True)
                return parsed_date.strftime('%Y-%m-%d')
            else:
                # Fallback to simple year extraction
                year_match = re.search(r'\b(20\d{2})\b', date_str)
                if year_match:
                    return f"{year_match.group(1)}-01-01"
                return None
        except:
            # Try to extract just the year
            year_match = re.search(r'\b(20\d{2})\b', date_str)
            if year_match:
                return f"{year_match.group(1)}-01-01"
            return None
    
    def parse_cv(self, pdf_file):
        """Main method to parse CV and extract all information"""
        text = self.extract_text_from_pdf(pdf_file)
        if not text:
            return None
        
        parsed_data = {
            'contact': self.extract_contact_info(text),
            'employment': self.extract_employment(text),
            'education': self.extract_education(text),
            'certifications': self.extract_certifications(text),
            'projects': self.extract_projects(text),
            'about': self.extract_about_summary(text)
        }
        
        return parsed_data
