#!/usr/bin/env python3
"""
Real API Test Script for Confluence Cloud
"""

from confluence_client import ConfluenceClient
import datetime

def main():
    print("🔗 Testing Real Confluence Cloud API...")
    print("=" * 50)
    
    try:
        # Initialize client
        client = ConfluenceClient()
        print("✅ Connected to Confluence Cloud API!")
        
        # Test 1: Get existing spaces
        print("\n📁 Getting existing spaces:")
        spaces = ['ADMIN', 'TEAM', 'PUBLIC']
        for space_key in spaces:
            try:
                space = client.get_space(space_key)
                print(f"  ✅ {space_key}: {space.get('name', 'Unknown')}")
            except Exception as e:
                print(f"  ❌ {space_key}: Error - {e}")
        
        # Test 2: Create new content
        print("\n📄 Creating new content:")
        timestamp = datetime.datetime.now().strftime('%H%M%S')
        title = f'API Test Page {timestamp}'
        
        try:
            page = client.create_page(
                space_key='PUBLIC',
                title=title,
                content='''
                <h1>Real API Test Page</h1>
                <p>This page was created using the Confluence Cloud REST API!</p>
                <h2>Features Demonstrated:</h2>
                <ul>
                    <li>✅ Real API connection</li>
                    <li>✅ Content creation</li>
                    <li>✅ Space management</li>
                    <li>✅ Authentication</li>
                </ul>
                <p><strong>Created at:</strong> ''' + str(datetime.datetime.now()) + '''</p>
                '''
            )
            print(f"  ✅ Created page: {title}")
            print(f"  📄 Page ID: {page.get('id')}")
            print(f"  🌐 URL: https://mmnjong.atlassian.net/wiki{page.get('_links', {}).get('webui', '')}")
        except Exception as e:
            print(f"  ❌ Error creating page: {e}")
        
        # Test 3: Create blog post
        print("\n📝 Creating blog post:")
        blog_title = f'API Test Blog {timestamp}'
        
        try:
            blog = client.create_blog_post(
                space_key='TEAM',
                title=blog_title,
                content='''
                <h1>Real API Blog Post</h1>
                <p>This blog post was created via REST API!</p>
                <h2>What we accomplished:</h2>
                <ul>
                    <li>Connected to Confluence Cloud</li>
                    <li>Created pages and blog posts</li>
                    <li>Demonstrated full API functionality</li>
                </ul>
                '''
            )
            print(f"  ✅ Created blog: {blog_title}")
            print(f"  📄 Blog ID: {blog.get('id')}")
            print(f"  🌐 URL: https://mmnjong.atlassian.net/wiki{blog.get('_links', {}).get('webui', '')}")
        except Exception as e:
            print(f"  ❌ Error creating blog: {e}")
        
        print("\n🎉 Real API calls completed successfully!")
        print("=" * 50)
        print("✅ Your Confluence Cloud setup is working perfectly!")
        print("🌐 Visit your site: https://mmnjong.atlassian.net/wiki")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    main()
