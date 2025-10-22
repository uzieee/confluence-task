"""
Mock test script to demonstrate the Confluence setup functionality
without requiring real Confluence Cloud access.
"""

import os
import time
from typing import Dict, List, Any


class MockConfluenceClient:
    """Mock Confluence client for testing purposes."""
    
    def __init__(self):
        self.users = {}
        self.groups = {}
        self.spaces = {}
        self.content = {}
        self.user_counter = 0
        self.content_counter = 0
    
    def create_user(self, username: str, email: str, display_name: str, is_admin: bool = False) -> Dict[str, Any]:
        """Mock user creation."""
        self.user_counter += 1
        user = {
            'id': f'user-{self.user_counter}',
            'username': username,
            'email': email,
            'displayName': display_name,
            'isAdmin': is_admin
        }
        self.users[username] = user
        print(f"  ✅ Mock user '{username}' created successfully")
        return user
    
    def get_users(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Mock get users."""
        return list(self.users.values())[:limit]
    
    def create_group(self, group_name: str) -> Dict[str, Any]:
        """Mock group creation."""
        group = {
            'id': f'group-{group_name}',
            'name': group_name
        }
        self.groups[group_name] = group
        print(f"  ✅ Mock group '{group_name}' created successfully")
        return group
    
    def add_user_to_group(self, group_name: str, username: str) -> Dict[str, Any]:
        """Mock add user to group."""
        if group_name not in self.groups:
            self.groups[group_name] = {'name': group_name, 'members': []}
        if 'members' not in self.groups[group_name]:
            self.groups[group_name]['members'] = []
        self.groups[group_name]['members'].append(username)
        print(f"  ✅ Mock user '{username}' added to group '{group_name}'")
        return {'success': True}
    
    def create_space(self, space_key: str, name: str, description: str = "") -> Dict[str, Any]:
        """Mock space creation."""
        space = {
            'id': f'space-{space_key}',
            'key': space_key,
            'name': name,
            'description': {'value': description, 'representation': 'storage'}
        }
        self.spaces[space_key] = space
        print(f"  ✅ Mock space '{space_key}' created successfully")
        return space
    
    def set_space_permissions(self, space_key: str, permissions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mock set space permissions."""
        if space_key in self.spaces:
            self.spaces[space_key]['permissions'] = permissions
            print(f"  ✅ Mock permissions set for space '{space_key}'")
        return {'success': True}
    
    def create_page(self, space_key: str, title: str, content: str, parent_id: str = None) -> Dict[str, Any]:
        """Mock page creation."""
        self.content_counter += 1
        page = {
            'id': f'content-{self.content_counter}',
            'type': 'page',
            'title': title,
            'space': {'key': space_key},
            'body': {'storage': {'value': content, 'representation': 'storage'}}
        }
        self.content[title] = page
        print(f"  ✅ Mock page '{title}' created successfully")
        return page
    
    def create_blog_post(self, space_key: str, title: str, content: str) -> Dict[str, Any]:
        """Mock blog post creation."""
        self.content_counter += 1
        blog_post = {
            'id': f'content-{self.content_counter}',
            'type': 'blogpost',
            'title': title,
            'space': {'key': space_key},
            'body': {'storage': {'value': content, 'representation': 'storage'}}
        }
        self.content[title] = blog_post
        print(f"  ✅ Mock blog post '{title}' created successfully")
        return blog_post
    
    def set_content_permissions(self, content_id: str, permissions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mock set content permissions."""
        print(f"  ✅ Mock permissions set for content '{content_id}'")
        return {'success': True}
    
    def get_space(self, space_key: str) -> Dict[str, Any]:
        """Mock get space."""
        return self.spaces.get(space_key, {})
    
    def get_content(self, content_id: str) -> Dict[str, Any]:
        """Mock get content."""
        for content in self.content.values():
            if content['id'] == content_id:
                return content
        return {}


class MockConfluenceSetup:
    """Mock Confluence setup for testing."""
    
    def __init__(self):
        self.client = MockConfluenceClient()
        self.users = {}
        self.group_name = "standard-users"
        self.spaces = {}
        self.content = {}
    
    def setup_users(self) -> None:
        """Create mock users."""
        print("🔧 Setting up users...")
        
        user_configs = [
            {'username': 'admin-user', 'email': 'admin@example.com', 'display_name': 'Administrator User', 'is_admin': True},
            {'username': 'user-1', 'email': 'user1@example.com', 'display_name': 'Standard User 1', 'is_admin': False},
            {'username': 'user-2', 'email': 'user2@example.com', 'display_name': 'Standard User 2', 'is_admin': False},
            {'username': 'user-3', 'email': 'user3@example.com', 'display_name': 'Standard User 3', 'is_admin': False},
            {'username': 'user-4', 'email': 'user4@example.com', 'display_name': 'Standard User 4', 'is_admin': False}
        ]
        
        for config in user_configs:
            user = self.client.create_user(**config)
            self.users[config['username']] = user
            time.sleep(0.1)  # Simulate API delay
        
        print(f"✅ User setup completed. Created {len(self.users)} users.")
    
    def setup_groups(self) -> None:
        """Create mock groups."""
        print("🔧 Setting up groups...")
        
        group = self.client.create_group(self.group_name)
        standard_users = [username for username in self.users.keys() if username != 'admin-user']
        
        for username in standard_users:
            self.client.add_user_to_group(self.group_name, username)
            time.sleep(0.1)
        
        print(f"✅ Group setup completed. Added {len(standard_users)} users to group.")
    
    def setup_spaces(self) -> None:
        """Create mock spaces."""
        print("🔧 Setting up spaces...")
        
        space_configs = [
            {'key': 'ADMIN', 'name': 'Administrator Space', 'description': 'Space restricted to administrators only'},
            {'key': 'RESTRICTED', 'name': 'Restricted Workspace', 'description': 'Highly restricted workspace for sensitive information'},
            {'key': 'COLLAB', 'name': 'Collaborative Workspace', 'description': 'Open collaborative workspace for team projects'},
            {'key': 'TEAM', 'name': 'Team Space', 'description': 'Space for team collaboration'},
            {'key': 'PUBLIC', 'name': 'Public Space', 'description': 'Public space with read access for all users'}
        ]
        
        for config in space_configs:
            space = self.client.create_space(
                space_key=config['key'],
                name=config['name'],
                description=config['description']
            )
            self.spaces[config['key']] = space
            time.sleep(0.1)
        
        print(f"✅ Space setup completed. Created {len(self.spaces)} spaces.")
    
    def setup_content(self) -> None:
        """Create mock content."""
        print("🔧 Setting up content...")
        
        page_configs = [
            {'space_key': 'ADMIN', 'title': 'Admin Documentation', 'content': '<h1>Administrator Documentation</h1>'},
            {'space_key': 'TEAM', 'title': 'Team Guidelines', 'content': '<h1>Team Guidelines</h1>'},
            {'space_key': 'PUBLIC', 'title': 'Welcome to Our Confluence Site', 'content': '<h1>Welcome to Our Confluence Site</h1>'}
        ]
        
        for config in page_configs:
            page = self.client.create_page(**config)
            self.content[config['title']] = page
            time.sleep(0.1)
        
        blog_configs = [
            {'space_key': 'TEAM', 'title': 'Team Update - Project Status', 'content': '<h1>Project Status Update</h1>'},
            {'space_key': 'PUBLIC', 'title': 'Company News - Q1 Updates', 'content': '<h1>Q1 Company Updates</h1>'}
        ]
        
        for config in blog_configs:
            blog_post = self.client.create_blog_post(**config)
            self.content[config['title']] = blog_post
            time.sleep(0.1)
        
        print(f"✅ Content setup completed. Created {len(self.content)} content items.")
    
    def run_setup(self) -> None:
        """Run the complete mock setup."""
        print("🚀 Starting Mock Confluence Setup (No Real API Calls)")
        print("=" * 60)
        
        self.setup_users()
        print()
        
        self.setup_groups()
        print()
        
        self.setup_spaces()
        print()
        
        self.setup_content()
        print()
        
        print("🎉 Mock setup completed successfully!")
        print("=" * 60)
        print(f"✅ Created {len(self.users)} users")
        print(f"✅ Created 1 group: {self.group_name}")
        print(f"✅ Created {len(self.spaces)} spaces")
        print(f"✅ Created {len(self.content)} content items")
        print()
        print("📋 Summary:")
        print(f"  - Users: {list(self.users.keys())}")
        print(f"  - Group: {self.group_name}")
        print(f"  - Spaces: {list(self.spaces.keys())}")
        print(f"  - Content: {list(self.content.keys())}")


def main():
    """Run the mock setup."""
    print("🧪 Running Mock Confluence Setup")
    print("This demonstrates the functionality without real API calls")
    print("=" * 60)
    
    setup = MockConfluenceSetup()
    setup.run_setup()
    
    print("\n💡 This was a mock demonstration.")
    print("To run with real Confluence Cloud:")
    print("1. Ensure your Atlassian site has Confluence enabled")
    print("2. Grant your user Confluence permissions")
    print("3. Run 'python3 main.py' for real setup")


if __name__ == "__main__":
    main()
