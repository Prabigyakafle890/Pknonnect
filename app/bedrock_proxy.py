from app.bedrock_client import bedrock_client
from flask import session as flask_session
import uuid

# ---------------- QUERY BEDROCK AGENT ----------------
def query_bedrock(prompt, user_type="guest", department=None, role=None, user_name=None):
    """
    Query AWS Bedrock Agent with access-based control.
    The agent is configured with knowledge about Padma Kanya College and access levels.
    """
    
    is_new_session = 'bedrock_session_id' not in flask_session
    
    if is_new_session:
        flask_session['bedrock_session_id'] = f"session-{uuid.uuid4().hex[:8]}"
    
    session_id = flask_session['bedrock_session_id']
    
    # ALWAYS add access control context to maintain restrictions throughout conversation
    metadata_filter = None  # For knowledge base filtering
    
    # Build user identity string if name is available
    user_identity = f"User: {user_name}" if user_name else "User"
    
    if user_type == "guest":
        enhanced_prompt = f"""[ACCESS LEVEL: GUEST]
{user_identity}
User question: {prompt}

RESTRICTION: No personal information about students or teachers. Only general college information."""

    elif user_type == "student":
        # For students, use prompt-based filtering instead of metadata filter
        # The agent will filter based on the prompt instructions
        enhanced_prompt = f"""[ACCESS LEVEL: STUDENT - Department: {department}]
{user_identity}
User question: {prompt}

CRITICAL INSTRUCTION: You MUST check the department field of each student record before responding.
- If the student's department matches "{department}", provide their information
- If the student's department does NOT match "{department}", respond: "I can only provide information about {department} department students."
- NEVER show information from other departments (BIT, BSc CSIT, BCA, etc.)
- NO phone numbers, family info, religion, caste
- Don't give /n"""

    elif user_type == "teacher":
        enhanced_prompt = f"""[ACCESS LEVEL: TEACHER]
{user_identity}
User question: {prompt}

Full access to all information."""

    else:
        enhanced_prompt = f"""[ACCESS LEVEL: GUEST]
{user_identity}
User question: {prompt}

RESTRICTION: Only general college information."""
        
    try:
        # Temporarily disable metadata filter to test if data is accessible
        # We'll rely on prompt-based filtering for now
        response = bedrock_client.chat(
            user_message=enhanced_prompt,
            session_id=session_id,
            metadata_filter=None  # Disabled for now
        )
        return response if response else "Sorry, I couldn't process your request at the moment."
    except Exception as e:
        print(f"Bedrock Agent API error: {e}")
        return "Sorry, I couldn't process your request at the moment."

# ---------------- HANDLE USER QUERY ----------------
def handle_user_query(user_query, user_type="guest", department=None, role=None, user_name=None):
    """
    Handle user query with Bedrock - all responses come from trained agent.
    Access control is handled through context prompts.
    """
    return query_bedrock(user_query, user_type, department, role, user_name)