# Archive Directory

This directory contains deprecated files that were used in earlier versions of the PKonnect chatbot but are no longer needed.

## Archived Files

### dataloader.py
- **Purpose**: CSV data loading and searching functionality
- **Status**: Restored to active use in hybrid approach
- **Date archived**: November 4, 2024

### data/ directory
- **Purpose**: Contains CSV files with course and department information
- **Status**: Data files moved back to main data/ directory
- **Note**: Used for local data search in hybrid approach

### debug_scripts/ directory
- **Purpose**: Contains debugging and testing scripts
- **Contents**: 
  - debug_data.py
  - debug_general_knowledge.py
  - debug_general_students.py
  - debug_prabigya.py
  - debug_prabigya_variations.py
  - test_restored_version.py
- **Reason for archival**: Development and debugging complete
- **Date archived**: November 4, 2024

### bedrock_system_prompt.txt
- **Purpose**: System prompt configuration for Bedrock agent
- **Reason for archival**: System prompt configured directly in Bedrock agent
- **Date archived**: November 4, 2024

## Current Architecture

The chatbot uses a **hybrid approach**:
- **Local data search** for specific student/teacher information
- **AWS Bedrock** for general college information and AI responses
- **Best of both worlds**: Fast specific data lookup + intelligent AI responses

## Active Dependencies
- flask, flask-cors
- requests
- pandas, openpyxl (for local data processing)
- boto3 (for AWS Bedrock)
- python-dotenv (for configuration)