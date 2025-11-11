import os
import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError

# Optional: load environment variables from a .env file if present
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # dotenv is optional; safe to continue if not installed
    pass

class BedrockClient:
    def __init__(self):
        """
        Initialize AWS Bedrock Agent client
        Make sure AWS credentials are configured via:
        - AWS credentials file (~/.aws/credentials)
        - Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        - IAM roles (if running on EC2)
        - AWS_PROFILE environment variable
        """
        # Configuration from environment variables
        self.region = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-2"))
        self.agent_id = os.getenv("AGENT_ID", "KGNSQQYWQD")
        self.alias_id = os.getenv("AGENT_ALIAS_ID", "Y5HBOIBFJR")
        self.session_id = os.getenv("SESSION_ID", "session-001")
        aws_profile = os.getenv("AWS_PROFILE")
        
        try:
            # Use a session so we can honor AWS_PROFILE if provided
            if aws_profile:
                self.session = boto3.Session(profile_name=aws_profile, region_name=self.region)
            else:
                self.session = boto3.Session(region_name=self.region)
            
            self.bedrock_agent = self.session.client("bedrock-agent-runtime")
        except NoCredentialsError:
            self.bedrock_agent = None
        except Exception as e:
            self.bedrock_agent = None
    
    def set_agent_config(self, agent_id, alias_id, session_id=None):
        """Set the agent configuration"""
        self.agent_id = agent_id
        self.alias_id = alias_id
        if session_id:
            self.session_id = session_id
    
    def _format_response(self, text):
        """
        Format the agent's response by handling escaped characters and converting to proper format
        """
        # Replace literal \n with actual newlines
        text = text.replace('\\n', '\n')
        
        # Replace literal \t with spaces
        text = text.replace('\\t', '    ')
        
        # Remove any remaining backslash escapes
        text = text.replace('\\', '')
        
        # Clean up multiple consecutive newlines (max 2)
        import re
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Clean up spaces around newlines
        text = re.sub(r' +\n', '\n', text)
        text = re.sub(r'\n +', '\n', text)
        
        return text.strip()
    
    def chat(self, user_message, session_id=None, metadata_filter=None):
        """
        Send a message to AWS Bedrock Agent and get response
        
        Args:
            user_message: The message to send to the agent
            session_id: Optional session ID for conversation continuity
            metadata_filter: Optional dict for filtering knowledge base results
                            Example: {'department': 'BSc CSIT'}
        """
        if not self.bedrock_agent:
            return "AWS Bedrock Agent client not initialized. Please check your credentials."
        
        # Use provided session_id or default
        current_session_id = session_id or self.session_id
        
        try:
            # Build the request parameters
            request_params = {
                'agentId': self.agent_id,
                'agentAliasId': self.alias_id,
                'sessionId': current_session_id,
                'inputText': user_message,
            }
            
            # Add session state with knowledge base configuration
            # Significantly increased chunks for comprehensive retrieval
            # More chunks = better chance of finding all students and their complete data
            kb_config = {
                'knowledgeBaseId': '4DD13OSHSU',  # pkstudents-knowledgebase
                'retrievalConfiguration': {
                    'vectorSearchConfiguration': {
                        'numberOfResults': 50,  # Increased to 50 for queries involving multiple students
                        'overrideSearchType': 'HYBRID'  # Use hybrid search (semantic + keyword) for better accuracy
                    }
                }
            }
            
            # Add metadata filter if provided
            if metadata_filter:
                kb_config['retrievalConfiguration']['vectorSearchConfiguration']['filter'] = {
                    'equals': {
                        'key': 'department',
                        'value': metadata_filter.get('department', '')
                    }
                }
            
            request_params['sessionState'] = {
                'knowledgeBaseConfigurations': [kb_config],
                # Add prompt session attributes to guide the agent
                'promptSessionAttributes': {
                    'retrievalMode': 'comprehensive',
                    'includeAllResults': 'true'
                }
            }
            
            # Invoke the Bedrock Agent
            response_stream = self.bedrock_agent.invoke_agent(**request_params)
            
            # Collect the reply from the event stream
            output_text = []
            citations = []
            
            # The response is an event stream of "chunks"
            for event in response_stream.get("completion", []):
                if "chunk" in event:
                    chunk_data = event["chunk"]
                    if "bytes" in chunk_data:
                        chunk = chunk_data["bytes"].decode("utf-8")
                        output_text.append(chunk)
                    # Collect citations to see what sources were used
                    if "attribution" in chunk_data:
                        citations.extend(chunk_data.get("attribution", {}).get("citations", []))
                elif "trace" in event:
                    # Log trace for debugging retrieval issues
                    trace = event.get("trace", {})
                    if "orchestrationTrace" in trace:
                        orch_trace = trace["orchestrationTrace"]
                        # Log retrieval results count for debugging
                        if "observation" in orch_trace:
                            obs = orch_trace["observation"]
                            if "knowledgeBaseLookupOutput" in obs:
                                kb_output = obs["knowledgeBaseLookupOutput"]
                                retrieved_refs = kb_output.get("retrievedReferences", [])
                                print(f"DEBUG: Retrieved {len(retrieved_refs)} documents from knowledge base")
            
            result = "".join(output_text)
            
            # Format the response to handle escaped characters and markdown
            if result:
                result = self._format_response(result)
            
            return result if result else "Sorry, I couldn't generate a response."
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                return "Access denied. Please check your AWS permissions for Bedrock Agents."
            elif error_code == 'ValidationException':
                return "Invalid request. Please check the agent ID and alias ID."
            elif error_code == 'ResourceNotFoundException':
                return "Agent not found. Please check your agent ID and alias ID."
            else:
                return f"AWS Bedrock Agent error: {error_code}"
        except NoCredentialsError:
            return "No AWS credentials found. Set AWS_PROFILE or AWS_ACCESS_KEY_ID/SECRET and try again."
        except Exception as e:
            return f"Unexpected error: {str(e)}"

# Global instance
bedrock_client = BedrockClient()