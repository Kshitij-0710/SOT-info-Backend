import os
import sys
import django
import random
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Set up Django environment
sys.path.append('.')  # Add the current directory to the Python path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sotinfo.settings')  # Replace with your actual settings module
django.setup()

# Import your models after Django setup
from authentication.models import User
from catogories.models import Form  # Assuming this is the correct path

# Sample data for generation
tech_stacks = [
    ["Python", "Django", "React", "PostgreSQL"],
    ["JavaScript", "Node.js", "Express", "MongoDB"],
    ["Java", "Spring Boot", "MySQL", "Angular"],
    ["Python", "TensorFlow", "Keras", "scikit-learn"],
    ["C++", "Qt", "SQLite"],
    ["Swift", "Core Data", "Firebase"],
    ["Ruby on Rails", "Redis", "PostgreSQL"],
    ["Flutter", "Dart", "Firebase"],
    ["Go", "Docker", "Kubernetes", "AWS"],
    ["PHP", "Laravel", "MySQL", "Vue.js"]
]

team_members_options = [
    "John Doe, Jane Smith",
    "Alex Johnson, Taylor Williams",
    "Solo Project",
    "Sam Brown, Chris Davis, Jordan Wilson",
    "Team of 5 members",
    "Research Group Alpha",
    "Innovation Team",
    "Cross-functional team of developers and designers",
    "International collaboration with 3 universities",
    "Industry-academic partnership"
]

project_urls = [
    "https://github.com/username/project1",
    "https://project-demo.example.com",
    "https://research-paper.example.org/publication/123",
    "https://www.example.com/portfolio/project",
    "https://gitlab.com/username/project",
    "N/A",
    "https://play.google.com/store/apps/details?id=com.example.app",
    "https://apps.apple.com/app/id123456789",
    "https://demo.example.net",
    "https://www.example.org/research/papers/2023/paper.pdf"
]

achievements_options = [
    ["First Place Hackathon 2023", "Featured in Tech Magazine"],
    ["10,000+ Downloads", "4.8 Star Rating"],
    ["Published in IEEE Journal", "Cited 25+ times"],
    ["Reduced processing time by 40%", "Increased user engagement by 35%"],
    ["Best Student Project Award", "Patent Filed"],
    ["Open Source Contribution with 50+ stars on GitHub"],
    ["Invited talk at Industry Conference", "Featured Case Study"],
    ["Successfully deployed to production", "Serving 1000+ daily users"],
    ["Research grant awarded", "Collaboration with leading industry partner"],
    ["Innovator Award 2023", "Published in ACM Conference"]
]

# Achievement project data
achievement_titles = [
    "National Coding Championship Victory",
    "Student Innovation Award 2023",
    "International Science Fair Gold Medal",
    "Young Researcher Recognition Program",
    "Academic Excellence Award for Technical Innovation",
    "Industry-Recognized Certification Achievement",
    "Professional Development Leadership Award",
    "Outstanding Technical Contribution Award",
    "Community Impact Recognition for Tech Solution",
    "Entrepreneurship Challenge Winner"
]

achievement_descriptions = [
    "Led a team to victory in the National Coding Championship, demonstrating exceptional problem-solving skills and algorithm optimization techniques.",
    "Received the prestigious Student Innovation Award for developing a novel approach to sustainable energy management using machine learning algorithms.",
    "Awarded the Gold Medal at the International Science Fair for research on efficient data structures for real-time applications.",
    "Selected for the Young Researcher Recognition Program for outstanding contributions to the field of artificial intelligence ethics.",
    "Earned the Academic Excellence Award for developing an innovative approach to database optimization that reduced query times by 60%.",
    "Achieved top scores in industry-recognized certification exams, placing in the 99th percentile nationwide.",
    "Selected for the Professional Development Leadership Award for mentoring junior developers and creating comprehensive learning resources.",
    "Recognized with the Outstanding Technical Contribution Award for developing key features that enhanced platform performance.",
    "Received Community Impact Recognition for developing a technology solution that addressed critical needs in underserved communities.",
    "Won the Entrepreneurship Challenge with a technology startup proposal that attracted seed funding from industry investors."
]

# Research project data
research_titles = [
    "Machine Learning Approaches to Predictive Maintenance",
    "Novel Algorithms for Distributed Computing Efficiency",
    "Comparative Analysis of Database Optimization Techniques",
    "Ethical Implications of AI in Healthcare Decision Making",
    "Secure Communication Protocols for IoT Environments",
    "Blockchain Applications in Supply Chain Management",
    "Natural Language Processing for Educational Assessment",
    "Quantum Computing Impacts on Cryptographic Security",
    "Sustainable Computing: Energy Efficiency in Data Centers",
    "Augmented Reality Applications in STEM Education"
]

research_descriptions = [
    "Investigated machine learning techniques to predict equipment failures before they occur, resulting in a model with 92% accuracy on test data.",
    "Developed and analyzed novel algorithms for improving efficiency in distributed computing environments, demonstrating a 30% reduction in processing time.",
    "Conducted empirical studies of various database optimization techniques across different workloads, providing actionable insights for system architects.",
    "Explored the ethical considerations and implications of using AI in critical healthcare decisions, proposing a framework for responsible implementation.",
    "Researched and developed secure communication protocols specifically designed for resource-constrained IoT devices in industrial settings.",
    "Investigated practical applications of blockchain technology in supply chain management, with focus on traceability and fraud prevention.",
    "Developed natural language processing techniques to automate educational assessment processes while maintaining evaluation quality.",
    "Analyzed potential impacts of quantum computing advancements on current cryptographic security measures, proposing mitigation strategies.",
    "Researched innovative approaches to reduce energy consumption in data centers while maintaining performance requirements.",
    "Explored effective applications of augmented reality technology to enhance STEM education outcomes, with controlled studies in classroom environments."
]

# Project data
project_titles = [
    "E-commerce Platform with Recommendation Engine",
    "Mobile Health Monitoring Application",
    "Smart Home Automation System",
    "Financial Portfolio Management Dashboard",
    "Social Media Analytics Tool",
    "Multiplayer Online Game Development",
    "Content Management System with Advanced Workflows",
    "Real-time Transportation Tracking System",
    "Cross-platform Mobile Development Framework",
    "AI-Powered Personal Assistant Application"
]

project_descriptions = [
    "Built a comprehensive e-commerce platform featuring a machine learning-based recommendation engine that improved conversion rates by 23%.",
    "Developed a mobile application for health monitoring that integrates with wearable devices and provides personalized health insights.",
    "Created a smart home automation system using IoT devices, supporting voice commands and adaptable schedules based on user behavior.",
    "Designed and implemented a financial portfolio management dashboard with real-time data visualization and performance analytics.",
    "Built a social media analytics tool that processes engagement metrics across platforms and generates actionable marketing insights.",
    "Developed a multiplayer online game with real-time interaction capabilities, custom physics engine, and advanced graphics rendering.",
    "Created a content management system with advanced workflow features, version control, and role-based access control for enterprise use.",
    "Implemented a real-time transportation tracking system with predictive arrival times using GPS data and traffic pattern analysis.",
    "Developed a cross-platform mobile development framework that significantly reduced code duplication and maintenance costs.",
    "Built an AI-powered personal assistant application with natural language processing capabilities for task management and scheduling."
]

# Student specific data
student_first_names = [
    "Aiden", "Sophia", "Ethan", "Olivia", "Liam", 
    "Emma", "Noah", "Ava", "Mason", "Isabella", 
    "Lucas", "Mia", "Oliver", "Charlotte", "Elijah"
]

student_last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"
]

# Faculty specific data
faculty_first_names = [
    "William", "Elizabeth", "James", "Katherine", "Michael",
    "Margaret", "Robert", "Jennifer", "David", "Patricia",
    "Richard", "Susan", "Charles", "Barbara", "Joseph"
]

faculty_last_names = [
    "Taylor", "Moore", "Jackson", "White", "Harris",
    "Martin", "Thompson", "Young", "Clark", "Walker",
    "Hall", "Allen", "Wright", "King", "Scott"
]

# Domains for generating emails
domains = ["example.com", "university.edu", "college.org", "institute.net", "academy.org"]

def random_date(start_date=date(2022, 1, 1), days_range=730):
    """Generate a random date within range"""
    random_days = random.randint(0, days_range)
    return start_date + timedelta(days=random_days)

def generate_phone_number():
    """Generate a random 10-digit phone number"""
    return f"+1{random.randint(2000000000, 9999999999)}"

def create_users():
    """Create student and faculty users"""
    created_users = {
        'STUDENT': [],
        'FACULTY': []
    }
    
    # Create 5 student users
    for i in range(5):
        first_name = random.choice(student_first_names)
        last_name = random.choice(student_last_names)
        name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
        phone_number = generate_phone_number()
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            print(f"User with email {email} already exists. Skipping.")
            continue
        
        # Create student user
        user = User.objects.create(
            email=email,
            name=name,
            phone_number=phone_number,
            user_type='STUDENT',
            password=make_password('password123'),  # Default password
            is_verified=True
        )
        created_users['STUDENT'].append(user)
        print(f"Created student user: {name} ({email})")
    
    # Create 5 faculty users
    for i in range(5):
        first_name = random.choice(faculty_first_names)
        last_name = random.choice(faculty_last_names)
        name = f"Dr. {first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
        phone_number = generate_phone_number()
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            print(f"User with email {email} already exists. Skipping.")
            continue
        
        # Create faculty user
        user = User.objects.create(
            email=email,
            name=name,
            phone_number=phone_number,
            user_type='FACULTY',
            password=make_password('password123'),  # Default password
            is_verified=True
        )
        created_users['FACULTY'].append(user)
        print(f"Created faculty user: {name} ({email})")
    
    return created_users

def create_projects_for_user(user, num_projects=10):
    """Create projects for a specific user"""
    print(f"Creating projects for user: {user.name} ({user.user_type})")
    
    # Create achievements
    for i in range(num_projects):
        # Generate random dates
        from_date = random_date()
        to_date = from_date + timedelta(days=random.randint(30, 365)) if random.random() > 0.2 else None
        
        # Set some entries as top 6
        is_top_6 = True if i < 2 else False  # Make first 2 entries top 6
        
        # Create achievement
        form = Form(
            title=achievement_titles[i % len(achievement_titles)],
            description=achievement_descriptions[i % len(achievement_descriptions)],
            team_members=random.choice(team_members_options),
            tech_stack=random.choice(tech_stacks),
            projecturl=random.choice(project_urls),
            achivements=random.choice(achievements_options),
            from_date=from_date,
            to_date=to_date,
            category='achievement',
            is_top_6=is_top_6,
            user=user,
            user_type=user.user_type
        )
        form.save()
        print(f"  - Created achievement: {form.title}")
    
    # Create research projects
    for i in range(num_projects):
        # Generate random dates
        from_date = random_date()
        to_date = from_date + timedelta(days=random.randint(30, 365)) if random.random() > 0.2 else None
        
        # Set some entries as top 6
        is_top_6 = True if i < 2 else False  # Make first 2 entries top 6
        
        # Create research project
        form = Form(
            title=research_titles[i % len(research_titles)],
            description=research_descriptions[i % len(research_descriptions)],
            team_members=random.choice(team_members_options),
            tech_stack=random.choice(tech_stacks),
            projecturl=random.choice(project_urls),
            achivements=random.choice(achievements_options),
            from_date=from_date,
            to_date=to_date,
            category='research',
            is_top_6=is_top_6,
            user=user,
            user_type=user.user_type
        )
        form.save()
        print(f"  - Created research: {form.title}")
    
    # Create projects
    for i in range(num_projects):
        # Generate random dates
        from_date = random_date()
        to_date = from_date + timedelta(days=random.randint(30, 365)) if random.random() > 0.2 else None
        
        # Set some entries as top 6
        is_top_6 = True if i < 2 else False  # Make first 2 entries top 6
        
        # Create project
        form = Form(
            title=project_titles[i % len(project_titles)],
            description=project_descriptions[i % len(project_descriptions)],
            team_members=random.choice(team_members_options),
            tech_stack=random.choice(tech_stacks),
            projecturl=random.choice(project_urls),
            achivements=random.choice(achievements_options),
            from_date=from_date,
            to_date=to_date,
            category='project',
            is_top_6=is_top_6,
            user=user,
            user_type=user.user_type
        )
        form.save()
        print(f"  - Created project: {form.title}")

def main():
    """Main function to create users and projects"""
    try:
        print("Starting to create users and projects...")
        
        # Create users
        created_users = create_users()
        
        # Create projects for each user
        for user_type, users in created_users.items():
            print(f"\nCreating projects for {user_type} users...")
            for user in users:
                create_projects_for_user(user)
        
        print("\nDatabase population completed successfully!")
        
        # Print summary
        student_count = User.objects.filter(user_type='STUDENT').count()
        faculty_count = User.objects.filter(user_type='FACULTY').count()
        achievement_count = Form.objects.filter(category='achievement').count()
        research_count = Form.objects.filter(category='research').count()
        project_count = Form.objects.filter(category='project').count()
        
        print("\nSummary:")
        print(f"Total Students: {student_count}")
        print(f"Total Faculty: {faculty_count}")
        print(f"Total Achievements: {achievement_count}")
        print(f"Total Research Projects: {research_count}")
        print(f"Total Projects: {project_count}")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()