import re

def extract_keywords(query):
    """Extract keywords from user query for searching"""
    # Remove common stop words and extract meaningful terms
    stop_words = {'is', 'are', 'the', 'of', 'in', 'at', 'to', 'for', 'on', 'with', 'by', 'about', 'tell', 'me'}
    words = re.findall(r'\w+', query.lower())
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return keywords

def recognize_intent(message):
    """
    Simple intent recognition for access control.
    All actual responses come from AWS Bedrock.
    """
    message = message.lower()
    if "admission" in message or "enroll" in message:
        return "admission_info"
    elif "result" in message or "grade" in message or "marks" in message:
        return "exam_result"
    elif "salary" in message or "budget" in message or "finance" in message:
        return "confidential_finance"
    elif "teacher" in message or "faculty" in message or "lecturer" in message:
        return "teacher_info"
    elif "student" in message and ("contact" in message or "email" in message or "phone" in message):
        return "student_contact"
    else:
        return "general"

def is_allowed_for_user(intent, user_type, role=None):
    """
    Check if user has permission to ask about specific topics.
    Note: AWS Bedrock handles all actual data and responses.
    This is just for topic-level access control.
    """
    
    # Guests can access most general information
    if user_type == "guest":
        return intent in ["general", "admission_info", "teacher_info"]
    
    # Students have broader access but limited sensitive info
    elif user_type == "student":
        return intent not in ["confidential_finance", "student_contact"]
    
    # Teachers have full access to all topics
    elif user_type == "teacher":
        return True
    
    # Default: allow general access
    return intent == "general"
