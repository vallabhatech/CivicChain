# Project Structure Documentation

## Overview

The Decentralized Online Voting System is built using Django's Model-View-Template (MVT) architecture pattern, organized into modular applications that handle different aspects of the voting system.

## Directory Structure

```
DECENTRALIZED-ONLINE-VOTING-SYSTEM-USING-BLOCKCHAIN/
├── adminapp/                    # Administrator Module
│   ├── __init__.py             # Package initialization
│   ├── admin.py                # Django admin configuration
│   ├── apps.py                 # App configuration
│   ├── models.py               # Database models
│   ├── views.py                # Business logic and views
│   ├── urls.py                 # URL routing
│   ├── tests.py                # Unit tests
│   └── migrations/             # Database migration files
│       ├── 0001_initial.py
│       ├── 0002_alter_votermodel_aadhar.py
│       ├── 0003_electionmodel_voters.py
│       ├── 0004_remove_electionmodel_voters_electionmodel_voters.py
│       ├── 0005_rename_voter_count_electionmodel_candidates_count_and_more.py
│       ├── 0006_votermodel_otp.py
│       ├── 0007_votermodel_status.py
│       ├── 0008_remove_votermodel_city_remove_votermodel_dob_and_more.py
│       └── 0009_alter_votermodel_phone.py
├── voterapp/                   # Voter Module
│   ├── __init__.py             # Package initialization
│   ├── admin.py                # Django admin configuration
│   ├── apps.py                 # App configuration
│   ├── models.py               # Voter-specific models (extends adminapp)
│   ├── views.py                # Voting interface and authentication logic
│   ├── urls.py                 # URL routing for voter functions
│   ├── tests.py                # Unit tests
│   └── migrations/             # Database migrations (empty)
├── mainapp/                    # Main Application Module
│   ├── __init__.py             # Package initialization
│   ├── admin.py                # Django admin configuration
│   ├── apps.py                 # App configuration
│   ├── models.py               # Main application models
│   ├── views.py                # Home page and common views
│   ├── urls.py                 # Main URL routing
│   └── tests.py                # Unit tests
├── decentralizedvoting/         # Django Project Configuration
│   ├── __init__.py             # Package initialization
│   ├── settings.py             # Django settings and configuration
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI configuration for deployment
│   ├── asgi.py                 # ASGI configuration for async support
│   └── BlockcahinAlgo.py       # Blockchain hashing algorithm implementation
├── assets/                     # Static Files and Templates
│   ├── static/                 # Static assets
│   │   ├── css/                # Stylesheets
│   │   ├── js/                 # JavaScript files
│   │   ├── images/             # Image assets
│   │   └── vendor/             # Third-party libraries
│   └── templates/              # HTML templates
│       ├── admin/              # Admin interface templates
│       ├── voter/              # Voter interface templates
│       ├── main/               # Main application templates
│       └── base.html           # Base template
├── media/                      # User Uploaded Files
│   ├── images/                 # Election images
│   ├── symbols/                # Candidate party symbols
│   └── uploads/                # Other user uploads
├── Documentation/              # Project Documentation
│   └── Documentation.pdf      # Project report and technical details
├── .venv/                      # Virtual environment (Python)
├── dvoteenv/                   # Virtual environment (alternative)
├── dataset/                    # Dataset files (empty)
├── .git/                       # Git version control
├── .gitignore                  # Git ignore file
├── activate.sh                 # Virtual environment activation script
├── manage.py                   # Django management script
└── requirements.txt            # Python dependencies
```

## Module Details

### 1. adminapp/ - Administrator Module

**Purpose**: Handles all administrative functions including election management, candidate registration, and voter management.

**Key Components**:
- **models.py**: Contains core data models
  - `VoterModel`: Stores voter information and authentication data
  - `ElectionModel`: Manages election details and configurations
  - `CandidateModel`: Handles candidate information and voting data
  - `VotesModel`: Records blockchain-encrypted votes

- **views.py**: Implements administrative operations
  - Election creation and management
  - Candidate registration and management
  - Voter registration and approval
  - Real-time voting monitoring
  - Results generation and publication

- **urls.py**: URL routing for admin functions
  - `/admin/` - Admin dashboard
  - `/admin/create-election/` - Create new election
  - `/admin/manage-candidates/` - Candidate management
  - `/admin/register-voters/` - Voter registration

### 2. voterapp/ - Voter Module

**Purpose**: Provides voting interface and authentication for eligible voters.

**Key Components**:
- **views.py**: Implements voter-facing functionality
  - Voter registration and authentication
  - Biometric verification (face and fingerprint)
  - OTP verification
  - Voting interface
  - Vote confirmation and tracking

- **urls.py**: URL routing for voter functions
  - `/voter/login/` - Voter login
  - `/voter/register/` - Voter registration
  - `/voter/vote/` - Voting interface
  - `/voter/status/` - Vote status tracking

### 3. mainapp/ - Main Application Module

**Purpose**: Handles common functionality and serves as the entry point for the application.

**Key Components**:
- **views.py**: Main application views
  - Home page and landing
  - About and information pages
  - Navigation and routing

- **urls.py**: Main URL configuration
  - `/` - Home page
  - `/about/` - About page
  - `/contact/` - Contact page

### 4. decentralizedvoting/ - Project Configuration

**Purpose**: Contains Django project settings and core configurations.

**Key Components**:
- **settings.py**: Django configuration
  - Database settings (MySQL)
  - Installed applications
  - Middleware configuration
  - Static files configuration
  - Security settings

- **urls.py**: Root URL configuration
  - Includes URL patterns from all apps
  - Admin interface routing
  - Static file serving

- **BlockcahinAlgo.py**: Blockchain implementation
  - `HashDataBlock` class for vote encryption
  - SHA-256 hashing algorithm
  - Blockchain integrity validation

## Database Schema

### Core Tables

1. **voters_details** (VoterModel)
   - `id`: Primary key
   - `phone`: Phone number for OTP
   - `aadhar`: Aadhar card number
   - `otp`: One-time password
   - `status`: Registration status

2. **elction_detials** (ElectionModel)
   - `id`: Primary key
   - `election_name`: Name of election
   - `election_head`: Election administrator
   - `election_date`: Voting date
   - `election_picture`: Election image
   - `constituency`: Electoral constituency
   - `area`: Geographic area
   - `address`: Full address
   - `state`: State
   - `city`: City
   - `zip`: ZIP code
   - `candidates_count`: Number of candidates

3. **candidate_details** (CandidateModel)
   - `id`: Primary key
   - `election`: Foreign key to ElectionModel
   - `candidate_name`: Candidate's name
   - `party_name`: Political party
   - `symbol`: Party symbol image
   - `votes`: Vote count

4. **votes** (VotesModel)
   - `id`: Primary key
   - `election`: Foreign key to ElectionModel
   - `candidate`: Foreign key to CandidateModel
   - `voter`: Foreign key to VoterModel
   - `voter_block`: Blockchain hash for voter
   - `candidate_block`: Blockchain hash for candidate
   - `election_block`: Blockchain hash for election

## Static Assets Organization

### CSS Structure
```
static/css/
├── admin/
│   ├── dashboard.css
│   ├── forms.css
│   └── tables.css
├── voter/
│   ├── voting.css
│   ├── authentication.css
│   └── profile.css
├── main/
│   ├── layout.css
│   ├── navigation.css
│   └── responsive.css
└── vendor/
    ├── bootstrap.min.css
    └── fontawesome.min.css
```

### JavaScript Structure
```
static/js/
├── admin/
│   ├── dashboard.js
│   ├── charts.js
│   └── validation.js
├── voter/
│   ├── voting.js
│   ├── biometric.js
│   └── otp.js
├── main/
│   ├── navigation.js
│   └── common.js
└── vendor/
    ├── jquery.min.js
    ├── bootstrap.min.js
    └── chart.js
```

### Template Structure
```
templates/
├── base.html                 # Base template with common elements
├── admin/
│   ├── dashboard.html
│   ├── create_election.html
│   ├── manage_candidates.html
│   └── register_voters.html
├── voter/
│   ├── login.html
│   ├── register.html
│   ├── vote.html
│   └── status.html
└── main/
    ├── home.html
    ├── about.html
    └── contact.html
```

## Security Architecture

### Authentication Flow
1. **Registration**: Aadhar + Voter ID validation
2. **Mobile Verification**: OTP sent to registered phone
3. **Biometric Authentication**: Face and fingerprint verification
4. **Session Management**: Secure session tokens
5. **Vote Encryption**: Blockchain-based vote encryption

### Data Protection
- **Encryption**: All sensitive data encrypted at rest
- **Audit Trail**: Complete blockchain audit log
- **Access Control**: Role-based permissions
- **Data Integrity**: Cryptographic validation

## Development Workflow

### File Naming Conventions
- **Models**: PascalCase (e.g., `VoterModel`)
- **Views**: snake_case (e.g., `voter_registration`)
- **Templates**: kebab-case (e.g., `voter-registration.html`)
- **Static Files**: Descriptive names with prefixes

### Code Organization
- **Models**: Database schema and relationships
- **Views**: Business logic and request handling
- **Templates**: Presentation layer
- **Static Assets**: CSS, JavaScript, images
- **Tests**: Unit and integration tests

### Database Migration Strategy
- **Version Control**: All migrations tracked in Git
- **Backward Compatibility**: Maintained where possible
- **Data Integrity**: Validations and constraints
- **Rollback Support**: Migration rollback capabilities

## Deployment Considerations

### Production Structure
```
/var/www/voting-system/
├── app/                       # Application code
├── static/                    # Collected static files
├── media/                     # User uploads
├── logs/                      # Application logs
├── backups/                   # Database backups
└── config/                    # Configuration files
```

### Environment Configuration
- **Development**: SQLite/MySQL, DEBUG=True
- **Staging**: PostgreSQL, DEBUG=False
- **Production**: MySQL Cluster, DEBUG=False, SSL

This modular structure ensures maintainability, scalability, and security while following Django best practices and industry standards.
