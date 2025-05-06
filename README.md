
# CS122 Group 5: Money Maestro

Members: Kevin Cui, Arjun Bemarkar

## Project Overview

Repository is a finance website designed to show visualizations of user expenses.
Users would input date, spending category, item, and amount. This will be shown in a pie chart to show the split in the total spending. A line graph will be used to handle spending over a period of time.

## Live Website

Access the deployed web application here: [https://cs122-group5.uw.r.appspot.com/](https://cs122-group5.uw.r.appspot.com/)

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/CCLDArjun/personal-budgeting-app.git
   ```

2. **Create and activate a virtual environment and deployment:**

   ```bash
   python -m venv .venv
   source ./.venv/bin/activate  # On Windows: .\.venv\Scripts\activate
   cd appengine
   pip install -r requirements.txt
   python app.py
   ```

## Pipeline Overview

1. **Data Handling:**
   - CSV for data handling.
   - Generate visualizations to show money usage and usage over a period of time.

2. **Web Application Development:**
   - Utilizes Flask framework for web development.
   - Dash for styling and graphs.
   - Deploy the application using Google App Engine or app.py for local.

## Directory Structure

- `/appengine/`: Houses the web app functionality, components, data, routes.
   - `/assets/`: For custom CSS styling.
   - `/components/`: Functions used for page callbacks.
      - `/data/`: Data for local deployment and testing.
   - `/pages/`: Routes for each page of the website.
