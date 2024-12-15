# Contributing to EasyAccess

Thank you for your interest in contributing to the EasyAccess project! Contributions are what make the open-source community an incredible place to learn, inspire, and create. We welcome your contributions to help improve EasyAccess. 

This document provides guidelines for contributing to the project hosted at [EasyAccess GitLab Repository](https://git.tulane.edu/apl/easyaccess).

---

## How to Contribute

### 1. Fork the Repository
1. Visit the project repository at [EasyAccess GitLab Repository](https://git.tulane.edu/apl/easyaccess).
2. Click the "Fork" button to create your copy of the repository.

### 2. Clone Your Fork
Clone the repository to your local development environment:

```bash
git clone https://git.tulane.edu/<your-username>/easyaccess.git
cd easyaccess
```

### 3. Set Up the Development Environment
Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```
For development, it's recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Windows, use venv\Scripts\activate
```

### 4. Create a New Branch
Create a branch to work on your feature, bug fix, or enhancement:
```bash
git checkout -b feature/<feature-name>
```

### 5. Make Your Changes
Follow the project's coding style (PEP 8 for Python).
Write meaningful commit messages.
Add or update tests to ensure your changes work as expected.
Document any significant changes in code or behavior.

### 6. Test Your Changes
Run the test suite to verify your changes:
```bash
pytest
```
Ensure that all tests pass and the code coverage does not decrease.

### 7. Push Your Changes
Push your branch to your forked repository:
```bash
git add .
git commit -m "Add meaningful commit message here"
git push origin feature/<feature-name>
```
### 8. Submit a Merge Request (MR)
1. Go to your forked repository on GitLab.
2. Click on the Merge Requests tab.
3. Click New Merge Request and select your branch.
4. Provide a clear title and description for your MR.
5. Ensure your MR includes the following:
    - Description of the changes made.
    - Issue or feature ticket reference, if applicable.
    - Tests or evidence of changes working as intended.

## Coding Standards
- Follow the PEP 8 coding style for Python.
- Use meaningful variable and function names.
- Write concise and clear inline comments.
- Document all public methods and classes using Python docstring conventions.

## Reporting Issues
If you encounter any issues or have feature requests, please report them by opening an issue in the [GitLab Issues Tracker](https://git.tulane.edu/apl/easyaccess/-/issues).

Please provide the following details when submitting an issue:

- A clear and concise description of the issue or request.
- Steps to reproduce the issue, if applicable.
- Environment details (e.g., operating system, Python version).

## Contributor Code of Conduct
By participating in this project, you agree to abide by our Code of Conduct.

We appreciate your time and effort in contributing to EasyAccess. Together, we can build a powerful and user-friendly tool for connecting to EasyAPI!
