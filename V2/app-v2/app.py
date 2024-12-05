from flask import Flask, request, jsonify
import json
import os
from skill_extraction import extract_skills_from_description, process_job_description

app = Flask(__name__)

CV_PATH = "cv_data.json"
if os.path.exists(CV_PATH):
    with open(CV_PATH, "r") as f:
        CV_DATA = json.load(f)
else:
    raise FileNotFoundError(f"CV data file '{CV_PATH}' not found.")

WHITELIST_PATH = "whitelist.json"

if os.path.exists(WHITELIST_PATH):
    with open(WHITELIST_PATH, "r") as f:
        WHITELIST = json.load(f)
else:
    raise FileNotFoundError(f"Whitelist file '{WHITELIST_PATH}' not found.")

BLACKLIST_PATH = "blacklist.json"

if os.path.exists(BLACKLIST_PATH):
    with open(BLACKLIST_PATH, "r") as f:
        BLACKLIST = json.load(f)["blacklist"]
else:
    raise FileNotFoundError(f"Blacklist file '{BLACKLIST_PATH}' not found.")


@app.route('/process', methods=['OPTIONS'])
def handle_preflight():
    response = jsonify({"message": "Preflight check passed"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response


# Endpoint to process a single job description
@app.route('/process', methods=['POST'])
def process_job():
    data = request.json
    job_description = data.get("job_description", "")
    
    if not job_description:
        return jsonify({"error": "Job description is required"}), 400

    # Process the job description
    matched_skills = process_job_description(job_description)
    
    return jsonify(matched_skills)

if __name__ == '__main__':
    app.run(debug=True)
