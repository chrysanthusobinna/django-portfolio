# Testing

> [!NOTE]  
> Return back to the [README.md](README.md) file.

## Feature-by-Feature Testing

### Navigation
- Verified smooth transitions between pages.
- Checked that all links direct to the correct destinations.

### Responsive Design
- Tested the site on various devices and screen sizes (mobile, tablet, desktop).
- Confirmed consistent layout and functionality across devices.

### Portfolio Display
- Ensured all projects are properly showcased with accurate descriptions, images, and links.
- Checked that external links open in a new tab and direct to the intended destinations.

### Contact Form
- Tested form submission with valid and invalid inputs.
- Confirmed that users receive a success message upon submission.
- Verified that messages are stored correctly in the database.

## Regression Testing
- After updates, re-tested all core features to ensure no existing functionality was broken.
- Verified navigation, responsive design, portfolio display, and contact form submissions still work as intended.

---
This testing process confirms that the project functions as intended and provides a seamless user experience.



## Code Validation

I utilized the recommended [HTML W3C Validator](https://validator.w3.org) to validate all my HTML files. Using the live link, I viewed the source code, accessed the HTML W3C Validator, and selected the "Validate by Direct Input" tab. I then copied the entire source code and inserted it for validation. Below are the results for the custom pages I created:

| Directory                | File                                                                                                                                                    | Screenshot                                                      | Notes                                      |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|--------------------------------------------|
| portfolio_app/templates  | home.html                                                                                                                                               | ![screenshot](documentation/test/home-page-html-validator.png) | Document checking completed. No errors or warnings to show. |
| templates/account/       | login.html                                                                                                                                              | ![screenshot](documentation/test/login-page-html-validator.png) | Document checking completed. No errors or warnings to show. |
| templates/account/       | signup.html                                                                                                                                             | ![screenshot](documentation/test/signup-page-html-validator.png) | Document checking completed. No errors or warnings to show. |
| templates/account/       | logout.html                                                                                                                                             | ![screenshot](documentation/test/logout-page-html-validator.png) | Document checking completed. No errors or warnings to show. |
| portfolio_app/templates  | user-portfolio.html                                                                                                                                     | ![screenshot](documentation/test/view-user-portfolio-page-html-validator.png) | Document checking completed. No errors or warnings to show. |
| portfolio_app/templates  | edit-user-portfolio.html, home-page.html, modal-about.html, modal-certification.html, modal-contact.html, modal-education.html, modal-employment.html, modal-portfolio.html, modal-profilephoto.html, scroll-to-top.html | ![screenshot](documentation/test/edit-user-portfolio-page-html-validator.png) | Document checking completed. No errors or warnings to show. |


I used the [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to check my CSS files. On the validator website, I selected the option to input my CSS directly. After copying and pasting my CSS code into the provided text box, I ran the validation process by clicking the "Check" button. The validator confirmed that there were no errors, displaying a message stating, "Congratulations! No Error Found."

| Directory | File | Screenshot | Notes |
| --- | --- | --- | --- |
| static/css/ | styles.css | ![screenshot](documentation/test/css-validation.png) | Congratulations! No Error Found. |


### JavaScript

I used the recommended [JShint Validator](https://jshint.com) to validate all of my JS files.

**Summary of Results:**
- There are 35 functions in the file.
- The function with the largest signature takes 2 arguments, while the median is 0.
- The largest function has 16 statements, while the median is 1.
- The most complex function has a cyclomatic complexity value of 2, with a median of 1.
- There are 29 warnings, mostly about using `const` and `object short notation` which are available in ES6 or Mozilla JS extensions.
- There are also 2 undefined variables reported.

| Directory | File | Screenshot | Notes |
| --- | --- | --- | --- |
| static/js/ | scripts.js | ![screenshot](documentation/test/jshint-test.png) | `No Error Found.` |


### Python

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

| Directory      | File           | CI URL                                                                                  | Screenshot                                                       | Notes                         |
|----------------|----------------|-----------------------------------------------------------------------------------------|------------------------------------------------------------------|-------------------------------|
|                | manage.py      | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/manage.py) | ![screenshot](documentation/test/validate-manage-py.png)        | All clear, no errors found   |
| portfolio      | settings.py    | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio/settings.py) | ![screenshot](documentation/test/validate-settings-py.png)       | All clear, no errors found   |
| portfolio      | urls.py        | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio/urls.py) | ![screenshot](documentation/test/validate-portfolio-app-urls-py.png) | All clear, no errors found   |
| portfolio_app  | admin.py       | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/admin.py) | ![screenshot](documentation/test/validate-admin-py.png)          | All clear, no errors found   |
| portfolio_app  | context_processors.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/context_processors.py) | ![screenshot](documentation/test/validate-context-processors-py.png) | All clear, no errors found   |
| portfolio_app  | forms.py       | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/forms.py) | ![screenshot](documentation/test/validate-forms-py.png)          | All clear, no errors found   |
| portfolio_app  | helpers.py     | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/helpers.py) | ![screenshot](documentation/test/validate-helpers-py.png)        | All clear, no errors found   |
| portfolio_app  | models.py      | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/models.py) | ![screenshot](documentation/test/validate-models-py.png)         | All clear, no errors found   |
| portfolio_app  | signals.py     | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/signals.py) | ![screenshot](documentation/test/validate-signals-py.png)        | All clear, no errors found   |
| portfolio_app  | urls.py        | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/urls.py) | ![screenshot](documentation/test/validate-urls-py.png)           | All clear, no errors found   |
| portfolio_app  | utils.py       | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/utils.py) | ![screenshot](documentation/test/validate-utils-py.png)          | All clear, no errors found   |
| portfolio_app  | views.py       | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/views.py) | ![screenshot](documentation/test/validate-views-py.png)          | All clear, no errors found   |

 
 
## Browser Compatibility

I've tested my deployed project on multiple browsers to check for compatibility issues.

| Browser  | Home Screenshot                                   | User Portfolio Screenshot                                    | Notes                                    |
|----------|--------------------------------------------------|------------------------------------------------------------|------------------------------------------|
| Chrome   | ![screenshot](documentation/test/browser-chrome-home.png)          | ![screenshot](documentation/test/browser-chrome-user-portfolio.png)         | Works as expected. No issues identified. |
| Firefox  | ![screenshot](documentation/test/browser-firefox-home.png)         | ![screenshot](documentation/test/browser-firefox-user-portfolio.png)        | Works as expected. No issues identified. |
| Opera    | ![screenshot](documentation/test/browser-opera-home.png)           | ![screenshot](documentation/test/browser-opera-user-portfolio.png)          | Works as expected. No issues identified. |

 
 
## Responsiveness

I've tested my deployed project using Googlechrome built-in device sizes in the Developer Tools to check for responsiveness issues. Here are the results for the Home page and User Portfolio page:

### Tested for:
- Mobile
- Tablet
- Desktop

| Device   | Home                                                              | User Portfolio                                                         | Notes            |
|----------|-------------------------------------------------------------------|------------------------------------------------------------------------|------------------|
| Mobile   | ![screenshot](documentation/test/responsiveness-mobile-home.png)       | ![screenshot](documentation/test/responsiveness-mobile-user-portfolio.png)   | No issues. Worked as expected.  |
| Tablet   | ![screenshot](documentation/test/responsiveness-tablet-home.png)       | ![screenshot](documentation/test/responsiveness-tablet-user-portfolio.png)   | No issues. Worked as expected.  |
| Desktop  | ![screenshot](documentation/test/responsiveness-desktop-home.png)      | ![screenshot](documentation/test/responsiveness-desktop-user-portfolio.png)  | No issues. Worked as expected.  |

This table shows the compatibility results for different device sizes, confirming that the site works as expected on mobile, tablet, and desktop. 


## Lighthouse Audit

I tested my deployed project using the Google Chrome Developer Lighthouse Audit tool to evaluate performance and identify potential issues.

### Home Page
![lighthouse-home-page](documentation/test/lighthouse-home-page.png)  
- **Performance**: 50 - The page shows reasonable performance, with room for optimization to improve load times and responsiveness.  
- **Accessibility**: 89 - Most accessibility features are implemented effectively, ensuring usability for diverse users.  
- **Best Practices**: 100 - All recommended best practices are fully implemented.  
- **SEO**: 92 - The page is well-optimized for search engines.

---

### User Portfolio Page
![lighthouse-user-portfolio-page](documentation/test/lighthouse-user-portfolio-page.png)  
- **Performance**: 92 - A commendable performance score, indicating a well-optimized page.  
- **Accessibility**: 80 - Accessibility standards are nearly perfect, ensuring an inclusive user experience.  
- **Best Practices**: 61 - A few improvements can be made to align with best practices fully.  
- **SEO**: 92 - The page is effectively optimized for search visibility.

---

### Edit User Portfolio Page
![lighthouse-edit-user-portfolio-page](documentation/test/lighthouse-edit-user-portfolio-page.png)  
- **Performance**: 95 - A good performance score, suggesting effective optimization.  
- **Accessibility**: 84 - The page adheres closely to accessibility standards, providing an inclusive experience.  
- **Best Practices**: 61 - Minor adjustments are needed to fully meet best practices.  
- **SEO**: 92 - The page is well-prepared for search engine optimization.

---

### Sign Out Page
![lighthouse-sign-out-page](documentation/test/lighthouse-sign-out-page.png)  
- **Performance**: 97 - Performance is acceptable, but there is potential for further optimization.  
- **Accessibility**: 80 - The page is highly accessible, supporting diverse user needs.  
- **Best Practices**: 100 - Slight improvements could enhance adherence to best practices.  
- **SEO**: 92 - Search engine optimization is effectively implemented.

---

### Login Page
![lighthouse-login-page](documentation/test/lighthouse-login-page.png)  
- **Performance**: 98 - Performance is satisfactory, with some scope for refinement.  
- **Accessibility**: 83 - The page meets most accessibility requirements, ensuring usability for all.  
- **Best Practices**: 100 - Minor refinements are needed to achieve full alignment with best practices.  
- **SEO**: 92 - The page is well-optimized for search engines.

---

### Register Page
![lighthouse-register-page](documentation/test/lighthouse-register-page.png)  
- **Performance**: 96 - Performance is solid, with opportunities for optimization.  
- **Accessibility**: 83 - Accessibility standards are well-addressed, providing an inclusive experience.  
- **Best Practices**: 100 - Further adjustments could improve compliance with best practices.  
- **SEO**: 92 - The page demonstrates strong search engine optimization.

