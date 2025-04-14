# Money Maestro - Personal Budgeting App

A full-stack personal budgeting application built with React.js and Flask.

## Features

- Track expenses by date, category, and amount
- View spending history in a tabular format
- Modern responsive React.js frontend
- Flask REST API backend
- Data persistence with CSV storage

## Requirements

- Python 3.6+
- Node.js and npm
- Flask (and dependencies in requirements.txt)

## Setup Instructions

1. Clone this repository
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install React dependencies:
   ```
   cd frontend
   npm install
   cd ..
   ```

## Running the Application

### Development Mode

To run both the Flask backend and React frontend in development mode:

1. Start the Flask backend:
   ```
   python app.py
   ```
   This will start the Flask server on http://localhost:5000

2. In a separate terminal, start the React frontend:
   ```
   cd frontend
   npm start
   ```
   This will start the React dev server on http://localhost:3000

### Production Mode

For production deployment:

1. Build the React frontend:
   ```
   cd frontend
   npm run build
   cd ..
   ```

2. Start the Flask app, which will serve the built React app:
   ```
   python app.py
   ```
   
3. Access the application at http://localhost:5000

## Project Structure

- `/app.py` - Flask backend application
- `/frontend/` - React frontend 
- `/data/` - Data storage (CSV files)
- `/templates/` - Legacy Flask templates (kept for backward compatibility)
