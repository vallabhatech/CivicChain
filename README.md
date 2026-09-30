# CivicChain

A Django-based voting-system prototype exploring authenticated voter registration, election management, vote recording, and a hash-chain integrity layer.

> **Status:** Educational/demo project. It is **not** a production election system and has not been certified for real-world elections.

## What is implemented

- Django web application with separate admin and voter modules.
- Election and candidate management.
- Voter registration with OTP workflow.
- Vote submission with duplicate-vote checks at the application layer.
- SHA-256 hash chaining for vote-integrity metadata.
- Result and integrity-verification views.
- MySQL support, with SQLite available as the default local-development database.
- Environment-based configuration for secrets and external SMS credentials.
- GitHub Actions CI and CodeQL scanning.

## Architecture

```text
Browser
  │
  ├── Main app
  ├── Voter app ────────┐
  └── Admin app         │
                        ▼
                  Django models
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
          Database          HashDataBlock
                              SHA-256
```

The blockchain component in this repository is a **custom hash-chain prototype**. It is not an Ethereum smart-contract implementation and should not be described as a public blockchain.

## Requirements

- Python 3.10–3.11
- pip
- Git
- SQLite for the quickest local setup, or MySQL for a fuller deployment
- A configured `BLOCKCHAIN_GENESIS_KEY`

## Quick start

### Windows

```bat
git clone https://github.com/vallabhatech/CivicChain.git
cd CivicChain

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set a unique `DJANGO_SECRET_KEY` and `BLOCKCHAIN_GENESIS_KEY`.

### Linux/macOS

```bash
git clone https://github.com/vallabhatech/CivicChain.git
cd CivicChain

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py test
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Configuration

Important variables:

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django signing/security secret |
| `DJANGO_DEBUG` | Development debug flag |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `DB_ENGINE` | Database backend |
| `DB_NAME` | Database name/path |
| `DB_USER` / `DB_PASSWORD` | Database credentials |
| `BLOCKCHAIN_GENESIS_KEY` | Stable secret used as the hash-chain root |
| `SMS_API_KEY` | Optional external SMS credential |

Never commit `.env` or real provider credentials.

## Security notes

This project handles sensitive voter-related data and should be treated as a prototype.

- Do not use real Aadhaar numbers, phone numbers, biometric data, or election records during development.
- Hashing is **not encryption** and does not by itself provide ballot secrecy.
- The application-level duplicate-vote check is not sufficient for a real election system.
- OTP storage and authentication need additional hardening before production use.
- External SMS integration is disabled unless credentials are explicitly configured.
- Use HTTPS, secure secret management, database encryption, audit controls, independent security review, and jurisdiction-specific legal/compliance review before any real deployment.

## Project layout

```text
CivicChain/
├── adminapp/                 # Election administration and verification
├── voterapp/                 # Registration, OTP and voting flows
├── mainapp/                  # Public/common views
├── decentralizedvoting/      # Django project settings and hash-chain code
├── assets/                   # Templates and static assets
├── docs/                     # Project documentation
├── Documentation/            # Original project PDF
├── .github/workflows/        # CI and CodeQL
├── .env.example              # Safe configuration template
├── manage.py
├── requirements.txt
└── README.md
```

## Development

Run checks locally before opening a PR:

```bash
python manage.py check
python manage.py test
```

The repository also runs these checks through GitHub Actions on pushes and pull requests.

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [User Guide](docs/USER_GUIDE.md)
- [API Notes](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Contributing](docs/CONTRIBUTING.md)

Some legacy documentation describes planned or conceptual capabilities more broadly than the current code. Treat the implementation in this repository as the source of truth.

## License

MIT — see [LICENSE](LICENSE).

## Disclaimer

CivicChain is an educational software project. Election infrastructure is safety-critical and requires substantially stronger guarantees than this prototype currently provides.
