# Cybersecurity Risk Assessment Framework

## Overview
A comprehensive, web-based Cybersecurity Risk Assessment Framework designed specifically for small and medium-sized businesses. This platform empowers organizations to seamlessly manage their digital assets, identify vulnerabilities, assess cyber threats, and generate executive-level risk reports.

## Key Features

### 1. Role-Based Access Control (RBAC)
- **Admin Accounts:** Register and manage the organization's profile, digital assets, threats, and assessments. Admins have full control over the workspace.
- **Employee Accounts:** Admins can provision a shared login for their employees. Employees can log in to view the dashboard and risk reports, ensuring transparency without compromising configuration security.
- **Access Revocation:** Admins can instantly revoke employee access with a single click if an employee resigns or changes roles.

### 2. Premium UI/UX & Design
- **Dark Mode Glassmorphism:** The entire application features a stunning, state-of-the-art dark mode aesthetic utilizing translucent "glass" cards, vibrant gradients, and smooth micro-animations.
- **Responsive Navigation:** A dynamic sidebar and top navigation bar that automatically adapts to the user's role (Admin vs. Employee) and displays the organization's name prominently.
- **Interactive Visualizations:** Includes a dynamic Doughnut Chart (via Chart.js) on the dashboard that visualizes risk distribution in real-time.

### 3. Core Assessment Engine
- **Asset Management:** Catalog all digital and physical assets (e.g., servers, databases, endpoints) with their respective values.
- **Threat Catalog:** Maintain a repository of potential cyber threats (e.g., Ransomware, Phishing, DDoS).
- **Risk Assessment:** Map threats to specific assets, calculate likelihood and impact, and generate an automated Risk Score (Low, Medium, High, Critical).
- **Risk Matrix:** A visual grid displaying the relationship between risk likelihood and impact.
- **Mitigation Recommendations:** The engine automatically suggests mitigation strategies based on the identified risks.

### 4. Reporting
- **Executive Reports:** Generate comprehensive HTML reports summarizing the organization's risk posture, top vulnerabilities, and actionable mitigation plans.

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite (via SQLAlchemy ORM)
- **Frontend:** HTML5, CSS3 (Custom Variables), Bootstrap 5, FontAwesome
- **Charts:** Chart.js

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd cyber-risk-assessment
   ```

2. **Create a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database:**
   ```bash
   python app.py
   ```
   *(Note: The database will be created automatically in the `instance/` folder on first run).* 
   You can optionally run `python seed/seed_data.py` to populate dummy data.

5. **Run the Application:**
   ```bash
   flask run
   ```
   The application will be available at `http://127.0.0.1:4444
   /`.

## Usage Flow
1. Register as a new Admin.
2. Navigate to **Business Profile** and set up your company details.
3. Add your digital infrastructure under **Assets**.
4. Define potential vulnerabilities under **Threats**.
5. Go to **New Assessment** to evaluate the risks on your assets.
6. Review the **Dashboard** and **Risk Matrix** for a high-level overview.
7. Generate an **Executive Report** for stakeholders.
8. (Optional) Provide **Employee Access** for team visibility.
