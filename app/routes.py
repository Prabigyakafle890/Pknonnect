from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from app.bedrock_proxy import query_bedrock
from app.db import verify_user
import requests
import re

chatbot_bp = Blueprint('chatbot_bp', __name__)

# Home page
@chatbot_bp.route("/")
def home():
    return render_template("index.html")

# Guest page
@chatbot_bp.route("/guest")
def guest():
    return render_template("guest.html")

# Chatbot page
@chatbot_bp.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

# Select Department
@chatbot_bp.route('/select-department', methods=['GET', 'POST'])
def select_department():
    if request.method == 'POST':
        department = request.form.get('department')
        if department:
            session['department'] = department
            return redirect(url_for('chatbot_bp.select_role'))
    return render_template('department_select.html')

# Select Role
@chatbot_bp.route('/select-role', methods=['GET', 'POST'])
def select_role():
    if request.method == 'POST':
        role = request.form.get('role')
        if role:
            session['role'] = role
            return redirect(url_for('chatbot_bp.institution_login'))
    return render_template('role_select.html')

# Institution Login
@chatbot_bp.route('/institution-login', methods=['GET', 'POST'])
def institution_login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        department = session.get('department')
        role = session.get('role')
        if not department or not role:
            error = "Session expired. Please start over."
        elif re.match(r'^[a-z0-9._%+-]+@pkonnect\.edu\.np$', email) and password:
            user = verify_user(email, password, role, department)
            if user:
                session['user_email'] = email
                session['user_name'] = user.get('full_name')
                session['is_student'] = True  # This covers all institutional users
                session['user_type'] = 'teacher' if role == 'teacher' else 'student'
                return redirect(url_for('chatbot_bp.student'))
            else:
                error = "Invalid credentials."
        else:
            error = "Invalid email or password."
    return render_template('institution_login.html', error=error)

# Student page
@chatbot_bp.route('/student')
def student():
    if not session.get('is_student'):
        return redirect(url_for('chatbot_bp.select_department'))
    return render_template('chatbot.html', user_type='student')

# Google Sign-In callback
@chatbot_bp.route('/signin/callback', methods=['POST', 'GET'])
def google_callback():
    # Google sends the ID token as a POST parameter named 'credential'
    token = request.form.get('credential') or request.json.get('credential')
    if not token:
        return "Missing credential", 400

    # Verify token with Google
    google_resp = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
    if google_resp.status_code != 200:
        return "Invalid token", 400

    user_info = google_resp.json()
    # Save user info in session
    session['user_email'] = user_info.get('email')
    session['user_name'] = user_info.get('name')
    # Redirect to chatbot or dashboard
    return redirect(url_for('chatbot_bp.chatbot'))

# Chat endpoint
@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        if not message:
            return jsonify({'response': 'No message provided.'}), 400

        # Get user type from request (sent from frontend)
        user_type = data.get('user_type', 'guest')
        department = data.get('department')
        role = data.get('role')
        user_name = None
        
        # Validate against session to prevent frontend manipulation
        if user_type != 'guest':
            if not session.get('is_student'):
                # Not logged in on backend, force guest mode
                user_type = 'guest'
                department = None
                role = None
            else:
                # Verify session matches
                session_role = session.get('role', 'student')
                session_dept = session.get('department')
                user_name = session.get('user_name')
                
                # Use session data (don't trust frontend completely)
                department = session_dept
                role = session_role
                user_type = 'teacher' if session_role == 'teacher' else 'student'

        from app.chatbot import get_response
        response = get_response(message, user_type, department, role, user_name)
        
        return jsonify({'response': response})

    except Exception as e:
        print("❌ Chat route error:", e)
        return jsonify({'response': 'Internal server error occurred.'}), 500

# Login endpoint
@chatbot_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        role = data.get('role', '')
        department = data.get('department', '')
        
        if not email or not password or not role or not department:
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        # Verify with database
        user = verify_user(email, password, role, department)
        if user:
            # Set session
            session['user_email'] = email
            session['user_name'] = user.get('full_name')
            session['is_student'] = True
            session['role'] = role
            session['department'] = department
            session['user_type'] = 'teacher' if role == 'teacher' else 'student'
            
            return jsonify({
                'success': True,
                'user_type': session['user_type'],
                'role': role,
                'department': department,
                'full_name': user.get('full_name'),
                'logged_in': True
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return jsonify({'success': False, 'message': 'Login failed'})

# Check login status
@chatbot_bp.route('/check-login-status', methods=['GET'])
def check_login_status():
    if session.get('is_student'):
        return jsonify({
            'logged_in': True,
            'user_type': session.get('user_type', 'guest'),
            'role': session.get('role'),
            'department': session.get('department'),
            'full_name': session.get('user_name')
        })
    else:
        return jsonify({'logged_in': False, 'user_type': 'guest'})

# Logout endpoint (clear session)
@chatbot_bp.route('/logout', methods=['POST'])
def logout():
    """Clear session to switch to guest mode"""
    session.pop('user_email', None)
    session.pop('user_name', None)
    session.pop('is_student', None)
    session.pop('role', None)
    session.pop('department', None)
    session.pop('user_type', None)
    # Also clear the Bedrock session to start fresh
    session.pop('bedrock_session_id', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# History endpoint (no DB, returns empty)
@chatbot_bp.route('/history', methods=['GET'])
@chatbot_bp.route('/history', methods=['GET'])
def history():
    return jsonify({'history': []})

# Clear conversation endpoint - starts a new session
@chatbot_bp.route('/clear-conversation', methods=['POST'])
def clear_conversation():
    """Clear the current Bedrock session to start a fresh conversation"""
    if 'bedrock_session_id' in session:
        del session['bedrock_session_id']
    return jsonify({'message': 'Conversation cleared successfully'})


@chatbot_bp.route('/student-login', methods=['GET', 'POST'])
def student_login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        # Replace with your college's domain
        if re.match(r'^[a-z0-9._%+-]+@pkonnect\.edu\.np$', email):
            session['user_email'] = email
            session['is_student'] = True
            return redirect(url_for('chatbot_bp.student'))
        else:
            error = "Please enter a valid college student email."
    return render_template('institution_login.html', error=error)