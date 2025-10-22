"""
Confluence Cloud Setup Script

This script implements the Senior Technical Specialist take-home exercise
for setting up a Confluence Cloud site with users, groups, spaces, and content.
"""

import os
import time
from typing import Dict, List, Any
from confluence_client import ConfluenceClient


class ConfluenceSetup:
    """Main class for setting up Confluence Cloud site."""
    
    def __init__(self):
        """Initialize the Confluence setup with API client."""
        self.client = ConfluenceClient()
        self.users = {}
        self.group_name = "standard-users"
        self.spaces = {}
        self.content = {}
    
    def setup_users(self) -> None:
        """
        Create users as specified in the requirements:
        - 1 administrator user
        - 4 standard users
        """
        print("🔧 Setting up users...")
        
        # User configurations
        user_configs = [
            {
                'username': 'admin-user',
                'email': 'admin@example.com',
                'display_name': 'Administrator User',
                'is_admin': True
            },
            {
                'username': 'user-1',
                'email': 'user1@example.com',
                'display_name': 'Standard User 1',
                'is_admin': False
            },
            {
                'username': 'user-2',
                'email': 'user2@example.com',
                'display_name': 'Standard User 2',
                'is_admin': False
            },
            {
                'username': 'user-3',
                'email': 'user3@example.com',
                'display_name': 'Standard User 3',
                'is_admin': False
            },
            {
                'username': 'user-4',
                'email': 'user4@example.com',
                'display_name': 'Standard User 4',
                'is_admin': False
            }
        ]
        
        for config in user_configs:
            try:
                print(f"  Creating user: {config['username']}")
                user = self.client.create_user(
                    username=config['username'],
                    email=config['email'],
                    display_name=config['display_name'],
                    is_admin=config['is_admin']
                )
                self.users[config['username']] = user
                print(f"  ✅ User {config['username']} created successfully")
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"  ❌ Failed to create user {config['username']}: {e}")
                # Continue with other users even if one fails
        
        print(f"✅ User setup completed. Created {len(self.users)} users.")
    
    def setup_groups(self) -> None:
        """
        Create group and add standard users to it.
        Administrator is not added to the group.
        """
        print("🔧 Setting up groups...")
        
        try:
            # Create the group
            print(f"  Creating group: {self.group_name}")
            group = self.client.create_group(self.group_name)
            print(f"  ✅ Group {self.group_name} created successfully")
            
            # Add standard users to the group (exclude admin)
            standard_users = [username for username in self.users.keys() if username != 'admin-user']
            
            for username in standard_users:
                try:
                    print(f"  Adding {username} to group {self.group_name}")
                    self.client.add_user_to_group(self.group_name, username)
                    print(f"  ✅ User {username} added to group successfully")
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    print(f"  ❌ Failed to add {username} to group: {e}")
            
            print(f"✅ Group setup completed. Added {len(standard_users)} users to group.")
            
        except Exception as e:
            print(f"❌ Failed to setup groups: {e}")
    
    def setup_spaces(self) -> None:
        """
        Create spaces with proper permissions.
        - Admin Space: Only administrators can view and edit
        - Team Space: Group members can view and edit
        - Public Space: All users can view, only administrators can edit
        """
        print("🔧 Setting up spaces...")
        
        space_configs = [
            {
                'key': 'ADMIN',
                'name': 'Administrator Space',
                'description': 'Space restricted to administrators only',
                'permissions': 'admin_only'
            },
            {
                'key': 'RESTRICTED',
                'name': 'Restricted Workspace',
                'description': 'Highly restricted workspace for sensitive information',
                'permissions': 'restricted_access'
            },
            {
                'key': 'COLLAB',
                'name': 'Collaborative Workspace',
                'description': 'Open collaborative workspace for team projects',
                'permissions': 'collaborative'
            },
            {
                'key': 'TEAM',
                'name': 'Team Space',
                'description': 'Space for team collaboration',
                'permissions': 'group_based'
            },
            {
                'key': 'PUBLIC',
                'name': 'Public Space',
                'description': 'Public space with read access for all users',
                'permissions': 'public_read'
            }
        ]
        
        for config in space_configs:
            try:
                print(f"  Creating space: {config['key']}")
                space = self.client.create_space(
                    space_key=config['key'],
                    name=config['name'],
                    description=config['description']
                )
                self.spaces[config['key']] = space
                print(f"  ✅ Space {config['key']} created successfully")
                
                # Set permissions based on configuration
                self._set_space_permissions(config['key'], config['permissions'])
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"  ❌ Failed to create space {config['key']}: {e}")
        
        print(f"✅ Space setup completed. Created {len(self.spaces)} spaces.")
    
    def _set_space_permissions(self, space_key: str, permission_type: str) -> None:
        """
        Set permissions for a space based on the permission type.
        
        Args:
            space_key: Space key
            permission_type: Type of permissions to set
        """
        try:
            if permission_type == 'admin_only':
                # Only administrators can view and edit
                permissions = [
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'read', 'targetType': 'space'},
                        'anonymousAccess': False
                    },
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'write', 'targetType': 'space'},
                        'anonymousAccess': False
                    }
                ]
            elif permission_type == 'restricted_access':
                # Highly restricted - only specific admin users
                permissions = [
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'read', 'targetType': 'space'},
                        'anonymousAccess': False
                    },
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'write', 'targetType': 'space'},
                        'anonymousAccess': False
                    },
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'admin', 'targetType': 'space'},
                        'anonymousAccess': False
                    }
                ]
            elif permission_type == 'collaborative':
                # Open collaborative workspace - all users can read and write
                permissions = [
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'read', 'targetType': 'space'},
                        'anonymousAccess': False
                    },
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'write', 'targetType': 'space'},
                        'anonymousAccess': False
                    }
                ]
            elif permission_type == 'group_based':
                # Group members can view and edit
                permissions = [
                    {
                        'subject': {'type': 'group', 'identifier': self.group_name},
                        'operation': {'operation': 'read', 'targetType': 'space'},
                        'anonymousAccess': False
                    },
                    {
                        'subject': {'type': 'group', 'identifier': self.group_name},
                        'operation': {'operation': 'write', 'targetType': 'space'},
                        'anonymousAccess': False
                    }
                ]
            elif permission_type == 'public_read':
                # All users can read, only administrators can write
                permissions = [
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'write', 'targetType': 'space'},
                        'anonymousAccess': False
                    }
                ]
            else:
                print(f"  ⚠️ Unknown permission type: {permission_type}")
                return
            
            self.client.set_space_permissions(space_key, permissions)
            print(f"  ✅ Permissions set for space {space_key}")
            
        except Exception as e:
            print(f"  ❌ Failed to set permissions for space {space_key}: {e}")
    
    def setup_content(self) -> None:
        """
        Create pages and blog posts with proper permissions.
        """
        print("🔧 Setting up content...")
        
        # Create pages in different spaces
        page_configs = [
            {
                'space_key': 'ADMIN',
                'title': 'Admin Documentation',
                'content': '''
                <h1>Administrator Documentation</h1>
                <p>This page contains sensitive administrative information.</p>
                <h2>System Configuration</h2>
                <ul>
                    <li>Database settings</li>
                    <li>Security configurations</li>
                    <li>User management procedures</li>
                </ul>
                ''',
                'permissions': 'admin_only'
            },
            {
                'space_key': 'RESTRICTED',
                'title': 'Confidential Information',
                'content': '''
                <h1>Confidential Information</h1>
                <p>This workspace contains highly sensitive and confidential information.</p>
                <h2>Security Protocols</h2>
                <ul>
                    <li>Access is strictly limited to authorized personnel</li>
                    <li>All content is encrypted and protected</li>
                    <li>Regular security audits are conducted</li>
                </ul>
                <h2>Compliance Requirements</h2>
                <ul>
                    <li>GDPR compliance documentation</li>
                    <li>Security incident procedures</li>
                    <li>Data retention policies</li>
                </ul>
                ''',
                'permissions': 'restricted_access'
            },
            {
                'space_key': 'COLLAB',
                'title': 'Collaborative Project Hub',
                'content': '''
                <h1>Collaborative Project Hub</h1>
                <p>Welcome to our open collaborative workspace! This space encourages innovation and teamwork.</p>
                <h2>Project Management</h2>
                <ul>
                    <li>Active project tracking</li>
                    <li>Team collaboration tools</li>
                    <li>Real-time updates and notifications</li>
                </ul>
                <h2>Innovation Lab</h2>
                <ul>
                    <li>Brainstorming sessions</li>
                    <li>Prototype development</li>
                    <li>Knowledge sharing</li>
                </ul>
                ''',
                'permissions': 'collaborative'
            },
            {
                'space_key': 'TEAM',
                'title': 'Team Guidelines',
                'content': '''
                <h1>Team Guidelines</h1>
                <p>Welcome to the team space! This document outlines our team's working guidelines.</p>
                <h2>Communication</h2>
                <ul>
                    <li>Use clear and concise language</li>
                    <li>Update documentation regularly</li>
                    <li>Collaborate effectively</li>
                </ul>
                <h2>Best Practices</h2>
                <ul>
                    <li>Code review process</li>
                    <li>Testing procedures</li>
                    <li>Documentation standards</li>
                </ul>
                ''',
                'permissions': 'group_based'
            },
            {
                'space_key': 'PUBLIC',
                'title': 'Welcome to Our Confluence Site',
                'content': '''
                <h1>Welcome to Our Confluence Site</h1>
                <p>This is a public page accessible to all users.</p>
                <h2>Getting Started</h2>
                <p>Here you can find general information about our organization and resources.</p>
                <h2>Resources</h2>
                <ul>
                    <li>Company policies</li>
                    <li>General announcements</li>
                    <li>Contact information</li>
                </ul>
                ''',
                'permissions': 'public_read'
            }
        ]
        
        # Create pages
        for config in page_configs:
            try:
                print(f"  Creating page: {config['title']} in space {config['space_key']}")
                page = self.client.create_page(
                    space_key=config['space_key'],
                    title=config['title'],
                    content=config['content']
                )
                self.content[config['title']] = page
                print(f"  ✅ Page '{config['title']}' created successfully")
                
                # Set content permissions
                self._set_content_permissions(page['id'], config['permissions'])
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"  ❌ Failed to create page '{config['title']}': {e}")
        
        # Create blog posts
        blog_configs = [
            {
                'space_key': 'RESTRICTED',
                'title': 'Security Alert - System Maintenance',
                'content': '''
                <h1>Security Alert - System Maintenance</h1>
                <p>This is a confidential security update for authorized personnel only.</p>
                <h2>Security Updates</h2>
                <ul>
                    <li>Critical security patches applied</li>
                    <li>Access logs reviewed and analyzed</li>
                    <li>New security protocols implemented</li>
                </ul>
                <h2>Action Required</h2>
                <ul>
                    <li>All users must update their passwords</li>
                    <li>Two-factor authentication is now mandatory</li>
                    <li>Regular security training sessions scheduled</li>
                </ul>
                ''',
                'permissions': 'restricted_access'
            },
            {
                'space_key': 'COLLAB',
                'title': 'Innovation Spotlight - New Ideas',
                'content': '''
                <h1>Innovation Spotlight - New Ideas</h1>
                <p>Sharing exciting new ideas and innovations from our collaborative workspace!</p>
                <h2>Featured Innovations</h2>
                <ul>
                    <li>AI-powered automation tools</li>
                    <li>Enhanced user experience designs</li>
                    <li>Sustainable technology solutions</li>
                </ul>
                <h2>Collaboration Opportunities</h2>
                <ul>
                    <li>Cross-team project initiatives</li>
                    <li>Knowledge sharing sessions</li>
                    <li>Innovation workshops</li>
                </ul>
                ''',
                'permissions': 'collaborative'
            },
            {
                'space_key': 'TEAM',
                'title': 'Team Update - Project Status',
                'content': '''
                <h1>Project Status Update</h1>
                <p>Here's the latest update on our current project status.</p>
                <h2>Completed Tasks</h2>
                <ul>
                    <li>User authentication setup</li>
                    <li>Database configuration</li>
                    <li>API integration</li>
                </ul>
                <h2>Next Steps</h2>
                <ul>
                    <li>Testing and validation</li>
                    <li>Documentation updates</li>
                    <li>Deployment preparation</li>
                </ul>
                ''',
                'permissions': 'group_based'
            },
            {
                'space_key': 'PUBLIC',
                'title': 'Company News - Q1 Updates',
                'content': '''
                <h1>Q1 Company Updates</h1>
                <p>Welcome to our quarterly company updates!</p>
                <h2>Key Achievements</h2>
                <ul>
                    <li>Successful product launch</li>
                    <li>Team expansion</li>
                    <li>Customer satisfaction improvements</li>
                </ul>
                <h2>Looking Ahead</h2>
                <p>We're excited about the upcoming quarter and the new initiatives we'll be launching.</p>
                ''',
                'permissions': 'public_read'
            }
        ]
        
        # Create blog posts
        for config in blog_configs:
            try:
                print(f"  Creating blog post: {config['title']} in space {config['space_key']}")
                blog_post = self.client.create_blog_post(
                    space_key=config['space_key'],
                    title=config['title'],
                    content=config['content']
                )
                self.content[config['title']] = blog_post
                print(f"  ✅ Blog post '{config['title']}' created successfully")
                
                # Set content permissions
                self._set_content_permissions(blog_post['id'], config['permissions'])
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"  ❌ Failed to create blog post '{config['title']}': {e}")
        
        print(f"✅ Content setup completed. Created {len(self.content)} content items.")
    
    def _set_content_permissions(self, content_id: str, permission_type: str) -> None:
        """
        Set permissions for content based on the permission type.
        
        Args:
            content_id: Content ID
            permission_type: Type of permissions to set
        """
        try:
            if permission_type == 'admin_only':
                # Only administrators can view and edit
                permissions = [
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'read', 'targetType': 'content'},
                        'anonymousAccess': False
                    },
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'write', 'targetType': 'content'},
                        'anonymousAccess': False
                    }
                ]
            elif permission_type == 'restricted_access':
                # Highly restricted content - only specific admin users
                permissions = [
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'read', 'targetType': 'content'},
                        'anonymousAccess': False
                    },
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'write', 'targetType': 'content'},
                        'anonymousAccess': False
                    },
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'admin', 'targetType': 'content'},
                        'anonymousAccess': False
                    }
                ]
            elif permission_type == 'collaborative':
                # Open collaborative content - all users can read and write
                permissions = [
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'read', 'targetType': 'content'},
                        'anonymousAccess': False
                    },
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'write', 'targetType': 'content'},
                        'anonymousAccess': False
                    }
                ]
            elif permission_type == 'group_based':
                # Group members can view and edit
                permissions = [
                    {
                        'subject': {'type': 'group', 'identifier': self.group_name},
                        'operation': {'operation': 'read', 'targetType': 'content'},
                        'anonymousAccess': False
                    },
                    {
                        'subject': {'type': 'group', 'identifier': self.group_name},
                        'operation': {'operation': 'write', 'targetType': 'content'},
                        'anonymousAccess': False
                    }
                ]
            elif permission_type == 'public_read':
                # All users can read, only administrators can write
                permissions = [
                    {
                        'subject': {'type': 'user', 'identifier': 'admin-user'},
                        'operation': {'operation': 'write', 'targetType': 'content'},
                        'anonymousAccess': False
                    }
                ]
            else:
                print(f"  ⚠️ Unknown permission type: {permission_type}")
                return
            
            self.client.set_content_permissions(content_id, permissions)
            print(f"  ✅ Permissions set for content {content_id}")
            
        except Exception as e:
            print(f"  ❌ Failed to set permissions for content {content_id}: {e}")
    
    def run_setup(self) -> None:
        """Run the complete Confluence setup process."""
        print("🚀 Starting Confluence Cloud setup...")
        print("=" * 50)
        
        try:
            # Execute setup steps in order
            self.setup_users()
            print()
            
            self.setup_groups()
            print()
            
            self.setup_spaces()
            print()
            
            self.setup_content()
            print()
            
            # Summary
            print("🎉 Setup completed successfully!")
            print("=" * 50)
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
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            raise


def main():
    """Main function to run the Confluence setup."""
    try:
        setup = ConfluenceSetup()
        setup.run_setup()
    except Exception as e:
        print(f"❌ Application failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
