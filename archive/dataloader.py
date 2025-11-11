import pandas as pd
import os

def load_department_data(department):
    """
    Load CSV and Excel data for the specified department.
    """
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    data = []
    if department == 'BSC CSIT':
        # Load teacher data
        teacher_filepath = os.path.join(base_path, 'bsc_csit_data.csv')
        if os.path.exists(teacher_filepath):
            df = pd.read_csv(teacher_filepath)
            data.extend(df.to_dict(orient='records'))
        # Load student data
        student_filepath = os.path.join(base_path, 'batch2078.xlsx')
        if os.path.exists(student_filepath):
            df = pd.read_excel(student_filepath)
            data.extend(df.to_dict(orient='records'))
    elif department == 'BIT':
        filepath = os.path.join(base_path, 'bit_data.csv')
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            data.extend(df.to_dict(orient='records'))
    return data

def search_data(data, keywords, full_query=""):
    """
    Search for rows in data that contain any of the keywords in any column.
    Prioritizes exact name matches if full_query contains a potential full name.
    Returns matching rows as a list of dicts.
    """
    if not data:
        return []
    matches = []

    # Check for potential full name in query (2-3 words)
    query_words = full_query.lower().split()
    potential_names = []
    if len(query_words) >= 2:
        # Look for sequences of 2-3 words that might be names
        for i in range(len(query_words)):
            for j in range(2, min(4, len(query_words) - i + 1)):
                potential_names.append(' '.join(query_words[i:i+j]))

    # First, find exact name matches
    exact_matches = []
    for row in data:
        if 'name_of_teacher' in row:
            teacher_name = str(row.get('name_of_teacher', '')).lower()
            for name in potential_names:
                if name in teacher_name or teacher_name in name:
                    exact_matches.append(row)
                    break
        elif 'Nameof students' in row:
            student_name = str(row.get('Nameof students', '')).lower()
            for name in potential_names:
                if name in student_name or student_name in name:
                    exact_matches.append(row)
                    break

    if exact_matches:
        return exact_matches[:5]  # Return exact matches first

    # Fallback to keyword search
    for row in data:
        # Convert all values to strings, handling NaN values properly
        row_values = []
        for key, val in row.items():
            if val is not None and str(val).lower() != 'nan':
                row_values.append(str(val).lower())
        row_str = ' '.join(row_values)
        
        # Check if any keyword matches
        if any(keyword.lower() in row_str for keyword in keywords):
            matches.append(row)
            
        # Special handling for numeric keywords (like "1st", "1", "first")
        if any(keyword in ['1st', '1', 'first'] for keyword in keywords):
            if str(row.get('semester', '')).strip() == '1':
                matches.append(row)
        elif any(keyword in ['2nd', '2', 'second'] for keyword in keywords):
            if str(row.get('semester', '')).strip() == '2':
                matches.append(row)
        elif any(keyword in ['3rd', '3', 'third'] for keyword in keywords):
            if str(row.get('semester', '')).strip() == '3':
                matches.append(row)
        # Add more semester patterns as needed
                
    # Remove duplicates while preserving order
    seen = set()
    unique_matches = []
    for match in matches:
        # Create a unique identifier for each match
        match_id = (match.get('name_of_teacher', ''), match.get('subject', ''), match.get('semester', ''))
        if match_id not in seen:
            seen.add(match_id)
            unique_matches.append(match)
    
    return unique_matches[:5]
