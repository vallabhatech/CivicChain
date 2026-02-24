# Contributing Guidelines

## Overview

Thank you for your interest in contributing to the Decentralized Online Voting System! This document provides guidelines and standards for contributing to this project. We welcome contributions from developers, designers, security experts, and anyone passionate about secure digital democracy.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation Standards](#documentation-standards)
7. [Security Considerations](#security-considerations)
8. [Pull Request Process](#pull-request-process)
9. [Issue Reporting](#issue-reporting)
10. [Community Guidelines](#community-guidelines)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors. We value respect, collaboration, and constructive feedback.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of different viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior
- Harassment, trolling, or discriminatory language
- Personal attacks or political discussions
- Publishing private information without consent
- Any other conduct which could reasonably be considered inappropriate

## Getting Started

### Prerequisites
- Python 3.10+
- Git
- Basic knowledge of Django framework
- Understanding of blockchain concepts
- Familiarity with MySQL database

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork the repository on GitHub
   # Clone your fork locally
   git clone https://github.com/yourusername/DECENTRALIZED-ONLINE-VOTING-SYSTEM-USING-BLOCKCHAIN.git
   cd DECENTRALIZED-ONLINE-VOTING-SYSTEM-USING-BLOCKCHAIN
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Configure Development Database**
   ```bash
   # Create development database
   mysql -u root -p
   CREATE DATABASE decentralized_voting_dev;
   
   # Update settings in decentralizedvoting/settings_dev.py
   ```

4. **Run Initial Setup**
   ```bash
   python manage.py migrate --settings=decentralizedvoting.settings_dev
   python manage.py createsuperuser --settings=decentralizedvoting.settings_dev
   python manage.py runserver --settings=decentralizedvoting.settings_dev
   ```

### Development Dependencies

Create `requirements-dev.txt`:
```txt
# Production dependencies
-r requirements.txt

# Development tools
black==22.3.0
flake8==4.0.1
isort==5.10.1
pytest==7.1.2
pytest-django==4.5.2
pytest-cov==3.0.0
django-debug-toolbar==3.5.0
django-extensions==3.2.1
factory-boy==3.2.1
```

## Development Workflow

### 1. Create a Feature Branch
```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Follow coding standards
- Write tests for new features
- Update documentation
- Commit frequently with descriptive messages

### 3. Test Your Changes
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.

# Run linting
flake8 .
black --check .
isort --check-only .
```

### 4. Submit Pull Request
- Push to your fork
- Create pull request to main branch
- Fill out pull request template
- Wait for code review

## Coding Standards

### Python Code Style

#### Formatting
We use **Black** for code formatting:
```bash
# Format code
black .

# Check formatting
black --check .
```

#### Import Sorting
We use **isort** for import organization:
```bash
# Sort imports
isort .

# Check imports
isort --check-only .
```

#### Linting
We use **flake8** for linting:
```bash
# Run linting
flake8 .
```

### Code Style Guidelines

#### Naming Conventions
```python
# Classes: PascalCase
class VoterModel:
    pass

# Functions and variables: snake_case
def calculate_vote_percentage():
    total_votes = 100
    return total_votes

# Constants: UPPER_SNAKE_CASE
MAX_VOTE_ATTEMPTS = 3

# Private methods: underscore prefix
def _internal_method(self):
    pass
```

#### Docstrings
```python
def calculate_block_hash(previous_hash: str, data: list) -> str:
    """
    Calculate blockchain hash for vote data.
    
    Args:
        previous_hash: Hash of the previous block
        data: List of vote data to hash
        
    Returns:
        SHA-256 hash string
        
    Raises:
        ValueError: If data is empty or invalid
        
    Example:
        >>> hash = calculate_block_hash("abc123", ["vote1", "vote2"])
        >>> print(hash)
        "def456..."
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    # Implementation here
    pass
```

#### Type Hints
```python
from typing import List, Optional, Dict, Any

def process_voter_data(
    voter_id: str,
    election_data: Dict[str, Any],
    candidates: Optional[List[str]] = None
) -> bool:
    """Process voter data and return success status."""
    pass
```

### Django-Specific Standards

#### Models
```python
from django.db import models
from django.core.validators import RegexValidator


class VoterModel(models.Model):
    """Model representing a registered voter."""
    
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        help_text="Phone number with country code"
    )
    aadhar = models.CharField(
        max_length=50,
        unique=True,
        help_text="Aadhar card number"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Verification'),
            ('active', 'Active'),
            ('suspended', 'Suspended'),
        ],
        default='pending'
    )
    
    class Meta:
        db_table = 'voters_details'
        verbose_name = 'Voter'
        verbose_name_plural = 'Voters'
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"Voter {self.aadhar}"
    
    def clean(self) -> None:
        """Custom validation logic."""
        super().clean()
        # Add custom validation here
        pass
```

#### Views
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator


@login_required
@require_http_methods(["GET", "POST"])
def election_create_view(request):
    """
    Create a new election.
    
    Handles both GET (display form) and POST (process form) requests.
    """
    if request.method == 'POST':
        form = ElectionForm(request.POST, request.FILES)
        if form.is_valid():
            election = form.save(commit=False)
            election.created_by = request.user
            election.save()
            messages.success(request, 'Election created successfully!')
            return redirect('election_detail', pk=election.pk)
    else:
        form = ElectionForm()
    
    return render(request, 'admin/election_create.html', {'form': form})
```

#### Forms
```python
from django import forms
from django.core.exceptions import ValidationError
from .models import ElectionModel


class ElectionForm(forms.ModelForm):
    """Form for creating and editing elections."""
    
    class Meta:
        model = ElectionModel
        fields = [
            'election_name', 'election_head', 'election_date',
            'constituency', 'area', 'address', 'state', 'city', 'zip',
            'election_picture'
        ]
        widgets = {
            'election_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_election_date(self) -> datetime.date:
        """Validate election date is in the future."""
        election_date = self.cleaned_data['election_date']
        if election_date <= datetime.date.today():
            raise ValidationError('Election date must be in the future.')
        return election_date
```

## Testing Guidelines

### Test Structure
```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_views.py
│   └── test_utils.py
├── integration/
│   ├── test_workflows.py
│   └── test_api.py
└── fixtures/
    ├── voters.json
    └── elections.json
```

### Unit Testing
```python
import pytest
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from adminapp.models import VoterModel, ElectionModel


class VoterModelTest(TestCase):
    """Test cases for VoterModel."""
    
    def setUp(self):
        """Set up test data."""
        self.voter_data = {
            'phone': '+1234567890',
            'aadhar': '123456789012',
            'status': 'pending'
        }
    
    def test_voter_creation(self):
        """Test voter model creation."""
        voter = VoterModel.objects.create(**self.voter_data)
        self.assertEqual(voter.phone, '+1234567890')
        self.assertEqual(voter.aadhar, '123456789012')
        self.assertEqual(voter.status, 'pending')
    
    def test_voter_str_representation(self):
        """Test string representation of voter."""
        voter = VoterModel.objects.create(**self.voter_data)
        self.assertEqual(str(voter), 'Voter 123456789012')
    
    @patch('adminapp.models.validate_aadhar')
    def test_aadhar_validation(self, mock_validate):
        """Test Aadhar validation during creation."""
        mock_validate.return_value = True
        voter = VoterModel.objects.create(**self.voter_data)
        mock_validate.assert_called_once_with('123456789012')
```

### Integration Testing
```python
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from adminapp.models import ElectionModel, CandidateModel


class ElectionWorkflowTest(TestCase):
    """Test election creation and voting workflow."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )
        self.client.login(username='admin', password='testpass123')
    
    def test_election_creation_workflow(self):
        """Test complete election creation workflow."""
        # Create election
        response = self.client.post(reverse('election_create'), {
            'election_name': 'Test Election',
            'election_head': 'Test Commissioner',
            'election_date': '2024-12-15',
            'constituency': 'Test District',
            'area': 'Test Area',
            'address': 'Test Address',
            'state': 'Test State',
            'city': 'Test City',
            'zip': '12345'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ElectionModel.objects.filter(election_name='Test Election').exists())
        
        # Add candidate
        election = ElectionModel.objects.get(election_name='Test Election')
        response = self.client.post(reverse('candidate_add', args=[election.pk]), {
            'candidate_name': 'Test Candidate',
            'party_name': 'Test Party'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CandidateModel.objects.filter(candidate_name='Test Candidate').exists())
```

### API Testing
```python
import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from adminapp.models import VoterModel


class VoterAPITest(TestCase):
    """Test voter API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.voter_data = {
            'full_name': 'Test Voter',
            'aadhar_number': '123456789012',
            'voter_id': 'VOT123456789',
            'phone_number': '+1234567890',
            'email': 'test@example.com'
        }
    
    def test_voter_registration_api(self):
        """Test voter registration API endpoint."""
        response = self.client.post(
            reverse('voter-register-api'),
            data=self.voter_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(VoterModel.objects.filter(aadhar='123456789012').exists())
    
    def test_voter_registration_validation(self):
        """Test voter registration validation."""
        invalid_data = self.voter_data.copy()
        invalid_data['aadhar_number'] = 'invalid'
        
        response = self.client.post(
            reverse('voter-register-api'),
            data=invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('aadhar_number', response.data['errors'])
```

### Test Coverage
```bash
# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Coverage requirements:
# - Minimum 90% line coverage
# - All critical paths covered
# - All security functions tested
```

## Documentation Standards

### Code Documentation
- All public functions must have docstrings
- Complex logic should be commented
- Use type hints where applicable
- Include examples in docstrings

### API Documentation
- Update API documentation for new endpoints
- Include request/response examples
- Document error codes
- Provide usage examples

### User Documentation
- Update user guides for new features
- Include screenshots for UI changes
- Provide step-by-step instructions
- Update FAQ for common issues

## Security Considerations

### Security Review Checklist
- [ ] Input validation and sanitization
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Authentication and authorization
- [ ] Data encryption
- [ ] Audit logging
- [ ] Error handling (no information leakage)

### Security Testing
```python
import pytest
from django.test import TestCase, Client
from django.urls import reverse


class SecurityTest(TestCase):
    """Test security measures."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Client()
    
    def test_sql_injection_protection(self):
        """Test SQL injection protection."""
        malicious_input = "'; DROP TABLE voters_details; --"
        response = self.client.post(
            reverse('voter-search'),
            {'search_term': malicious_input}
        )
        
        # Should not cause database error
        self.assertNotEqual(response.status_code, 500)
    
    def test_xss_protection(self):
        """Test XSS protection."""
        xss_payload = '<script>alert("xss")</script>'
        response = self.client.post(
            reverse('voter-register'),
            {'full_name': xss_payload}
        )
        
        # Should escape script tags
        self.assertNotIn('<script>', response.content.decode())
    
    def test_authentication_required(self):
        """Test that protected endpoints require authentication."""
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
```

### Vulnerability Reporting
If you discover a security vulnerability:
1. Do not open a public issue
2. Email security@votingsystem.com
3. Provide detailed description
4. Include steps to reproduce
5. Wait for acknowledgment before disclosure

## Pull Request Process

### Pull Request Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Coverage requirements met

## Security Considerations
- [ ] Security review completed
- [ ] No sensitive data exposed
- [ ] Proper authentication/authorization

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Ready for review
```

### Review Process
1. **Automated Checks**
   - Code formatting (Black, isort)
   - Linting (flake8)
   - Tests (pytest)
   - Security scan

2. **Code Review**
   - At least one maintainer review
   - Focus on logic, security, and performance
   - All comments addressed

3. **Integration Testing**
   - Test in staging environment
   - Verify no breaking changes
   - Performance impact assessment

4. **Merge**
   - Squash and merge commits
   - Update version if needed
   - Deploy to production

## Issue Reporting

### Bug Report Template
```markdown
## Bug Description
Clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.10]
- Django version: [e.g. 4.1.3]
- Browser: [e.g. Chrome 91]

## Additional Context
Add any other context about the problem here.
```

### Feature Request Template
```markdown
## Feature Description
Clear and concise description of the feature.

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How would you like to solve this problem?

## Alternatives Considered
What other approaches have you considered?

## Additional Context
Add any other context about the feature request here.
```

## Community Guidelines

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **Discord**: Real-time discussion and help
- **Email**: Private questions and security issues
- **Discussions**: General questions and ideas

### Contribution Recognition
- Contributors list in README
- Release notes attribution
- Annual contributor spotlight
- Swag for significant contributions

### Mentorship Program
- New contributor mentorship available
- Pair programming sessions
- Code review guidance
- Best practices workshops

## Release Process

### Version Management
- Semantic versioning (MAJOR.MINOR.PATCH)
- Changelog maintained for each release
- Backward compatibility considerations
- Migration guides for breaking changes

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Security review completed
- [ ] Performance testing done
- [ ] Release notes prepared
- [ ] Version numbers updated
- [ ] Tag created
- [ ] Deployed to staging
- [ ] Approved for production

## Getting Help

### Resources
- [Project Documentation](https://docs.votingsystem.com)
- [API Reference](https://api.votingsystem.com/docs)
- [Community Forum](https://forum.votingsystem.com)
- [FAQ](https://docs.votingsystem.com/faq)

### Contact
- **Technical Questions**: discussions@votingsystem.com
- **Security Issues**: security@votingsystem.com
- **General Inquiries**: info@votingsystem.com

---

Thank you for contributing to the Decentralized Online Voting System! Your contributions help make digital democracy more secure and accessible for everyone.
