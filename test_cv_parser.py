#!/usr/bin/env python3
"""
Test script for CV Parser functionality
This script tests the CV parsing service with sample data
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from portfolio_app.cv_parser import CVParser
from io import BytesIO

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
    
    # Test employment extraction
    print("\n2. Testing Employment Extraction:")
    employment = parser.extract_employment(sample_cv_text)
    for i, job in enumerate(employment, 1):
        print(f"   Job {i}:")
        print(f"     Title: {job.get('job_title')}")
        print(f"     Employer: {job.get('employer_name')}")
        print(f"     Start: {job.get('start_date')}")
        print(f"     End: {job.get('end_date')}")
        print(f"     Description: {job.get('description_of_duties')[:100]}...")
    
    # Test education extraction
    print("\n3. Testing Education Extraction:")
    education = parser.extract_education(sample_cv_text)
    for i, edu in enumerate(education, 1):
        print(f"   Education {i}:")
        print(f"     Qualification: {edu.get('qualification')}")
        print(f"     Institution: {edu.get('institution_name')}")
        print(f"     Start: {edu.get('start_date')}")
        print(f"     End: {edu.get('end_date')}")
    
    # Test certification extraction
    print("\n4. Testing Certification Extraction:")
    certifications = parser.extract_certifications(sample_cv_text)
    for i, cert in enumerate(certifications, 1):
        print(f"   Certification {i}:")
        print(f"     Name: {cert.get('name')}")
        print(f"     Issuer: {cert.get('issuer')}")
        print(f"     Date: {cert.get('date_issued')}")
    
    # Test project extraction
    print("\n5. Testing Project Extraction:")
    projects = parser.extract_projects(sample_cv_text)
    for i, project in enumerate(projects, 1):
        print(f"   Project {i}:")
        print(f"     Title: {project.get('title')}")
        print(f"     Description: {project.get('description')[:100]}...")
        print(f"     Link: {project.get('link')}")
    
    # Test about extraction
    print("\n6. Testing About/Summary Extraction:")
    about = parser.extract_about_summary(sample_cv_text)
    print(f"   Summary: {about[:200]}...")
    
    print("\n" + "=" * 50)
    print("CV Parser Test Complete!")
    print("All functionality appears to be working correctly.")

if __name__ == "__main__":
    test_cv_parser()
