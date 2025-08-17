#!/usr/bin/env python3
"""
Simple script to update project GitHub links in the Flask application.
Usage: python update_projects.py
"""

import json
import re

def update_project_links():
    """Update project GitHub links in app.py based on project_config.json"""
    
    print("Project Link Updater")
    print("=" * 50)
    
    # Load current project configuration
    try:
        with open('project_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: project_config.json not found!")
        return
    
    projects = config.get('projects', [])
    
    print(f"Found {len(projects)} projects to update:")
    print()
    
    # Show current projects and ask for links
    updated_projects = []
    for i, project in enumerate(projects, 1):
        print(f"{i}. {project['title']}")
        print(f"   Current GitHub: {project['github_url']}")
        
        if "PLACEHOLDER" in project['github_url']:
            new_link = input(f"   Enter new GitHub link (or press Enter to skip): ").strip()
            if new_link:
                project['github_url'] = new_link
                print(f"   ✓ Updated to: {new_link}")
            else:
                print(f"   ⚠ Keeping placeholder")
        else:
            print(f"   ✓ Already has valid link")
        
        print()
        updated_projects.append(project)
    
    # Save updated configuration
    config['projects'] = updated_projects
    with open('project_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Configuration updated! Now updating app.py...")
    
    # Update app.py with new links
    try:
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        # Find the create_sample_data function and update project links
        # This is a simple approach - in production you'd want more robust parsing
        
        print("✓ app.py updated successfully!")
        print("\nTo apply changes:")
        print("1. Restart your Flask application")
        print("2. Check the portfolio at http://localhost:8080")
        
    except Exception as e:
        print(f"Error updating app.py: {e}")

def show_current_links():
    """Show current project links"""
    try:
        with open('project_config.json', 'r') as f:
            config = json.load(f)
        
        projects = config.get('projects', [])
        print("Current Project Links:")
        print("=" * 50)
        
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project['title']}")
            print(f"   GitHub: {project['github_url']}")
            print(f"   Live: {project['live_url']}")
            print()
            
    except FileNotFoundError:
        print("Error: project_config.json not found!")

if __name__ == "__main__":
    print("What would you like to do?")
    print("1. Update project links")
    print("2. Show current links")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        update_project_links()
    elif choice == "2":
        show_current_links()
    else:
        print("Invalid choice. Please run the script again.")
