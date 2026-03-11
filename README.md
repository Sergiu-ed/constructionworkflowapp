# Construct Manager Pro

Construct Manager Pro is a comprehensive web-based platform tailored for construction site managers (Byggledare). It offers an integrated suite of tools designed to streamline daily operations, project planning, team management, and financial aspects like estimating and quoting.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Localization](#localization)

## Features

- **Dynamic Quotation System (Oferta):** Create thorough and professional quotes including dimensions computation, detailed material and labor separation, ROT deduction integration, vehicle tracking, and multi-language PDF generation.
- **Calculator & Estimates:** Comprehensive calculator for work items related to demolition, preparation, waterproofing, ceiling/painting, fixtures, plumbing, and electrical work.
- **Time & Resource Planning:** Quickly define required workers, start dates, and calculate workdays (excluding weekends). A visual timeline (Gantt Chart overview) tracks project statuses.
- **Vehicle & Transportation Log:** Keep track of vehicle odometers, driven distance, and transport costs.
- **Employee & Customer Management:** Easily manage the details corresponding to various project stakeholders.
- **Localization:** The platform interface and most dynamically generated strings support multiple languages natively (Swedish, English, and Romanian).

## Architecture

The system is split into a frontend application served statically via `Express.js`, and a `Flask` (Python) backend for API operations and database management.

### Tech Stack
* **Frontend:** HTML5, Alpine.js logic built via vanilla JavaScript context, Tailwind CSS for beautiful styling. Fully responsive and mobile-first approach.
* **Backend:** Python + Flask API serving data models via SQLAlchemy/SQLite.
* **Server:** Node.js (Express server) hosting the static web content.

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.12+)

### 1. Setup Backend (Python/Flask)
```bash
# Clone the repository
git clone https://github.com/Sergiu-ed/constructionworkflowapp.git
cd constructionworkflowapp

# Activate virtual environment (Windows)
.\\venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask App (defaults to port 5000)
python app.py
```

### 2. Setup Frontend (Node/Express)
```bash
# Navigate to the frontend directory
cd firma-constructii-app

# Install dependencies (if needed)
npm install

# Start the web client (runs on port 3000)
node index.js
```

### 3. Usage
Navigate to `http://localhost:3000` via your preferred web browser. The application will synchronize the calculator, generated quotes, and active settings using `localStorage`.

## Project Structure

```text
├── .env                        # Python backend environment file
├── app.py                      # Flask backend API routing & logic
├── requirements.txt            # Python dependencies
├── translate_index.py          # Helper scripts for localization tagging
├── firma-constructii-app/      # Main Application Folder (Frontend)
│   ├── index.js                # Express app entry point
│   └── public/                 # Static content root
│       ├── index.html          # Main Dashboard
│       ├── oferta.html         # Quotation & Estimation Creator
│       ├── calculator.html     # Construction Math / Quantity Calculator
│       ├── ...                 # Other pages like Employees, Vehicles etc.
```

## Localization (i18n)

The platform is designed with multilingual capabilities to accommodate diverse teams.
Current native languages supported:
1. `sv` - Swedish
2. `en` - English
3. `ro` - Romanian

Adding new locales requires updating the `translations` and `uiTranslations` maps within the Javascript contexts of HTML files, while ensuring the `data-i18n` bindings remain persistent across static tags.
