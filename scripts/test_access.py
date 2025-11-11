#!/usr/bin/env python3
"""
Test access control for different user types
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.chatbot import get_response
from app.utils import recognize_intent, is_allowed_for_user

def test_access_levels():
    """Test different access levels"""
    test_message = "Who are the teachers of 1st semester BSC CSIT?"
    
    print("🧪 Testing Access Control")
    print("=" * 50)
    print(f"Test Query: {test_message}")
    print()
    
    # Test Guest Access
    print("👤 Guest Access:")
    guest_response = get_response(test_message, user_type='guest')
    print(f"Response: {guest_response[:100]}...")
    print()
    
    # Test Student Access
    print("🎓 Student Access:")
    student_response = get_response(test_message, user_type='student', department='BSC CSIT', role='student')
    print(f"Response: {student_response[:100]}...")
    print()
    
    # Test Teacher Access
    print("👩‍🏫 Teacher Access:")
    teacher_response = get_response(test_message, user_type='teacher', department='BSC CSIT', role='teacher')
    print(f"Response: {teacher_response[:100]}...")
    print()
    
    # Test Intent Recognition
    print("🔍 Intent Recognition:")
    intent = recognize_intent(test_message)
    print(f"Detected Intent: {intent}")
    
    print("📋 Access Permissions:")
    print(f"Guest can access: {is_allowed_for_user(intent, 'guest')}")
    print(f"Student can access: {is_allowed_for_user(intent, 'student')}")
    print(f"Teacher can access: {is_allowed_for_user(intent, 'teacher')}")

if __name__ == "__main__":
    test_access_levels()