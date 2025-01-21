<img src="documentation/logo.png" alt="logo" width="200"/>

# MiPortfolio

## Overview

**MiPortfolio** is a web-based application designed to help individuals create an online portfolio. Users can register, log in, and update their profiles with various sections they wish to include. The application allows customization of sections such as About, Employment Timeline, Education Timeline, Certification Timeline, Portfolio, and Contact Information. 

MiPortfolio is open to everyone, regardless of their job specialty, enabling users to showcase their portfolios on social media platforms, CVs, and other professional networks. This visibility allows recruiters and potential business partners to learn about them and connect.
 


## User Stories and Acceptance Criteria

### User Registration and Login

#### User Stories

- **As a user, I want to register on the website so that I can create my portfolio.**
  - **Acceptance Criteria:**
    - Given I am on the registration page,
    - When I fill out the registration form and submit it,
    - Then I should receive a confirmation email and be able to log in.

- **As a user, I want to log in and log out of the website so that I can access and manage my portfolio securely.**
  - **Acceptance Criteria:**
    - Given I am on the login page,
    - When I enter my credentials and submit,
    - Then I should be logged in and redirected to my profile page.
    - Given I am logged in,
    - When I click the logout button,
    - Then I should be logged out and redirected to the homepage.

- **As a user, I want to manage my profile so that I can update my personal information.**
  - **Acceptance Criteria:**
    - Given I am logged in,
    - When I navigate to the profile management page,
    - Then I should be able to update my personal information and save the changes.

### Home Page

#### User Stories

- **As a user, I want to visit the home page and see information about the website.**
  - **Acceptance Criteria:**
    - Given I am on the homepage,
    - When I load the page,
    - Then I should see an overview of the website and its features.

- **As a user, I want to have navigation links to the "Register" and "Login" pages from the home page.**
  - **Acceptance Criteria:**
    - Given I am on the homepage,
    - When I look at the navigation menu,
    - Then I should see links to the "Register" and "Login" pages.

### Profile Management

#### User Stories

- **As a user, I want to add my employment history so that I can showcase my work experience.**
  - **Acceptance Criteria:**
    - Given I am logged in,
    - When I navigate to the employment history section,
    - Then I should be able to add, edit, and delete my employment entries.

- **As a user, I want to add my education details so that I can highlight my academic background.**
  - **Acceptance Criteria:**
    - Given I am logged in,
    - When I navigate to the education section,
    - Then I should be able to add, edit, and delete my education entries.

- **As a user, I want to add my certifications and training so that I can demonstrate my professional development.**
  - **Acceptance Criteria:**
    - Given I am logged in,
    - When I navigate to the certifications section,
    - Then I should be able to add, edit, and delete my certifications.

- **As a user, I want to add my portfolio projects so that I can showcase my work.**
  - **Acceptance Criteria:**
    - Given I am logged in,
    - When I navigate to the portfolio section,
    - Then I should be able to add, edit, and delete my portfolio projects.

- **As a user, I want to add my contact information so that I can display my contacts.**
  - **Acceptance Criteria:**
    - Given I am logged in,
    - When I navigate to the contact information section,
    - Then I should be able to add, edit, and delete my contact information.

- **As a user, I want to choose which sections to add to my portfolio so that I can customize it according to my needs.**
  - **Acceptance Criteria:**
    - Given I am logged in,
    - When I navigate to the profile customization page,
    - Then I should be able to select and customize the sections I want to include in my portfolio.

### Email Functionality for Contact Forms

#### User Stories

- **As a user, I want to send an email using the contact form on the home page so that I can reach out for inquiries or support.**
  - **Acceptance Criteria:**
    - Given I am on the homepage,
    - When I fill out and submit the contact form,
    - Then I should receive a confirmation message that my email was sent successfully.

- **As a user, I want to receive a user-friendly message on the screen after sending an email so that I know my message was sent successfully.**
  - **Acceptance Criteria:**
    - Given I have submitted the contact form,
    - When the email is sent,
    - Then I should see a confirmation message on the screen.

- **As a user, I want to send an email for support so that I can get help when needed.**
  - **Acceptance Criteria:**
    - Given I am on the support page,
    - When I fill out and submit the support form,
    - Then I should receive a confirmation message that my email was sent successfully.

- **As a user, I want to use the contact form in a user portfolio to send an email to the user so that I can communicate directly with them.**
  - **Acceptance Criteria:**
    - Given I am viewing a user's portfolio,
    - When I fill out and submit the contact form,
    - Then the user should receive an email with my message.


## Tools & Technologies Used

- **HTML** - Used for structuring the web pages.
- **CSS** - Used for styling the web pages.
- **JavaScript** - Used for interactive elements.
- **jQuery** - Used for simplifying DOM manipulation and event handling.
- **Bootstrap** - Used for responsive design and layout.
- **Python Django** - Used for backend development.
- **PostgreSQL** - Used for the database.
- **Cloudinary** - Used for storing images.
- **GitHub Pages** - Used for hosting the deployed site.
- **Heroku** - Used for deployment.
 

## Application Workflow

The application workflow outlines the steps a user takes from visiting the website to managing their profile and portfolio. Here's a detailed explanation of the workflow:

1. **Visit the Home Page**:
   - The user navigates to the home page of the website.
   - The home page provides an overview of the website, instructions on how to use it, a Frequently Asked Questions section, and contact information along with a contact form.

2. **Register**:
   - The user clicks on the "Register" link from the navigation menu on the home page.
   - The user is directed to the registration page where they can create a new account by providing their details.
   - Upon successful registration, the user receives a confirmation email and can log in to their new account.

3. **Login**:
   - The user clicks on the "Login" link from the navigation menu on the home page.
   - The user is directed to the login page where they can enter their credentials to access their account.
   - Upon successful login, the user is redirected to their profile page.

4. **Edit Profile**:
   - Once logged in, the user can navigate to the profile management page.
   - The user can update their personal information, including their profile photo, about section, contact information, employment history, education details, certifications, and portfolio projects.

5. **Add, Update, or Delete Sections**:
   - The user can add new sections to their profile, such as employment history, education details, certifications, and portfolio projects.
   - The user can also update existing sections with new information or delete sections they no longer want to include in their profile.

6. **View and Share Profile**:
   - The user can click on "View My Profile" to see their user profile page.
   - The user can share this profile page with others, allowing them to view the user's portfolio.

7. **Logout**:
   - When the user is done managing their profile, they can log out by clicking the logout button.
   - The user is then redirected to the home page.

 
## Main Site Pages

The application features three primary pages on the main site:

- **`index.html`**: The homepage, which provides an overview and introduction, instructions on how to use the website, a Frequently Asked Questions section, and contact information along with a contact form.
- **`register`**: The registration page for new users to create an account.
- **`login.html`**: The login page for registered users to access their accounts.

## User Pages

The application provides several pages for users once they are logged in. Below is a description of each page and its functionality:

- **User Profile Page**: Accessible via `www.example.com/<username>`, this page displays the user's profile. It is available to both logged-in and non-logged-in users, allowing users to share their profile link with others. For example, `www.example.com/chrysanthusobinna`.

- **Edit User Profile Page**: Accessible via `www.example.com/edit/<username>`, this page allows users to create, edit, and delete their profile photo, about section, contacts, employment, education, and portfolio.

- **Logout Page**: Accessible via `www.example.com/logout/`, this page allows users to log out of their accounts.

## Admin Pages

In addition to the user pages, the application also includes admin pages for managing the site. These pages are built using Django Allauth for authentication and user management. Below is a description of each admin page and its functionality:

- **Admin Dashboard**: Accessible via `www.example.com/admin-panel/`, this page provides an overview of the site's activity and allows administrators to manage users, content, and site settings.
- **User Management**: Accessible via `www.example.com/admin-panel/auth/user/`, this page allows administrators to view, add, edit, and delete user accounts.
- **Group Management**: Accessible via `www.example.com/admin-panel/auth/group/`, this page allows administrators to manage user groups and permissions.
- **Site Configuration**: Accessible via `www.example.com/admin-panel/sites/site/`, this page allows administrators to configure site settings.
- **Social Account Management**: Accessible via `www.example.com/admin-panel/socialaccount/socialaccount/`, this page allows administrators to manage social accounts linked to user profiles.
- **Email Address Management**: Accessible via `www.example.com/admin-panel/account/emailaddress/`, this page allows administrators to manage email addresses associated with user accounts.

 
 
![screenshot](documentation/mockup.png)


## UX

#### Color Scheme

- **Background Color:** `#f8f9fa`
  - The light grey background color provides a clean and modern look, ensuring that the content is easy to read and visually appealing.

- **Page Header Color:** `#007bff` with `color: white`
  - The blue header color creates a cohesive and harmonious design, while the white text ensures high contrast and readability, making the header stand out.

- **Page Footer Color:** `#343a40` with `color: white`
  - The dark grey footer color provides a strong foundation for the page, grounding the design. The white text color maintains readability and consistency with the header, creating a balanced and professional appearance.

#### Typography

- **Font:** Arial, sans-serif
  - Arial is a widely used sans-serif font known for its clean and modern appearance. It is highly readable on both screens and print, making it an excellent choice for a portfolio website. The use of a sans-serif font also aligns with contemporary design trends, ensuring that the website looks up-to-date and professional.


 
## Features

### Existing Features

- **User Registration**  
  Allows new users to create an account by providing their details. This feature ensures that users can securely register and access the platform.

  !screenshot

- **User Login**  
  Enables registered users to log in to their accounts using their credentials. This feature ensures secure access to user profiles and personalized content.

  !screenshot

- **Profile Customization**  
  Users can customize their profiles by adding sections such as About, Employment Timeline, Education Timeline, Certification Timeline, Portfolio, and Contact Information. This feature allows users to create a comprehensive and personalized portfolio.

  !screenshot

- **Portfolio Management**  
  Users can add, edit, and delete portfolio items. This feature allows users to showcase their work and achievements in a structured manner.

  ![screenshot](documentation/xxxx.png)

- **Certification Management**  
  Users can add, edit, and delete certifications. This feature helps users highlight their qualifications and professional development.

  ![screenshot](documentation/xxxx.png)

- **Education Management**  
  Users can add, edit, and delete education entries. This feature allows users to present their academic background and achievements.

  ![screenshot](documentation/xxxx.png)

- **Employment Management**  
  Users can add, edit, and delete employment entries. This feature enables users to showcase their work experience and career progression.

  ![screenshot](documentation/xxxx.png)

- **Contact Information Management**  
  Users can update and delete their contact information. This feature ensures that users can provide up-to-date contact details for networking and professional connections.

 ![screenshot](documentation/xxxx.png)

- **Profile Photo Management**  
  Users can save and delete their profile photos. This feature allows users to personalize their profiles with a professional image.

   ![screenshot](documentation/xxxx.png)

- **Admin Dashboard**  
  Provides administrators with an overview of the site's activity and tools to manage users, content, and site settings. This feature ensures efficient site management and user administration.

 ![screenshot](documentation/xxxx.png)
 

### Future Features to Implement

- **AI-Powered CV Upload and Profile Generation**  
  A feature that allows users to upload their CV in PDF or Word document format. The system uses AI to analyze the CV and automatically generate a profile for the user, organizing their information into relevant sections such as About, Employment, Education, Certifications, and Portfolio.


- **AI-Generated CV Creation**  
  A feature that uses AI to generate a CV based on the information in the user's profile. This feature will allow users to easily create a professional CV by leveraging the data they have already entered into their profile.


- **Skill Endorsements**  
  A feature that allows users to endorse each other's skills. This feature can help users validate their expertise and build credibility within their professional network.


- **Portfolio Analytics**  
  A feature that provides users with analytics on their portfolio views, including the number of views, the most viewed sections, and the sources of traffic. This feature can help users understand the impact of their portfolio and make data-driven improvements.


- **Customizable Themes**  
  A feature that allows users to choose from a variety of themes to customize the look and feel of their portfolio. This feature can help users create a unique and personalized presentation of their professional information.


- **Integration with Job Boards**  
  A feature that integrates the portfolio with popular job boards, allowing users to easily apply for jobs using their MiPortfolio profile. This feature can streamline the job application process and increase the visibility of users' profiles to potential employers.


- **Unique Domain Names**  
  A feature that allows users to have a unique domain attached to their profile, such as `www.chrysanthusobinna.com` instead of `www.example.com/chrysanthusobinna`. This feature can help users create a more professional and personalized online presence.
 

## Data Model

### Profilephoto
Stores a user's profile photo.
- `user`: Links to a user.
- `profile_photo`: The photo itself.

### About
Stores information about a user.
- `user`: Links to a user.
- `about`: Text field for the user's description.

### Employment
Stores employment history.
- `user`: Links to a user.
- `employer_name`: Name of the employer.
- `job_title`: Job title.
- `description_of_duties`: Description of job duties.
- `start_date` and `end_date`: Employment period.

### Education
Stores educational background.
- `user`: Links to a user.
- `qualification`: Degree or qualification.
- `institution_name`: Name of the institution.
- `start_date` and `end_date`: Education period.

### Certification
Stores certifications.
- `user`: Links to a user.
- `name`: Name of the certification.
- `issuer`: Issuing organization.
- `date_issued`: Date of issuance.

### Portfolio
Stores portfolio projects.
- `user`: Links to a user.
- `title`: Title of the project.
- `description`: Description of the project.
- `link`: URL link to the project.
- `portfolio_photo`: Photo related to the project.

### Contact
Stores contact information.
- `user`: Links to a user.
- `phone_number`: Phone number.
- `email_address`: Email address.
- `linkedin`: LinkedIn profile URL.


### Flowchart


## Testing

> [!NOTE]  
> SEE [TESTING.md](TESTING.md) file.

 
## Credits


### Deploying to Heroku


**Media**

* The photos used on the Home Page, About Page, and Contact Page are from [Pexels](https://www.pexels.com/).
* The favicon for this project was sourced from [Favicon.io](https://favicon.io/).

**Mentor Support**

I would like to express my gratitude to my mentor for their invaluable support throughout this project. They shared best practices and guidelines that significantly improved my approach to the design and development of this project.
