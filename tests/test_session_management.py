"""
Test Session Management - Verify session handling and conversation continuity
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from flask import session as flask_session

def test_session_creation():
    """Test that sessions are created properly"""
    print("\n" + "="*60)
    print("TEST 1: SESSION CREATION")
    print("="*60)
    
    app = create_app()
    
    with app.test_request_context():
        with app.test_client() as client:
            # Login as student
            response = client.post('/login', json={
                'email': 'prabigyakafle@pkonnect.edu.np',
                'password': 'prabigya123',
                'role': 'student',
                'department': 'BSC CSIT'
            })
            
            print(f"\n📝 Login Response: {response.get_json()}")
            
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    print("✅ Login successful")
                    print(f"   User Type: {data.get('user_type')}")
                    print(f"   Full Name: {data.get('full_name')}")
                    print(f"   Department: {data.get('department')}")
                else:
                    print(f"❌ Login failed: {data.get('message')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")

def test_login_status():
    """Test login status endpoint"""
    print("\n" + "="*60)
    print("TEST 2: LOGIN STATUS CHECK")
    print("="*60)
    
    app = create_app()
    
    with app.test_client() as client:
        # Check status before login
        print("\n📝 Checking status before login...")
        response = client.get('/check-login-status')
        data = response.get_json()
        print(f"Response: {data}")
        
        if not data.get('logged_in'):
            print("✅ Correctly shows not logged in")
        else:
            print("❌ Should not be logged in")
        
        # Login
        print("\n📝 Logging in...")
        login_response = client.post('/login', json={
            'email': 'prabigyakafle@pkonnect.edu.np',
            'password': '123',
            'role': 'student',
            'department': 'BSC CSIT'
        })
        
        login_data = login_response.get_json()
        if login_data.get('success'):
            print("✅ Login successful")
            
            # Check status after login
            print("\n📝 Checking status after login...")
            response = client.get('/check-login-status')
            data = response.get_json()
            print(f"Response: {data}")
            
            if data.get('logged_in') and data.get('full_name') == 'Prabigya Kafle':
                print("✅ Correctly shows logged in with full name")
            else:
                print("❌ Status not updated correctly")
        else:
            print(f"❌ Login failed: {login_data.get('message')}")

def test_logout():
    """Test logout functionality"""
    print("\n" + "="*60)
    print("TEST 3: LOGOUT")
    print("="*60)
    
    app = create_app()
    
    with app.test_client() as client:
        # Login first
        print("\n📝 Logging in...")
        client.post('/login', json={
            'email': 'praptighimire@pkonnect.edu.np',
            'password': '123',
            'role': 'student',
            'department': 'BSC CSIT'
        })
        
        # Check logged in
        response = client.get('/check-login-status')
        if response.get_json().get('logged_in'):
            print("✅ Login confirmed")
            
            # Logout
            print("\n📝 Logging out...")
            logout_response = client.post('/logout')
            logout_data = logout_response.get_json()
            print(f"Logout Response: {logout_data}")
            
            # Check status after logout
            print("\n📝 Checking status after logout...")
            response = client.get('/check-login-status')
            data = response.get_json()
            
            if not data.get('logged_in'):
                print("✅ Successfully logged out")
            else:
                print("❌ Still showing as logged in")
        else:
            print("❌ Login failed")

def test_session_persistence():
    """Test that session persists across requests"""
    print("\n" + "="*60)
    print("TEST 4: SESSION PERSISTENCE")
    print("="*60)
    
    app = create_app()
    
    with app.test_client() as client:
        # Login
        print("\n📝 Logging in as Karisha Pradhananga...")
        client.post('/login', json={
            'email': 'karishapradhananga@pkonnect.edu.np',
            'password': '123',
            'role': 'student',
            'department': 'BSC CSIT'
        })
        
        # Make multiple requests and check session persists
        for i in range(3):
            print(f"\n📝 Request #{i+1}...")
            response = client.get('/check-login-status')
            data = response.get_json()
            
            if data.get('logged_in') and data.get('full_name') == 'Karisha Pradhananga':
                print(f"✅ Session persists - User: {data.get('full_name')}")
            else:
                print(f"❌ Session lost on request #{i+1}")
                break

def test_multiple_users():
    """Test multiple users with different access levels"""
    print("\n" + "="*60)
    print("TEST 5: MULTIPLE USERS")
    print("="*60)
    
    app = create_app()
    
    users = [
        {
            'email': 'prabigyakafle@pkonnect.edu.np',
            'password': 'prabigya123',
            'role': 'student',
            'department': 'BSC CSIT',
            'expected_name': 'Prabigya Kafle'
        },
        {
            'email': 'praptighimire@pkonnect.edu.np',
            'password': '123',
            'role': 'student',
            'department': 'BSC CSIT',
            'expected_name': 'Prapti Ghimire'
        },
        {
            'email': 'karishapradhananga@pkonnect.edu.np',
            'password': '123',
            'role': 'student',
            'department': 'BSC CSIT',
            'expected_name': 'Karisha Pradhananga'
        },
    ]
    
    for user in users:
        print(f"\n📝 Testing user: {user['email']}")
        
        with app.test_client() as client:
            response = client.post('/login', json={
                'email': user['email'],
                'password': user['password'],
                'role': user['role'],
                'department': user['department']
            })
            
            data = response.get_json()
            if data.get('success') and data.get('full_name') == user['expected_name']:
                print(f"✅ {user['expected_name']} logged in successfully")
            else:
                print(f"❌ Failed for {user['email']}")

if __name__ == "__main__":
    print("\n🧪 RUNNING SESSION MANAGEMENT TESTS")
    print("="*60)
    
    test_session_creation()
    test_login_status()
    test_logout()
    test_session_persistence()
    test_multiple_users()
    
    print("\n" + "="*60)
    print("✅ ALL SESSION TESTS COMPLETED")
    print("="*60)
