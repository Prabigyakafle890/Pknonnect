# AWS Bedrock Agent Configuration

# AWS Region (change as needed)
AWS_REGION = 'us-east-2'

# AWS Bedrock Agent Configuration
# These values can be overridden by environment variables
DEFAULT_AGENT_ID = 'KGNSQQYWQD'
DEFAULT_ALIAS_ID = 'Y5HBOIBFJR'
DEFAULT_SESSION_ID = 'session-001'

# Available Bedrock Foundation Models (for reference)
# Note: When using Bedrock Agents, the agent configuration determines which model is used
BEDROCK_MODELS = {
    'claude-3-haiku': 'anthropic.claude-3-haiku-20240307-v1:0',
    'claude-3-sonnet': 'anthropic.claude-3-sonnet-20240229-v1:0',
    'claude-3-opus': 'anthropic.claude-3-opus-20240229-v1:0',
    'claude-instant': 'anthropic.claude-instant-v1',
    'llama2-13b': 'meta.llama2-13b-chat-v1',
    'llama2-70b': 'meta.llama2-70b-chat-v1'
}

# Note: Bedrock Agents handle their own token limits and model selection
# These settings are managed in the AWS Bedrock console