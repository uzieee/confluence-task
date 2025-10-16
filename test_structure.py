"""
Test script to validate code structure without requiring real Confluence credentials

This script tests the code structure and imports without making actual API calls.
"""

def test_imports():
    """Test if all required modules can be imported."""
    print("🔧 Testing imports...")
    
    try:
        import requests
        print("  ✅ requests module imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import requests: {e}")
        return False
    
    try:
        import json
        print("  ✅ json module imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import json: {e}")
        return False
    
    try:
        import os
        print("  ✅ os module imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import os: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✅ python-dotenv module imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import python-dotenv: {e}")
        return False
    
    return True


def test_confluence_client_structure():
    """Test if ConfluenceClient class can be instantiated (without credentials)."""
    print("🔧 Testing ConfluenceClient structure...")
    
    try:
        # Test import without instantiating
        from confluence_client import ConfluenceClient
        print("  ✅ ConfluenceClient class imported successfully")
        
        # Test class attributes
        if hasattr(ConfluenceClient, '__init__'):
            print("  ✅ ConfluenceClient has __init__ method")
        else:
            print("  ❌ ConfluenceClient missing __init__ method")
            return False
        
        # Test key methods exist
        required_methods = [
            'create_user', 'get_users', 'create_group', 'add_user_to_group',
            'create_space', 'set_space_permissions', 'create_page', 
            'create_blog_post', 'set_content_permissions'
        ]
        
        for method in required_methods:
            if hasattr(ConfluenceClient, method):
                print(f"  ✅ Method '{method}' exists")
            else:
                print(f"  ❌ Method '{method}' missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to test ConfluenceClient: {e}")
        return False


def test_main_structure():
    """Test if main.py structure is correct."""
    print("🔧 Testing main.py structure...")
    
    try:
        # Test import without running
        import main
        print("  ✅ main.py imported successfully")
        
        # Test ConfluenceSetup class
        if hasattr(main, 'ConfluenceSetup'):
            print("  ✅ ConfluenceSetup class exists")
        else:
            print("  ❌ ConfluenceSetup class missing")
            return False
        
        # Test key methods
        setup_methods = [
            'setup_users', 'setup_groups', 'setup_spaces', 
            'setup_content', 'run_setup'
        ]
        
        for method in setup_methods:
            if hasattr(main.ConfluenceSetup, method):
                print(f"  ✅ Method '{method}' exists in ConfluenceSetup")
            else:
                print(f"  ❌ Method '{method}' missing from ConfluenceSetup")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to test main.py: {e}")
        return False


def test_file_structure():
    """Test if all required files exist."""
    print("🔧 Testing file structure...")
    
    required_files = [
        'main.py',
        'confluence_client.py', 
        'test_setup.py',
        'example_usage.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    import os
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ File '{file}' exists")
        else:
            print(f"  ❌ File '{file}' missing")
            return False
    
    return True


def main():
    """Run all structure tests."""
    print("🧪 Running Code Structure Tests")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Import Tests", test_imports),
        ("ConfluenceClient Structure", test_confluence_client_structure),
        ("Main Structure", test_main_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔧 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Structure Test Results:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All structure tests passed!")
        print("\n💡 Next steps:")
        print("  1. Set up your Confluence Cloud account")
        print("  2. Create an API token")
        print("  3. Update the .env file with your credentials")
        print("  4. Run 'python3 main.py' to execute the setup")
        print("  5. Run 'python3 test_setup.py' to validate the setup")
    else:
        print("\n⚠️ Some structure tests failed. Please check the code.")
    
    return all_passed


if __name__ == "__main__":
    exit(0 if main() else 1)
