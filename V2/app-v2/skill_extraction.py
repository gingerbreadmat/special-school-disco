import re
import json
import os
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# Pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

# Stop words list (common English words)
stop_words = STOP_WORDS

# Path to the skills database JSON file
DB_PATH = "skills_database.json"

# Path to your CV data file
CV_PATH = "cv_data.json"

# Path to whitelist and blacklist
WHITELIST_PATH = "whitelist.json"
BLACKLIST_PATH = "blacklist.json"

# Load the skills database
if os.path.exists(DB_PATH):
    with open(DB_PATH, "r") as f:
        skills_db = json.load(f)
else:
    skills_db = {
        "tech_skills": {},
        "soft_skills": {},
        "buzzwords": {},
        "new_skills": {}
    }

# Load CV data
if os.path.exists(CV_PATH):
    with open(CV_PATH, "r") as f:
        CV_DATA = json.load(f)
else:
    raise FileNotFoundError(f"CV data file '{CV_PATH}' not found.")

# Load Whitelist
if os.path.exists(WHITELIST_PATH):
    with open(WHITELIST_PATH, "r") as f:
        WHITELIST = json.load(f)
else:
    raise FileNotFoundError(f"Whitelist file '{WHITELIST_PATH}' not found.")

# Load Blacklist
if os.path.exists(BLACKLIST_PATH):
    with open(BLACKLIST_PATH, "r") as f:
        BLACKLIST = json.load(f)["blacklist"]
else:
    raise FileNotFoundError(f"Blacklist file '{BLACKLIST_PATH}' not found.")


def clean_skills(extracted_skills):
    """
    Cleans up the list of extracted skills by:
    - Removing stop words
    - Filtering out short words
    """
    cleaned_skills = [
        skill for skill in extracted_skills
        if skill not in stop_words and len(skill) > 2
    ]
    return cleaned_skills


def extract_skills_from_description(job_description):
    """
    Extracts skills from a job description using NLP and predefined patterns.
    """
    doc = nlp(job_description.lower())
    potential_skills = set()

    # Match predefined patterns
    patterns = [
        r"experience with (\w+)",
        r"knowledge of (\w+)",
        r"proficient in (\w+)"
    ]
    for pattern in patterns:
        matches = re.findall(pattern, job_description.lower())
        potential_skills.update(matches)

    # Extract tokens from the text
    for token in doc:
        if token.text.lower() not in stop_words and len(token.text) > 2:
            potential_skills.add(token.text)

    valid_skills = clean_skills(potential_skills)
    return valid_skills


def filter_with_whitelist_and_blacklist(extracted_skills):
    """
    Filters the extracted skills using the whitelist and excludes terms in the blacklist.
    """
    filtered_skills = {
        "tech_skills": [],
        "soft_skills": [],
        "buzzwords": [],
        "new_skills": []
    }

    for skill in extracted_skills:
        skill = skill.lower().strip()

        # Skip blacklisted terms
        if skill in BLACKLIST:
            continue

        # Whitelist filtering
        if skill in WHITELIST["tech_skills"]:
            filtered_skills["tech_skills"].append(skill)
        elif skill in WHITELIST["soft_skills"]:
            filtered_skills["soft_skills"].append(skill)
        elif skill in WHITELIST["buzzwords"]:
            filtered_skills["buzzwords"].append(skill)
        else:
            filtered_skills["new_skills"].append(skill)  # If not in whitelist or blacklist, classify as new skill

    return filtered_skills


def calculate_match_percentage(matched_skills, extracted_skills, cv_skills, weight):
    """
    Calculates the match percentage for a specific skill category.
    """
    matched_count = len(set(matched_skills) & set(cv_skills))
    total_count = len(set(extracted_skills))
    if total_count == 0:
        return 0
    return (matched_count / total_count) * weight


def process_job_description(job_description):
    """
    Processes a job description to match skills against the CV and filter with whitelist/blacklist.
    """
    extracted_skills = extract_skills_from_description(job_description)
    filtered_skills = filter_with_whitelist_and_blacklist(extracted_skills)

    # Match against CV
    tech_match = calculate_match_percentage(
        filtered_skills["tech_skills"],
        extracted_skills,
        CV_DATA["tech_skills"],
        weight=60
    )
    soft_skills_match = calculate_match_percentage(
        filtered_skills["soft_skills"],
        extracted_skills,
        CV_DATA["soft_skills"],
        weight=20
    )
    buzzwords_match = calculate_match_percentage(
        filtered_skills["buzzwords"],
        extracted_skills,
        CV_DATA["tech_skills"],  # Buzzwords overlap with tech skills for simplicity
        weight=20
    )

    overall_match = tech_match + soft_skills_match + buzzwords_match

    # Save new skills to the database for future review
    for skill in filtered_skills["new_skills"]:
        skills_db["new_skills"][skill] = skills_db["new_skills"].get(skill, 0) + 1

    # Save updated database
    with open(DB_PATH, "w") as f:
        json.dump(skills_db, f, indent=4)

    return {
        "match_percentage": f"{overall_match:.2f}%",
        "filtered_skills": filtered_skills,
        "new_skills": filtered_skills["new_skills"]
    }
