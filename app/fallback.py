from app.bedrock_proxy import query_bedrock

def fallback_with_phi(user_message: str) -> str:
    # Use the same Bedrock Agent as the main chatbot
    return query_bedrock(user_message)
