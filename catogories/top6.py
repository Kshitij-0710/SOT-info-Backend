import os
import sys
import django
import random

# Set up Django environment
sys.path.append('.')  # Add the current directory to the Python path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sotinfo.settings')  # Replace with your actual settings module
django.setup()

# Import your models after Django setup
from authentication.models import User
from catogories.models import Form  # Replace with your actual app name

def select_top_6_by_user_type():
    """
    Randomly selects 6 forms for each category (achievement, research, project) 
    for each user type (STUDENT, FACULTY) and marks them as top 6.
    First resets all existing top 6 selections.
    """
    try:
        # Reset all existing top 6 selections
        Form.objects.filter(is_top_6=True).update(is_top_6=False)
        print("Reset all existing top 6 selections")
        
        # Categories and user types to process
        categories = ['achievement', 'research', 'project']
        user_types = ['STUDENT', 'FACULTY']
        
        top_6_forms = []
        
        # Process each user type and category combination
        for user_type in user_types:
            print(f"\nProcessing {user_type} selections:")
            
            for category in categories:
                # Get all forms in this category for this user type
                category_forms = list(Form.objects.filter(
                    category=category,
                    user_type=user_type
                ))
                
                if len(category_forms) < 6:
                    print(f"  Warning: Not enough {category} entries for {user_type} (found {len(category_forms)}, need 6)")
                    # Select all available if less than 6
                    selected_forms = category_forms
                else:
                    # Randomly select 6 forms
                    selected_forms = random.sample(category_forms, 6)
                
                # Add to our top 6 list
                top_6_forms.extend(selected_forms)
                
                # Mark the selected forms as top 6
                for form in selected_forms:
                    form.is_top_6 = True
                    form.save()
                    print(f"  Marked as Top 6: {form.category.capitalize()} - {form.title} (User: {form.user.name})")
        
        # Print summary
        print(f"\nTotal forms marked as Top 6: {len(top_6_forms)}")
        print(f"  - {len([f for f in top_6_forms if f.user_type == 'STUDENT'])} for STUDENT")
        print(f"  - {len([f for f in top_6_forms if f.user_type == 'FACULTY'])} for FACULTY")
    
    except Exception as e:
        print(f"Error occurred: {e}")

def list_current_top_6():
    """
    Lists all forms currently marked as top 6, grouped by user type and category.
    """
    top_forms = Form.objects.filter(is_top_6=True)
    
    if not top_forms:
        print("No forms are currently marked as Top 6")
        return
    
    print("\nCurrent Top 6 Forms:")
    print("=" * 80)
    
    # Group by user type and category for cleaner output
    grouped_forms = {}
    for form in top_forms:
        user_type = form.user_type
        category = form.category
        
        if user_type not in grouped_forms:
            grouped_forms[user_type] = {}
        
        if category not in grouped_forms[user_type]:
            grouped_forms[user_type][category] = []
        
        grouped_forms[user_type][category].append(form)
    
    # Print each user type and category
    for user_type in sorted(grouped_forms.keys()):
        print(f"\n{user_type} TOP 6:")
        print("-" * 40)
        
        for category in sorted(grouped_forms[user_type].keys()):
            forms = grouped_forms[user_type][category]
            print(f"\n  {category.upper()} ({len(forms)}):")
            
            for form in forms:
                print(f"    - {form.title} (ID: {form.id}, User: {form.user.name})")
    
    print("\n" + "=" * 80)

def count_forms_by_type():
    """
    Counts and displays the number of forms by user type and category
    """
    print("\nForm Count by User Type and Category:")
    print("=" * 80)
    
    user_types = ['STUDENT', 'FACULTY']
    categories = ['achievement', 'research', 'project']
    
    for user_type in user_types:
        print(f"\n{user_type}:")
        for category in categories:
            count = Form.objects.filter(user_type=user_type, category=category).count()
            print(f"  - {category.capitalize()}: {count}")
    
    print("\nTotal Forms: " + str(Form.objects.count()))
    print("=" * 80)

if __name__ == "__main__":
    # Show menu
    print("\nTop 6 Selection Tool")
    print("1. List current Top 6 forms")
    print("2. Select new Top 6 (6 from each category for each user type)")
    print("3. Show form counts")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        list_current_top_6()
    elif choice == "2":
        confirm = input("This will reset all current Top 6 selections. Continue? (y/n): ")
        if confirm.lower() == 'y':
            select_top_6_by_user_type()
            list_current_top_6()
    elif choice == "3":
        count_forms_by_type()
    else:
        print("Exiting...")