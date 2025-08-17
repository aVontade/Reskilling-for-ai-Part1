import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all routes, allowing frontend to communicate with backend
CORS(app)

# --- Data Loading ---
def load_data():
    """Loads roles and resources data from JSON files."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    roles_path = os.path.join(script_dir, 'data', 'roles.json')
    resources_path = os.path.join(script_dir, 'data', 'resources.json')
    try:
        with open(roles_path, 'r') as f:
            roles_data = json.load(f)
        with open(resources_path, 'r') as f:
            resources_data = json.load(f)
        return roles_data, resources_data
    except FileNotFoundError:
        # This is a critical error if the files are missing on startup
        print(f"CRITICAL: Could not find data files at {roles_path} or {resources_path}")
        return None, None

ROLES, RESOURCES = load_data()

# --- API Endpoint ---
@app.route('/api/analyze', methods=['POST'])
def analyze_role():
    """
    Analyzes a job title to provide an AI impact report, skill gap analysis,
    and a personalized learning plan.
    """
    # Get job title from the request body
    data = request.get_json()
    if not data or 'job_title' not in data:
        return jsonify({"error": "Missing job_title in request body"}), 400

    job_title_raw = data['job_title']
    job_title_key = job_title_raw.lower().strip()

    if not ROLES or not RESOURCES:
        return jsonify({"error": "Server data not loaded correctly."}), 500

    # Find the role in our data
    role_info = ROLES.get(job_title_key)
    if not role_info:
        return jsonify({"error": f"Role '{job_title_raw}' not found. Try one of our supported roles like 'Financial Analyst' or 'Marketing Manager'."}), 404

    # --- MVP Skill Gap Analysis ---
    # For this MVP, we assume a hardcoded set of skills the user possesses.
    user_skills = set([
        "Creativity",
        "Programming",
        "Emotional Intelligence"
    ])

    required_skills = set(role_info.get("required_skills", []))

    # Identify the skills the user needs to learn for this role
    skill_gap = list(required_skills - user_skills)

    # --- Learning Plan Generation ---
    learning_plan = []
    for skill in skill_gap:
        resources_for_skill = RESOURCES.get(skill)
        if resources_for_skill:
            learning_plan.append({
                "skill_to_learn": skill,
                "suggested_resources": resources_for_skill
            })

    # --- Construct the Response ---
    response_data = {
        "role_title": role_info.get("title"),
        "impact_level": role_info.get("impact_level"),
        "description": role_info.get("description"),
        "user_skills": sorted(list(user_skills)),
        "required_skills_for_role": role_info.get("required_skills", []),
        "learning_plan": learning_plan
    }

    return jsonify(response_data)

# --- Main execution ---
if __name__ == '__main__':
    # Note: `debug=True` is for development only.
    # In a production environment, use a proper WSGI server.
    app.run(debug=True, port=5000)
