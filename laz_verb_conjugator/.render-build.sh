#!/usr/bin/env bash

# Navigate to the frontend directory
cd frontend

# Install frontend dependencies
npm install

# Build the React frontend
npm run build

# Navigate back to the root (where app.py is)
cd ..
