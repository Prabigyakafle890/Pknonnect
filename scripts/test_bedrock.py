#!/usr/bin/env python3
"""
Simple AWS Bedrock connectivity test
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.bedrock_client import bedrock_client

def main():
    print("🔍 Testing AWS Bedrock connection...")
    
    if not bedrock_client.bedrock_agent:
        print("❌ Bedrock client not initialized. Check your AWS credentials in app/.env")
        return False
    
    # Simple test query
    response = bedrock_client.chat("Hello")
    
    if "error" in response.lower() or "couldn't" in response.lower():
        print(f"❌ Connection failed: {response}")
        return False
    else:
        print("✅ AWS Bedrock connection successful!")
        return True

if __name__ == "__main__":
    main()