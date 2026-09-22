import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db
from models.user import User
from models.threat import Threat
from models.mitigation import Mitigation
from models.business import Business
from models.asset import Asset
from models.assessment import Assessment

app = create_app()

THREATS_DATA = [
    {
        "name": "Phishing",
        "category": "Social Engineering",
        "description": "Fraudulent attempt to obtain sensitive information by disguising as a trustworthy entity.",
        "likelihood_default": 4,
        "impact_default": 5,
        "mitigations": [
            {"title": "Enable Multi-Factor Authentication", "description": "Require MFA for all user accounts.", "priority": "High"},
            {"title": "Conduct employee security awareness training", "description": "Regularly train employees to recognize phishing attempts.", "priority": "High"},
            {"title": "Use email filtering", "description": "Implement automated filtering for spam and malicious links.", "priority": "Medium"}
        ]
    },
    {
        "name": "Ransomware",
        "category": "Malware",
        "description": "Malicious software that blocks access to a computer system until a sum of money is paid.",
        "likelihood_default": 3,
        "impact_default": 5,
        "mitigations": [
            {"title": "Maintain regular backups", "description": "Keep offline and isolated backups of critical data.", "priority": "Critical"},
            {"title": "Use endpoint protection", "description": "Install and update EDR/antivirus solutions.", "priority": "High"},
            {"title": "Patch systems regularly", "description": "Ensure OS and applications are up to date.", "priority": "High"}
        ]
    },
    {
        "name": "Weak Passwords",
        "category": "Authentication",
        "description": "Use of easily guessable or default passwords that can be cracked.",
        "likelihood_default": 4,
        "impact_default": 4,
        "mitigations": [
            {"title": "Enforce strong password policies", "description": "Require minimum length, complexity, and rotation.", "priority": "High"},
            {"title": "Use password managers", "description": "Provide a corporate password manager.", "priority": "Medium"},
            {"title": "Disable default passwords", "description": "Change all default vendor passwords.", "priority": "High"}
        ]
    },
    {
        "name": "Insider Threat",
        "category": "Human Resources",
        "description": "A malicious or negligent threat to an organization that comes from people within.",
        "likelihood_default": 2,
        "impact_default": 4,
        "mitigations": [
            {"title": "Apply least privilege", "description": "Users should only have access to data needed for their role.", "priority": "High"},
            {"title": "Use role-based access control", "description": "Implement RBAC systems.", "priority": "High"},
            {"title": "Monitor sensitive access", "description": "Log and alert on access to critical data.", "priority": "Medium"}
        ]
    },
    {
        "name": "Data Leakage",
        "category": "Data Security",
        "description": "Unauthorized transfer of classified information from a computer or datacenter to the outside world.",
        "likelihood_default": 3,
        "impact_default": 4,
        "mitigations": [
            {"title": "Data classification", "description": "Identify and classify sensitive data.", "priority": "Medium"},
            {"title": "Encryption", "description": "Encrypt data at rest and in transit.", "priority": "High"},
            {"title": "Data loss prevention", "description": "Implement DLP tools where appropriate.", "priority": "High"}
        ]
    },
    {
        "name": "Unpatched Software",
        "category": "Vulnerability",
        "description": "Software with known vulnerabilities that haven't been updated with security patches.",
        "likelihood_default": 4,
        "impact_default": 4,
        "mitigations": [
            {"title": "Patch management", "description": "Implement a formal patch management process.", "priority": "High"},
            {"title": "Asset inventory", "description": "Maintain an up-to-date inventory of all software.", "priority": "Medium"},
            {"title": "Automatic updates", "description": "Enable auto-updates for standard software.", "priority": "Medium"}
        ]
    },
    {
        "name": "Unauthorized Access",
        "category": "Access Control",
        "description": "Accessing systems or data without proper permission or authorization.",
        "likelihood_default": 3,
        "impact_default": 4,
        "mitigations": [
            {"title": "MFA", "description": "Require multi-factor authentication.", "priority": "High"},
            {"title": "Account monitoring", "description": "Monitor for anomalous login attempts.", "priority": "Medium"}
        ]
    },
    {
        "name": "Social Engineering",
        "category": "Social Engineering",
        "description": "Psychological manipulation of people into performing actions or divulging confidential information.",
        "likelihood_default": 3,
        "impact_default": 3,
        "mitigations": [
            {"title": "Security awareness training", "description": "Train employees to recognize manipulation.", "priority": "High"},
            {"title": "Verification procedures", "description": "Establish procedures to verify requests for sensitive info.", "priority": "Medium"}
        ]
    },
    {
        "name": "Insecure Backups",
        "category": "Data Security",
        "description": "Backups that are not encrypted, tested, or properly isolated.",
        "likelihood_default": 2,
        "impact_default": 5,
        "mitigations": [
            {"title": "Automated backups", "description": "Ensure backups run automatically on schedule.", "priority": "High"},
            {"title": "Backup testing", "description": "Regularly test restoring from backups.", "priority": "High"},
            {"title": "Offline/isolated backup copies", "description": "Keep at least one backup disconnected from the network.", "priority": "Critical"}
        ]
    },
    {
        "name": "Malware",
        "category": "Malware",
        "description": "General malicious software designed to cause damage or gain unauthorized access.",
        "likelihood_default": 4,
        "impact_default": 3,
        "mitigations": [
            {"title": "Endpoint protection", "description": "Use robust antivirus and EDR.", "priority": "High"},
            {"title": "Application whitelisting", "description": "Only allow approved software to run.", "priority": "Medium"}
        ]
    }
]

def seed_db():
    with app.app_context():
        print("Creating all tables...")
        db.create_all()

        print("Seeding threats and mitigations...")
        if Threat.query.count() == 0:
            for t_data in THREATS_DATA:
                threat = Threat(
                    name=t_data['name'],
                    category=t_data['category'],
                    description=t_data['description'],
                    likelihood_default=t_data['likelihood_default'],
                    impact_default=t_data['impact_default']
                )
                db.session.add(threat)
                db.session.flush() # get threat id

                for m_data in t_data['mitigations']:
                    mitigation = Mitigation(
                        threat_id=threat.id,
                        title=m_data['title'],
                        description=m_data['description'],
                        priority=m_data['priority']
                    )
                    db.session.add(mitigation)
            
            db.session.commit()
            print("Threats and mitigations seeded successfully.")
        else:
            print("Threats already seeded.")

        print("Seeding demo user...")
        demo_user = User.query.filter_by(username="demo").first()
        if not demo_user:
            demo_user = User(username="demo", email="demo@example.com")
            demo_user.set_password("password123")
            db.session.add(demo_user)
            db.session.flush()
            print("Demo user created (demo:password123).")
            
            # Case Study 1: ABC Retail Store (assigned to demo user)
            retail_business = Business(user_id=demo_user.id, name="ABC Retail Store", business_type="Retail", number_of_employees=15, number_of_devices=10, description="A small retail store with POS and customer loyalty program.")
            db.session.add(retail_business)
            db.session.flush()
            
            assets_to_add = [
                Asset(business_id=retail_business.id, name="POS system", category="Hardware", importance=5),
                Asset(business_id=retail_business.id, name="Customer information", category="Data", importance=5),
                Asset(business_id=retail_business.id, name="Employee computers", category="Hardware", importance=3),
                Asset(business_id=retail_business.id, name="Financial records", category="Data", importance=4),
            ]
            db.session.add_all(assets_to_add)
            
            db.session.commit()
            print("Case Study 1 (Retail) assets added to demo user.")
            
        print("Seeding other case studies...")
        user_edu = User.query.filter_by(username="edu_demo").first()
        if not user_edu:
            user_edu = User(username="edu_demo", email="edu@example.com")
            user_edu.set_password("password123")
            db.session.add(user_edu)
            db.session.flush()
            
            edu_biz = Business(user_id=user_edu.id, name="Springfield Educational Institute", business_type="Education", number_of_employees=40, number_of_devices=150, description="Local school with student database and lab computers.")
            db.session.add(edu_biz)
            db.session.flush()
            
            db.session.add_all([
                Asset(business_id=edu_biz.id, name="Student database", category="Data", importance=5),
                Asset(business_id=edu_biz.id, name="Website", category="Cloud", importance=3),
                Asset(business_id=edu_biz.id, name="Faculty records", category="Data", importance=4),
            ])
            db.session.commit()
            
        user_it = User.query.filter_by(username="it_demo").first()
        if not user_it:
            user_it = User(username="it_demo", email="it@example.com")
            user_it.set_password("password123")
            db.session.add(user_it)
            db.session.flush()
            
            it_biz = Business(user_id=user_it.id, name="TechSolutions IT", business_type="IT Services", number_of_employees=25, number_of_devices=35, description="Small IT firm developing software and hosting client data.")
            db.session.add(it_biz)
            db.session.flush()
            
            db.session.add_all([
                Asset(business_id=it_biz.id, name="Source code repositories", category="Data", importance=5),
                Asset(business_id=it_biz.id, name="Client cloud resources", category="Cloud", importance=5),
                Asset(business_id=it_biz.id, name="Employee laptops", category="Hardware", importance=4),
            ])
            db.session.commit()

if __name__ == '__main__':
    seed_db()
