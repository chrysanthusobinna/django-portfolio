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

| Directory | File | CI URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
|  | manage.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/manage.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio | settings.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio/settings.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio | urls.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio/urls.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio_app | admin.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/admin.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio_app | context_processors.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/context_processors.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio_app | forms.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/forms.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio_app | helpers.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/helpers.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio_app | models.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/models.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio_app | signals.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/signals.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio_app | urls.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/urls.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio_app | utils.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/utils.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
| portfolio_app | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/chrysanthusobinna/django-portfolio/main/portfolio_app/views.py) | ![screenshot](documentation/validation/path-to-screenshot.png) | |
