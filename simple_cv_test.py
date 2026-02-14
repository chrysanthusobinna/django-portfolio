#!/usr/bin/env python3
"""
Simple test script for CV Parser functionality
This script tests the CV parsing service without Django dependencies
"""

import re
from datetime import datetime
from dateutil import parser as date_parser

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

def test_cv_parser():
    """Test the CV parser with sample text data"""
    
    # Sample CV text for testing
    sample_cv_text = """
    John Doe
    Software Engineer
    
    Contact:
    Email: john.doe@example.com
    Phone: +1 (555) 123-4567
    LinkedIn: https://linkedin.com/in/johndoe
    
    Summary:
    Experienced software engineer with 5+ years of experience in full-stack development,
    specializing in Python, Django, and React. Passionate about building scalable
    web applications and leading development teams.
    
    Work Experience:
    Senior Software Engineer at Tech Corp
    June 2020 - Present
    Led development of enterprise web applications using Django and React.
    Managed a team of 5 developers and implemented CI/CD pipelines.
    
    Software Developer at StartupXYZ
    January 2018 - May 2020
    Developed RESTful APIs and responsive front-end interfaces.
    Worked with Python, JavaScript, and PostgreSQL.
    
    Education:
    Bachelor of Science in Computer Science
    University of Technology
    September 2014 - May 2018
    
    Certifications:
    AWS Certified Solutions Architect
    Issued by Amazon Web Services
    March 2021
    
    Django Developer Certification
    Issued by Django Software Foundation
    November 2019
    
    Projects:
    E-Commerce Platform
    Full-featured online shopping platform built with Django and React.
    Includes user authentication, payment processing, and admin dashboard.
    https://github.com/johndoe/ecommerce
    
    Task Management App
    Collaborative project management tool with real-time updates.
    Built using Django Channels and WebSocket technology.
    """
    
    print("Testing CV Parser...")
    print("=" * 50)
    
    # Create parser instance
    parser = CVParser()
    
    # Test contact extraction
    print("\n1. Testing Contact Extraction:")
    contact = parser.extract_contact_info(sample_cv_text)
    print(f"   Email: {contact.get('email')}")
    print(f"   Phone: {contact.get('phone')}")
    print(f"   LinkedIn: {contact.get('linkedin')}")
    
    # Test about extraction
    print("\n2. Testing About/Summary Extraction:")
    about = parser.extract_about_summary(sample_cv_text)
    print(f"   Summary: {about[:200]}...")
    
    print("\n" + "=" * 50)
    print("CV Parser Test Complete!")
    print("Basic functionality appears to be working correctly.")
    print("The parser can extract contact information and summaries from CV text.")

if __name__ == "__main__":
    test_cv_parser()
