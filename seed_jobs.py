import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_analyzer.settings')
django.setup()

from core.models import Job

# 50 diverse job descriptions spanning Software, Data, QA, Design, PM, MBA, Sales, Marketing, HR, Finance, etc.
jobs_data = [
    # --- Engineering & Tech ---
    {"title": "Frontend Developer (React)", "description": "Looking for a creative frontend developer skilled in React, JavaScript, HTML, CSS. Experience with state management (Redux) and responsive design is required."},
    {"title": "Backend Software Engineer", "description": "We are looking for a backend engineer proficient in Python, Django, SQL, and AWS. Experience with Docker and APIs is required."},
    {"title": "Full Stack Engineer", "description": "Join our agile team as a Full Stack Engineer. You will work with Node.js, React, MongoDB, PostgreSQL, and AWS to build scalable web applications. Strong communication skills needed."},
    {"title": "iOS Developer", "description": "Mobile app developer needed with strong Swift and Objective-C skills. Experience with CoreData, iOS SDKs, and publishing to the App Store is highly valued."},
    {"title": "Android Developer", "description": "Seeking an Android developer proficient in Kotlin and Java. Must have experience with Android Studio, RESTful APIs, and material design principles."},
    {"title": "DevOps Engineer", "description": "We need a DevOps engineer to manage our cloud infrastructure. Required skills: AWS, Docker, Kubernetes, Linux, Bash, and CI/CD pipelines."},
    {"title": "Site Reliability Engineer (SRE)", "description": "Looking for an SRE to ensure system uptime and performance. Skills: Python, Go, Kubernetes, Terraform, monitoring tools (Prometheus, Grafana), and incident management."},
    {"title": "Cloud Architect", "description": "Design and oversee cloud infrastructure. Requires deep expertise in AWS/GCP/Azure, microservices architecture, security, and cloud networking."},
    {"title": "Cybersecurity Analyst", "description": "Protect our networks and systems. Requires knowledge of firewalls, encryption, offensive security (ethical hacking), risk assessment, and incident response."},
    {"title": "Blockchain Developer", "description": "Seeking an engineer to build decentralized apps. Required: Solidity, Ethereum, smart contracts, cryptography, and Web3.js."},
    {"title": "Quality Assurance (QA) Tester", "description": "Manual and automated testing role. Skills required: Selenium, Cypress, Jira, writing test cases, and understanding Agile/Scrum methodologies."},
    {"title": "Game Developer", "description": "Develop 3D games using Unity or Unreal Engine. Requires strong C++, C#, physics engines, and graphics programming."},

    # --- Data & AI ---
    {"title": "Data Scientist", "description": "Seeking a Data Scientist proficient in Python, Machine Learning, Deep Learning, Pandas, Numpy, and Scikit-Learn. Must have strong data analysis and problem-solving skills."},
    {"title": "Machine Learning Engineer", "description": "Deploy AI models to production. Required: Python, TensorFlow, PyTorch, model optimization, Docker, and MLflow."},
    {"title": "Data Analyst", "description": "Analyze business data to find insights. Skills: SQL, Excel, Power BI, Tableau, Python, and strong communication skills."},
    {"title": "Data Engineer", "description": "Build data pipelines and data warehouses. Skills needed: SQL, Python, Apache Spark, Airflow, Snowflake, and AWS Redshift."},
    {"title": "NLP Engineer", "description": "Specialist in Natural Language Processing. Required: Python, Spacy, NLTK, HuggingFace transformers, LLMs, and Python."},
    {"title": "Computer Vision Engineer", "description": "Develop image processing models. Required: OpenCV, PyTorch, CNNs, image segmentation, and object detection."},

    # --- Product & Design ---
    {"title": "Product Manager", "description": "Lead product strategy from ideation to launch. Skills: Agile, roadmapping, user research, data analysis, A/B testing, and cross-functional leadership."},
    {"title": "Technical Product Manager", "description": "Bridge the gap between business and engineering. Requires software architecture understanding, API integrations, Agile, and strong analytical skills."},
    {"title": "UX/UI Designer", "description": "Design intuitive user experiences. Skills: Figma, Sketch, wireframing, prototyping, user-centered design, and basic HTML/CSS."},
    {"title": "Graphic Designer", "description": "Create visual concepts for branding and marketing. Required: Adobe Photoshop, Illustrator, InDesign, typography, and color theory."},
    {"title": "Product Analyst", "description": "Analyze product usage metrics to drive features. Required: SQL, mixpanel/amplitude, A/B testing, and data visualization."},

    # --- Sales & Marketing ---
    {"title": "Digital Marketing Manager", "description": "Oversee digital campaigns. Skills: SEO, SEM, content marketing, Google Analytics, social media marketing, and email marketing."},
    {"title": "SEO Specialist", "description": "Optimize website ranking and traffic. Required: Keyword research, on-page SEO, link building, Google Search Console, and content strategy."},
    {"title": "Content Marketer / Writer", "description": "Create engaging blog posts and copy. Skills: Copywriting, SEO, storytelling, grammar, and content management systems (CMS)."},
    {"title": "Social Media Manager", "description": "Manage brand presence. Required: Hootsuite, social media marketing, content calendar, community management, and analytics."},
    {"title": "B2B Sales Executive", "description": "Drive B2B revenue. Skills: Outbound sales, CRM (Salesforce), cold calling, negotiation, client relations, and lead generation."},
    {"title": "Account Executive (SaaS)", "description": "Close software deals. Requires presentation skills, pipeline management, CRM, forecasting, and closing strategies."},
    {"title": "Sales Development Representative (SDR)", "description": "Generate quality pipeline. Skills: Cold emailing, prospecting, CRM (Hubspot), communication, and resilience."},
    {"title": "Customer Success Manager", "description": "Ensure client retention and satisfaction. Skills: Onboarding, account management, churn reduction, upselling, and communication."},
    
    # --- Business, MBA, Leadership ---
    {"title": "Management Consultant", "description": "Help businesses solve complex problems. Skills: Strategic planning, financial modeling, presentations (PowerPoint), data analysis, and problem solving."},
    {"title": "Business Development Manager", "description": "Identify new business opportunities. Skills: Strategic partnerships, negotiation, brand management, B2B sales, and networking."},
    {"title": "Operations Manager", "description": "Oversee daily business activities. Skills: Supply chain logistics, process optimization, budgeting, team leadership, and P&L management."},
    {"title": "Strategy Director (MBA Preferred)", "description": "Guide corporate strategy. Required: Strategic planning, M&A analysis, financial forecasting, executive communication, and data-driven decision making."},
    {"title": "Project Manager", "description": "Deliver projects on time and budget. Skills: Agile, Scrum, resource allocation, risk management, Jira, and stakeholder communication."},
    
    # --- Finance & Accounting ---
    {"title": "Financial Analyst", "description": "Analyze financial data and business trends. Skills: Financial modeling, Excel, valuation, forecasting, and accounting principles."},
    {"title": "Accountant", "description": "Manage financial records. Skills: GAAP, bookkeeping, tax preparation, QuickBooks, and financial reporting."},
    {"title": "Investment Banker", "description": "Raise capital and advise on M&A. Skills: DCF valuation, pitch decks, financial modeling, negotiation, and high-pressure work resilience."},
    {"title": "Risk Analyst", "description": "Identify and mitigate financial risks. Skills: Quantitative analysis, SQL, Python, risk assessment models, and compliance."},
    
    # --- Human Resources (HR) & Operations ---
    {"title": "HR Manager", "description": "Manage employee lifecycle. Skills: Recruitment, employee relations, performance management, employment law, and payroll systems."},
    {"title": "Technical Recruiter", "description": "Hire engineering talent. Required: Sourcing, interviewing, understanding of tech stacks, LinkedIn Recruiter, and negotiation."},
    {"title": "Operations Analyst", "description": "Analyze operational processes. Skills: Data analysis, process improvement, Excel, supply chain, and reporting."},

    # --- Other Specific Niches ---
    {"title": "Healthcare Administrator", "description": "Manage medical facilities. Skills: Healthcare compliance, budgeting, staff scheduling, EMR systems, and leadership."},
    {"title": "Supply Chain Manager", "description": "Oversee logistics and inventory. Skills: Inventory management, procurement, negotiation, ERP systems, and cost reduction."},
    {"title": "Legal Counsel", "description": "Provide legal advice to the corporation. Skills: Corporate law, contract drafting, negotiation, compliance, and IP law."},
    {"title": "Civil Engineer", "description": "Design infrastructure projects. Required: AutoCAD, structural analysis, project management, and construction materials."},
    {"title": "Mechanical Engineer", "description": "Design mechanical systems. Skills: SolidWorks, thermodynamics, robotics, manufacturing processes, and problem solving."},
    {"title": "Event Coordinator", "description": "Plan and execute events. Skills: Budgeting, vendor negotiation, logistics, marketing, and communication."},
    {"title": "Customer Support Specialist", "description": "Assist customers with inquiries. Skills: Zendesk, troubleshooting, empathy, communication, and conflict resolution."}
]

def seed_jobs():
    created_count = 0
    skipped_count = 0
    
    for job in jobs_data:
        # Check if job already exists
        if not Job.objects.filter(title=job['title']).exists():
            Job.objects.create(title=job['title'], description=job['description'])
            created_count += 1
        else:
            skipped_count += 1
            
    print(f"Total jobs populated: Created {created_count}, Skipped {skipped_count} existing.")

if __name__ == "__main__":
    seed_jobs()
