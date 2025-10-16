"""
Example usage of the Confluence Client

This script demonstrates how to use the ConfluenceClient class
for various operations beyond the main setup.
"""

import os
from confluence_client import ConfluenceClient


def example_user_operations():
    """Example of user-related operations."""
    print("👥 User Operations Example")
    print("-" * 30)
    
    client = ConfluenceClient()
    
    # Get all users
    users = client.get_users(limit=10)
    print(f"Found {len(users)} users:")
    for user in users[:5]:  # Show first 5 users
        print(f"  - {user.get('displayName', 'Unknown')} ({user.get('username', 'No username')})")


def example_space_operations():
    """Example of space-related operations."""
    print("\n🏢 Space Operations Example")
    print("-" * 30)
    
    client = ConfluenceClient()
    
    # Get information about the created spaces
    spaces = ['ADMIN', 'TEAM', 'PUBLIC']
    for space_key in spaces:
        try:
            space = client.get_space(space_key)
            print(f"Space '{space_key}': {space.get('name', 'Unknown')}")
            print(f"  Description: {space.get('description', {}).get('value', 'No description')}")
        except Exception as e:
            print(f"Space '{space_key}': Not found ({e})")


def example_content_operations():
    """Example of content-related operations."""
    print("\n📄 Content Operations Example")
    print("-" * 30)
    
    client = ConfluenceClient()
    
    # Example: Create a simple page
    try:
        page = client.create_page(
            space_key='PUBLIC',
            title='Example Page from Script',
            content='''
            <h1>Example Page</h1>
            <p>This page was created using the ConfluenceClient API.</p>
            <h2>Features</h2>
            <ul>
                <li>Easy to use Python API</li>
                <li>Comprehensive error handling</li>
                <li>Flexible permission management</li>
            </ul>
            '''
        )
        print(f"✅ Created example page: {page.get('title')}")
        print(f"   Page ID: {page.get('id')}")
        print(f"   URL: {page.get('_links', {}).get('webui', 'N/A')}")
    except Exception as e:
        print(f"❌ Failed to create example page: {e}")


def example_permission_operations():
    """Example of permission-related operations."""
    print("\n🔐 Permission Operations Example")
    print("-" * 30)
    
    print("Permission types implemented:")
    print("  - admin_only: Only administrators can access")
    print("  - group_based: Group members can access")
    print("  - public_read: All users can read, admins can write")
    
    print("\nSpaces and their permission models:")
    print("  - ADMIN space: admin_only")
    print("  - TEAM space: group_based")
    print("  - PUBLIC space: public_read")


def main():
    """Run all examples."""
    print("📚 Confluence Client Usage Examples")
    print("=" * 50)
    
    # Check environment
    if not all([os.getenv('CONFLUENCE_URL'), os.getenv('CONFLUENCE_EMAIL'), os.getenv('CONFLUENCE_API_TOKEN')]):
        print("❌ Please configure your .env file with Confluence credentials first.")
        return
    
    try:
        example_user_operations()
        example_space_operations()
        example_content_operations()
        example_permission_operations()
        
        print("\n🎉 Examples completed successfully!")
        print("\n💡 Tips:")
        print("  - Use the test_setup.py script to validate your setup")
        print("  - Check the README.md for detailed documentation")
        print("  - Modify the main.py script to customize your setup")
        
    except Exception as e:
        print(f"❌ Example execution failed: {e}")


if __name__ == "__main__":
    main()
