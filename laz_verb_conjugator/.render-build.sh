#!/usr/bin/env bash

# Print the current directory
echo "Current directory: $(pwd)"

# Make sure the frontend directory exists
if [ ! -d "frontend" ]; then
  echo "Frontend directory not found!"
  exit 1
fi

# Navigate to the frontend directory
echo "Navigating to frontend..."
cd frontend

# Install frontend dependencies
echo "Installing npm dependencies..."
npm install || { echo "npm install failed"; exit 1; }

# Build the React frontend
echo "Building the frontend..."
npm run build || { echo "npm run build failed"; exit 1; }

# Navigate back to the root
echo "Navigating back to root..."
cd ..

echo "Build completed successfully."
