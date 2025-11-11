#!/usr/bin/env python3
"""
Test complete chatbot flow with student access
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.chatbot import get_response

def test_student_query():
    """Test the complete student query flow"""
    print("🧪 Testing Complete Student Query Flow")
    print("=" * 60)
    
    test_query = "teachers of 1st semester of bsc csit"
    print(f"Query: {test_query}")
    print()
    
    # Test as student
    print("🎓 Student Response:")
    response = get_response(
        message=test_query,
        user_type='student',
        department='BSC CSIT',
        role='student'
    )
    print(response)
    print()
    
    # Test another query
    test_query2 = "Who teaches C Programming in first semester?"
    print(f"Query: {test_query2}")
    print()
    
    print("🎓 Student Response:")
    response2 = get_response(
        message=test_query2,
        user_type='student',
        department='BSC CSIT',
        role='student'
    )
    print(response2)

if __name__ == "__main__":
    test_student_query()