#!/usr/bin/env bash

# Print the current directory for debugging
echo "Current directory: $(pwd)"

# Navigate to the frontend directory
echo "Navigating to frontend..."
cd frontend

# Install frontend dependencies
echo "Installing npm dependencies..."
npm install

# Build the React frontend
echo "Building the frontend..."
npm run build

# Navigate back to the root
cd ..

# Remove Poetry (to avoid interference)
echo "Removing Poetry..."
pip uninstall poetry -y

# Install Python dependencies using pip
echo "Installing Python dependencies with pip..."
pip install -r requirements.txt

# Start the Flask app using gunicorn
echo "Starting gunicorn..."
gunicorn app:app

