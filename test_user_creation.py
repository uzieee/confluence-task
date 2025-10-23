#!/usr/bin/env python3
"""
Test script to verify user creation process and API connectivity.
"""

import os
from confluence_client import ConfluenceClient

def test_user_creation():
    """Test the user creation process."""
    print("🧪 Testing User Creation Process")
    print("=" * 50)
    
    try:
        # Initialize client
        client = ConfluenceClient()
        print("✅ Confluence client initialized successfully")
        
        # Test user existence check
        test_username = "admin-user"
        print(f"\n🔍 Checking if user '{test_username}' exists...")
        
        try:
            exists = client.check_user_exists(test_username)
            if exists:
                print(f"✅ User '{test_username}' exists in the system")
            else:
                print(f"❌ User '{test_username}' not found")
                print("   Please create this user manually in the Atlassian admin console")
        except Exception as e:
            print(f"⚠️ Could not check user existence: {e}")
            print("   This might be due to API permissions or user not existing")
        
        # Test group creation
        print(f"\n🔧 Testing group creation...")
        try:
            group = client.create_group("test-group")
            print("✅ Group creation API call successful")
        except Exception as e:
            print(f"❌ Group creation failed: {e}")
        
        print("\n📋 Next Steps:")
        print("1. Create users manually in Atlassian admin console")
        print("2. Run the main setup script: python main.py")
        print("3. The script will verify users exist and continue with setup")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your .env file configuration")
        print("2. Verify your API token has proper permissions")
        print("3. Ensure your Confluence URL is correct")

if __name__ == "__main__":
    test_user_creation()
