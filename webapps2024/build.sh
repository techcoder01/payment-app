#!/bin/bash

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found"
    exit 1
fi

# Ensure pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 could not be found"
    exit 1
fi

# Upgrade pip
pip3 install --upgrade pip

# Install setuptools (usually already installed, but ensure it's up-to-date)
pip3 install --upgrade setuptools

# Install distutils if not already installed
if ! python3 -c "import distutils" &> /dev/null; then
    echo "distutils is not installed, installing now..."
    
    # Use appropriate package manager for your system
    if command -v apt-get &> /dev/null; then
        apt-get update
        apt-get install -y python3-distutils  # Replace with appropriate package name on non-Debian systems
    elif command -v yum &> /dev/null; then
        yum install -y python3-distutils  # Replace with appropriate package name on CentOS/RHEL
    else
        echo "Unsupported package manager. Please install distutils manually."
        exit 1
    fi
fi

# Install dependencies from requirements.txt
pip3 install -r requirements.txt

# Activate virtual environment if needed
# source <venv>/bin/activate

# Run Django collectstatic
python3 manage.py collectstatic --no-input
