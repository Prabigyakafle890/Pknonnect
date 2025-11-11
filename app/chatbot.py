from app.bedrock_proxy import query_bedrock

def get_response(user_query, user_type="guest", department=None, role=None, user_name=None):
    """
    Get chatbot response using AWS Bedrock with access-based control.
    All responses come from Bedrock agent with appropriate access level context.
    """
    
    # Route all queries to Bedrock with access control
    return query_bedrock(user_query, user_type, department, role, user_name)
