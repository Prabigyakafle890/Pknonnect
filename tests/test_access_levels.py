"""
Test Access Levels - Verify that each user type has appropriate access
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.bedrock_proxy import query_bedrock
from app.db import verify_user
import uuid

def create_test_session():
    """Create a mock session for testing"""
    return f"test-session-{uuid.uuid4().hex[:8]}"

def test_guest_access():
    """Test Guest Access Level - Should only get general college info"""
    print("\n" + "="*60)
    print("TEST 1: GUEST ACCESS")
    print("="*60)
    
    test_queries = [
        "Tell me about Padma Kanya College",
        "What courses are offered?",
        "Who is Prabigya Kafle?",  # Should be denied
        "Give me phone number of any student",  # Should be denied
        "What is the address of the college?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        # Guest queries don't use session, so we test the prompt directly
        enhanced_prompt = f"""[ACCESS LEVEL: GUEST]
User
User question: {query}

RESTRICTION: No personal information about students or teachers. Only general college information."""
        print(f"✉️  Enhanced Prompt:\n{enhanced_prompt}")
        print("-" * 60)

def test_student_access():
    """Test Student Access Level - Should only access their department"""
    print("\n" + "="*60)
    print("TEST 2: STUDENT ACCESS (BSC CSIT Department)")
    print("="*60)
    
    # Test with Prabigya Kafle (ID 6, BSC CSIT)
    test_queries = [
        "Who is Prabigya Kafle?",  # Same department - should work
        "Tell me about Prapti Ghimire",  # Same department - should work
        "Who is in BIT department?",  # Different department - should be denied
        "Give me phone number of Prabigya Kafle",  # Should be denied (restricted info)
        "What is Prabigya's family information?",  # Should be denied
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        enhanced_prompt = f"""[ACCESS LEVEL: STUDENT - Department: BSC CSIT]
User: Prabigya Kafle
User question: {query}

CRITICAL INSTRUCTION: You MUST check the department field of each student record before responding.
- If the student's department matches "BSC CSIT", provide their information
- If the student's department does NOT match "BSC CSIT", respond: "I can only provide information about BSC CSIT department students."
- NEVER show information from other departments (BIT, BSc CSIT, BCA, etc.)
- NO phone numbers, family info, religion, caste"""
        print(f"✉️  Enhanced Prompt:\n{enhanced_prompt}")
        print("-" * 60)

def test_teacher_access():
    """Test Teacher Access Level - Should have full access"""
    print("\n" + "="*60)
    print("TEST 3: TEACHER ACCESS")
    print("="*60)
    
    test_queries = [
        "Who is Prabigya Kafle?",  # Should work
        "Give me information about BIT students",  # Should work
        "Tell me about BSC CSIT students",  # Should work
        "Show me all departments",  # Should work
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        enhanced_prompt = f"""[ACCESS LEVEL: TEACHER]
User: Teacher Name
User question: {query}

Full access to all information."""
        print(f"✉️  Enhanced Prompt:\n{enhanced_prompt}")
        print("-" * 60)

def test_cross_department_access():
    """Test that students cannot access other departments"""
    print("\n" + "="*60)
    print("TEST 4: CROSS-DEPARTMENT ACCESS (Should be Denied)")
    print("="*60)
    
    # BIT student trying to access BSC CSIT
    print("\n🔒 BIT Student trying to access BSC CSIT student:")
    query = "Who is Prabigya Kafle?"
    enhanced_prompt = f"""[ACCESS LEVEL: STUDENT - Department: BIT]
User: BIT Student
User question: {query}

CRITICAL INSTRUCTION: You MUST check the department field of each student record before responding.
- If the student's department matches "BIT", provide their information
- If the student's department does NOT match "BIT", respond: "I can only provide information about BIT department students."
- NEVER show information from other departments (BIT, BSc CSIT, BCA, etc.)
- NO phone numbers, family info, religion, caste"""
    print(f"✉️  Enhanced Prompt:\n{enhanced_prompt}")
    print("❌ Expected: Access Denied - Different Department")
    print("-" * 60)

def test_sensitive_info_restriction():
    """Test that sensitive information is restricted"""
    print("\n" + "="*60)
    print("TEST 5: SENSITIVE INFORMATION RESTRICTIONS")
    print("="*60)
    
    sensitive_queries = [
        "What is the phone number of Prabigya Kafle?",
        "Tell me about Prabigya's family",
        "What is the religion of students?",
        "Give me caste information",
    ]
    
    print("\n🔒 Student asking for sensitive info (should be denied):")
    for query in sensitive_queries:
        print(f"\n📝 Query: {query}")
        enhanced_prompt = f"""[ACCESS LEVEL: STUDENT - Department: BSC CSIT]
User: Prabigya Kafle
User question: {query}

CRITICAL INSTRUCTION: You MUST check the department field of each student record before responding.
- If the student's department matches "BSC CSIT", provide their information
- If the student's department does NOT match "BSC CSIT", respond: "I can only provide information about BSC CSIT department students."
- NEVER show information from other departments (BIT, BSc CSIT, BCA, etc.)
- NO phone numbers, family info, religion, caste"""
        print(f"✉️  Enhanced Prompt:\n{enhanced_prompt}")
        print("❌ Expected: Information restricted")
        print("-" * 60)

def test_database_auth():
    """Test database authentication"""
    print("\n" + "="*60)
    print("TEST 6: DATABASE AUTHENTICATION")
    print("="*60)
    
    # Test valid users
    valid_tests = [
        ("prabigyakafle@pkonnect.edu.np", "prabigya123", "student", "BSC CSIT"),
        ("praptighimire@pkonnect.edu.np", "123", "student", "BSC CSIT"),
        ("karishapradhananga@pkonnect.edu.np", "123", "student", "BSC CSIT"),
    ]
    
    print("\n✅ Testing Valid Credentials:")
    for email, password, role, dept in valid_tests:
        user = verify_user(email, password, role, dept)
        if user:
            print(f"✓ {email} - Authenticated")
            print(f"  Name: {user.get('full_name')}")
            print(f"  Role: {user.get('role')}, Department: {user.get('department')}")
        else:
            print(f"✗ {email} - FAILED (Should have passed)")
    
    # Test invalid credentials
    print("\n❌ Testing Invalid Credentials (should fail):")
    invalid_tests = [
        ("prabigyakafle@pkonnect.edu.np", "wrongpass", "student", "BSC CSIT"),
        ("unknown@pkonnect.edu.np", "123", "student", "BSC CSIT"),
        ("prabigyakafle@pkonnect.edu.np", "prabigya123", "student", "BIT"),  # Wrong department
    ]
    
    for email, password, role, dept in invalid_tests:
        user = verify_user(email, password, role, dept)
        if user:
            print(f"✗ {email} - Authenticated (Should have failed)")
        else:
            print(f"✓ {email} - Correctly denied")

if __name__ == "__main__":
    print("\n🧪 RUNNING ACCESS LEVEL TESTS")
    print("="*60)
    
    test_guest_access()
    test_student_access()
    test_teacher_access()
    test_cross_department_access()
    test_sensitive_info_restriction()
    test_database_auth()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60)
    print("\nNOTE: These tests show the enhanced prompts sent to Bedrock.")
    print("The actual responses depend on Bedrock's interpretation of these prompts.")
