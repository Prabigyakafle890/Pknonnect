#!/usr/bin/env python3
"""
Test user login and database
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import init_db, verify_user, get_connection

def test_user_database():
    """Test user database functionality"""
    print("🗄️ Testing User Database")
    print("=" * 40)
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Test user verification
    test_cases = [
        ('student1@pkonnect.edu.np', 'password123', 'student', 'BSC CSIT'),
        ('teacher1@pkonnect.edu.np', 'password123', 'teacher', 'BSC CSIT'),
        ('invalid@test.com', 'wrong', 'student', 'BSC CSIT')
    ]
    
    for email, password, role, department in test_cases:
        result = verify_user(email, password, role, department)
        status = "✅ Valid" if result else "❌ Invalid"
        print(f"{status} - {email} as {role} in {department}")
    
    # List all users
    print("\n📋 All users in database:")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT email, role, department FROM users')
    users = cursor.fetchall()
    for user in users:
        print(f"- {user[0]} | {user[1]} | {user[2]}")
    conn.close()

if __name__ == "__main__":
    test_user_database()