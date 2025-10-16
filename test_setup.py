"""
Test script to validate Confluence Cloud setup

This script provides basic validation of the Confluence setup
by checking if resources were created successfully.
"""

import os
from confluence_client import ConfluenceClient


def test_confluence_connection():
    """Test basic connection to Confluence API."""
    try:
        client = ConfluenceClient()
        # Try to get users to test connection
        users = client.get_users(limit=10)
        print(f"✅ Connection successful. Found {len(users)} users.")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def test_users_exist():
    """Test if required users were created."""
    expected_users = ['admin-user', 'user-1', 'user-2', 'user-3', 'user-4']
    
    try:
        client = ConfluenceClient()
        users = client.get_users(limit=50)
        usernames = [user.get('username') for user in users if 'username' in user]
        
        print("🔍 Checking for required users...")
        for username in expected_users:
            if username in usernames:
                print(f"  ✅ User '{username}' exists")
            else:
                print(f"  ❌ User '{username}' not found")
        
        return all(username in usernames for username in expected_users)
    except Exception as e:
        print(f"❌ Failed to check users: {e}")
        return False


def test_spaces_exist():
    """Test if required spaces were created."""
    expected_spaces = ['ADMIN', 'TEAM', 'PUBLIC']
    
    print("🔍 Checking for required spaces...")
    try:
        client = ConfluenceClient()
        for space_key in expected_spaces:
            try:
                space = client.get_space(space_key)
                print(f"  ✅ Space '{space_key}' exists: {space.get('name', 'Unknown')}")
            except Exception as e:
                print(f"  ❌ Space '{space_key}' not found: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to check spaces: {e}")
        return False


def main():
    """Run all validation tests."""
    print("🧪 Running Confluence Setup Validation Tests")
    print("=" * 50)
    
    # Check if environment is configured
    if not all([os.getenv('CONFLUENCE_URL'), os.getenv('CONFLUENCE_EMAIL'), os.getenv('CONFLUENCE_API_TOKEN')]):
        print("❌ Environment variables not configured.")
        print("Please set up your .env file with Confluence credentials.")
        return False
    
    tests = [
        ("Connection Test", test_confluence_connection),
        ("Users Test", test_users_exist),
        ("Spaces Test", test_spaces_exist)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔧 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Setup validation successful.")
    else:
        print("\n⚠️ Some tests failed. Please check the setup.")
    
    return all_passed


if __name__ == "__main__":
    exit(0 if main() else 1)
