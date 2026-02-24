# Installation and Setup Guide

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, Ubuntu 18.04+, macOS 10.15+
- **Python**: 3.10 or higher
- **MySQL**: 8.0 or higher
- **RAM**: Minimum 4GB, Recommended 8GB
- **Storage**: Minimum 10GB free space
- **Internet**: Required for package installation and dependencies

### Required Software
1. **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
2. **MySQL 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
3. **Git** - [Download Git](https://git-scm.com/downloads/)
4. **Code Editor** - VS Code, PyCharm, or similar (recommended)

## Step-by-Step Installation

### Step 1: Install Python

#### Windows
1. Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Verify installation
python3 --version
pip3 --version
```

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3.10 python3.10-pip python3.10-venv

# Verify installation
python3.10 --version
pip3 --version
```

### Step 2: Install and Configure MySQL

#### Windows
1. Download MySQL Installer from [MySQL website](https://dev.mysql.com/downloads/installer/)
2. Run the installer and select "Developer Default"
3. Configure root password (remember this password)
4. Start MySQL service

#### macOS
```bash
# Install MySQL using Homebrew
brew install mysql

# Start MySQL service
brew services start mysql

# Secure installation
mysql_secure_installation
```

#### Ubuntu/Debian
```bash
# Install MySQL Server
sudo apt install mysql-server

# Secure installation
sudo mysql_secure_installation

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql
```

### Step 3: Create Database

1. Log in to MySQL as root:
   ```bash
   mysql -u root -p
   ```

2. Create the database and user:
   ```sql
   CREATE DATABASE decentralized_voting CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'voting_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON decentralized_voting.* TO 'voting_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

### Step 4: Clone the Repository

```bash
# Clone the project
git clone https://github.com/yourusername/DECENTRALIZED-ONLINE-VOTING-SYSTEM-USING-BLOCKCHAIN.git

# Navigate to project directory
cd DECENTRALIZED-ONLINE-VOTING-SYSTEM-USING-BLOCKCHAIN
```

### Step 5: Create Virtual Environment

#### Windows
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 6: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Note**: If `requirements.txt` doesn't exist, create it with:
```bash
pip freeze > requirements.txt
```

### Step 7: Configure Database Settings

1. Open `decentralizedvoting/settings.py`
2. Update the database configuration:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'decentralized_voting',
           'USER': 'voting_user',
           'PASSWORD': 'secure_password',  # Replace with your password
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

3. Update security settings:
   ```python
   # Generate a new secret key
   SECRET_KEY = 'your-new-secret-key-here'
   
   # Update allowed hosts for production
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-domain.com']
   ```

### Step 8: Install MySQL Connector

```bash
# Install MySQL connector for Python
pip install mysqlclient
```

**Note**: If you encounter installation issues:

#### Windows
```cmd
# Install Microsoft Visual C++ Build Tools
# Or use pre-compiled wheel
pip install mysqlclient-2.1.1-cp310-cp310-win_amd64.whl
```

#### macOS
```bash
# Install MySQL development headers
brew install mysql-connector-c

# Set environment variables
export LDFLAGS="-L/usr/local/opt/mysql-connector-c/lib"
export CPPFLAGS="-I/usr/local/opt/mysql-connector-c/include"
```

#### Ubuntu/Debian
```bash
# Install MySQL development headers
sudo apt install python3-dev default-libmysqlclient-dev build-essential
```

### Step 9: Run Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 10: Create Superuser

```bash
# Create admin user
python manage.py createsuperuser

# Follow prompts to create admin credentials
```

### Step 11: Collect Static Files

```bash
# Collect static files for production
python manage.py collectstatic --noinput
```

### Step 12: Test the Installation

```bash
# Run development server
python manage.py runserver

# Open browser and navigate to:
# http://localhost:8000
# http://localhost:8000/admin
```

## Configuration Files

### requirements.txt
Create this file in the project root:
```txt
Django==4.1.3
mysqlclient==2.1.1
Pillow==9.3.0
python-decouple==3.6
django-crispy-forms==1.14.0
crispy-bootstrap5==0.6
django-extensions==3.2.1
```

### .env File (Optional)
Create `.env` file for environment variables:
```env
SECRET_KEY=your-secret-key-here
DB_NAME=decentralized_voting
DB_USER=voting_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=3306
DEBUG=True
```

Update `settings.py` to use environment variables:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

## Troubleshooting

### Common Issues

#### 1. MySQL Connection Error
```
Error: (2003, "Can't connect to MySQL server")
```
**Solution**: 
- Ensure MySQL service is running
- Check credentials in settings.py
- Verify firewall settings

#### 2. ModuleNotFoundError
```
ModuleNotFoundError: No module named 'mysqlclient'
```
**Solution**:
- Activate virtual environment
- Install mysqlclient: `pip install mysqlclient`

#### 3. Migration Errors
```
django.db.utils.OperationalError: (1054, "Unknown column")
```
**Solution**:
- Delete migration files in app/migrations/
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`

#### 4. Static Files Not Loading
**Solution**:
- Run `python manage.py collectstatic`
- Check STATIC_URL and STATICFILES_DIRS in settings.py

#### 5. Permission Denied (Linux/macOS)
**Solution**:
```bash
# Fix permissions
sudo chown -R $USER:$USER /path/to/project
chmod -R 755 /path/to/project
```

### Port Conflicts
If port 8000 is in use:
```bash
# Use different port
python manage.py runserver 8080

# Or kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

## Development Setup

### VS Code Configuration
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

### Git Configuration
```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Create .gitignore
echo "venv/
__pycache__/
*.pyc
.env
db.sqlite3
media/
.DS_Store
*.log" > .gitignore
```

## Production Considerations

### Security Settings
```python
# settings.py for production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Performance Optimization
```python
# Database optimization
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 60,
    }
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## Next Steps

After successful installation:

1. **Explore the Admin Panel**: Visit `http://localhost:8000/admin`
2. **Create Test Data**: Add sample elections and candidates
3. **Test User Registration**: Register test voters
4. **Review Documentation**: Read other documentation files
5. **Customize**: Modify templates and styling as needed

## Support

For installation issues:
- Check the [Troubleshooting](#troubleshooting) section
- Review [Django Documentation](https://docs.djangoproject.com/)
- Open an issue on [GitHub](https://github.com/yourusername/DECENTRALIZED-ONLINE-VOTING-SYSTEM-USING-BLOCKCHAIN/issues)

---

**Note**: This installation guide is for development purposes. For production deployment, refer to the [Deployment Guide](DEPLOYMENT.md).
