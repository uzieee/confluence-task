# User Creation Guide for Confluence Cloud Setup

## ⚠️ Important: Manual User Creation Required

Confluence Cloud **does not support** direct user creation via REST API. Users must be created manually through the Atlassian admin console.

## 📋 Step-by-Step Instructions

### 1. Access Admin Console
- Go to your Confluence Cloud site
- Navigate to the admin console: `https://your-site.atlassian.net/admin`
- Or click on your profile → "Administration"

### 2. Navigate to User Management
- In the admin console, go to **"User management"**
- Click on **"Users"** in the left sidebar

### 3. Create Users
Click **"Invite users"** or **"Add users"** and create the following users:

#### User 1: Administrator
- **Username**: `admin-user`
- **Email**: `admin@example.com`
- **Display Name**: `Administrator User`
- **Admin privileges**: ✅ **Yes** (make this user a site administrator)

#### User 2: Standard User 1
- **Username**: `user-1`
- **Email**: `user1@example.com`
- **Display Name**: `Standard User 1`
- **Admin privileges**: ❌ **No**

#### User 3: Standard User 2
- **Username**: `user-2`
- **Email**: `user2@example.com`
- **Display Name**: `Standard User 2`
- **Admin privileges**: ❌ **No**

#### User 4: Standard User 3
- **Username**: `user-3`
- **Email**: `user3@example.com`
- **Display Name**: `Standard User 3`
- **Admin privileges**: ❌ **No**

#### User 5: Standard User 4
- **Username**: `user-4`
- **Email**: `user4@example.com`
- **Display Name**: `Standard User 4`
- **Admin privileges**: ❌ **No**

### 4. Verify User Creation
- Ensure all 5 users are created and active
- Verify that `admin-user` has administrator privileges
- Check that the other 4 users are standard users

### 5. Continue with Setup
Once all users are created, run the setup script:
```bash
python3 main.py
```

The script will:
- Verify that users exist
- Create groups and add users to groups
- Create spaces with proper permissions
- Create content with appropriate access controls

## 🔧 Alternative: Use Existing Users

If you prefer to use existing users instead of creating new ones:

1. **Identify existing users** in your Confluence site
2. **Update the user configurations** in `main.py` to match existing usernames
3. **Ensure one user has admin privileges** for the setup to work properly
4. **Run the setup script** with the updated configurations

## 📝 Notes

- **Admin User**: Must have site administrator privileges to create spaces and set permissions
- **Standard Users**: Will be added to the `standard-users` group for team-based permissions
- **Email Addresses**: Use real email addresses if you want to send invitations
- **Usernames**: Must be unique and follow Atlassian username conventions

## 🚨 Troubleshooting

### If user creation fails:
1. **Check permissions**: Ensure you have admin access to the Confluence site
2. **Verify email addresses**: Use valid email addresses for invitations
3. **Check username format**: Usernames should be lowercase, no spaces
4. **Review site limits**: Check if you've reached user limits for your plan

### If setup script fails:
1. **Verify users exist**: Check that all users are created and active
2. **Check admin privileges**: Ensure the admin user has proper permissions
3. **Review API credentials**: Verify your API token has sufficient permissions
4. **Check network connectivity**: Ensure the script can reach the Confluence API

## 📞 Support

If you encounter issues:
1. Check the [Atlassian documentation](https://confluence.atlassian.com/)
2. Review the setup script logs for specific error messages
3. Verify your Confluence Cloud site configuration
4. Ensure your API token has the necessary permissions
