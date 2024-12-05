from flask import Flask, request, jsonify, make_response
import re

try:
    from mangum import Mangum 
except ImportError:
    Mangum = None

app = Flask(__name__)

# Technical skills list
TECH_SKILLS = [
    # Programming Languages
    "python", "py", "javascript", "js", "java", "c++", "c#", "csharp", 
    "ruby", "go", "golang", "swift", "kotlin", "php", "typescript", 
    "ts", "scala", "perl", "rust", "haskell", "r", "matlab", "shell",
    "bash", "powershell", "dart", "objective-c", "objc", "groovy", 
    "elixir", "clojure", "f#", "assembly", "asm", "julia", "fortran", 
    "cobol", "erlang", "lua", "vba", "pl/sql", "plsql",

    # Web Development Frameworks and Variations
    "django", "flask", "node.js", "nodejs", "node", "express", "spring", 
    "laravel", "rails", "ruby on rails", "asp.net", "angular", "angularjs", 
    "react", "reactjs", "vue", "vuejs", "svelte", "next.js", "nextjs", 
    "nuxt.js", "nuxtjs", "bootstrap", "tailwind", "material-ui", "mui", 
    "graphql", "redux",

    # Databases and Variations
    "mysql", "sql", "postgresql", "postgres", "mongo", "mongodb", 
    "sqlite", "oracle", "redis", "cassandra", "elasticsearch", 
    "elastic search", "couchdb", "dynamodb", "sql server", 
    "firebase", "hbase", "neo4j", "bigquery", "clickhouse", 
    "redshift", "snowflake",

    # DevOps Tools and Variations
    "docker", "kubernetes", "k8s", "terraform", "cloudformation" "ansible", "puppet", 
    "chef", "jenkins", "git", "github", "github actions", 
    "bitbucket", "bitbucket pipelines", "teamcity", "circleci", 
    "travis ci", "nagios", "prometheus", "grafana", "splunk", 
    "new relic",

    # Cloud Platforms and Variations
    "aws", "amazon web services", "azure", "gcp", "google cloud platform", 
    "heroku", "digitalocean", "cloudflare", "openstack", "vmware", "kafka",

    # Other Tools and Technologies with Variations
    "linux", "windows", "macos", "mac os", "nosql", "apache", "nginx", 
    "webpack", "babel", "eslint", "prettier", "yarn", "npm", "pnpm", 
    "vagrant", "virtualbox", "unity", "unreal engine", "ue", "opencv", 
    "tensorflow", "keras", "pytorch", "torch", "scikit-learn", 
    "hadoop", "spark", "airflow"
]

# Soft skills list
SOFT_SKILLS = [
    "communication", "teamwork", "leadership", "problem-solving", 
    "critical thinking", "adaptability", "creativity", "time management",
    "interpersonal skills", "collaboration", "emotional intelligence", 
    "work ethic", "conflict resolution", "decision making", 
    "self-motivation", "organization", "resilience", "flexibility"
]
# Buzzwords
BUZZWORDS = [
    "agile", "scrum", "microservices", "data-driven", "cross-functional", 
    "continuous delivery", "cloud-native", "scalability", "devops"
]

# Education levels
EDUCATION_REQUIREMENTS = [
    "bachelor's degree", "master's degree", "phd", "diploma", "high school"
]

# User profile
PROFILE = {
    "tech_skills": [
        # Programming Languages
        "python", "bash", "c#", "c++", "groovy", "java", "jquery", "json",
        "mongo", "mysql", "node", "php", "postgresql", "powershell", 
        "react", "typescript",

        # Web Frameworks
        "symfony", "reactjs", "node.js", "express", "django", "flask",

        # DevOps and Tools
        "aws", "docker", "linux", "jenkins", "terraform", "cloudformation", 
        "git", "github actions", "bitbucket pipelines", "teamcity", "spacelift", 
        "serverless",

        # Databases
        "mongodb", "mysql", "mariadb", "postgresql", "elasticsearch",

        # Miscellaneous
        "npm", "swagger", "vagrant", "elasticsearch"
    ],
    "soft_skills": [
        "communication", "teamwork", "adaptability", "problem-solving", 
        "critical thinking", "leadership", "creativity", "time management", 
        "collaboration", "decision making", "resilience", "self-motivation", 
        "organization", "flexibility"
    ],
    "experience_years": 7, 
    "education": "bachelor's degree",
    "location": "london"
}


@app.after_request
def apply_cors(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

@app.route('/match', methods=['POST'])
def match_skills():
    data = request.json
    job_description = data.get('job_description', '').lower()
    words = re.findall(r'\b\w+\b', job_description)
    
    # Job skill extraction
    job_tech_skills = {word for word in words if word in TECH_SKILLS}
    job_soft_skills = {word for word in words if word in SOFT_SKILLS}
    job_buzzwords = {word for word in words if word in BUZZWORDS}
    matched_education = [req for req in EDUCATION_REQUIREMENTS if req in job_description]
    
    # Normalize user profile skills
    normalized_tech_skills = set(skill.lower() for skill in PROFILE["tech_skills"])
    normalized_soft_skills = set(skill.lower() for skill in PROFILE["soft_skills"])
    
    # Skill matching
    matched_tech_skills = job_tech_skills.intersection(normalized_tech_skills)
    missing_tech_skills = job_tech_skills - normalized_tech_skills
    matched_soft_skills = job_soft_skills.intersection(normalized_soft_skills)
    missing_soft_skills = job_soft_skills - normalized_soft_skills
    
    # Scoring logic
    total_tech_skills = len(job_tech_skills)
    total_soft_skills = len(job_soft_skills)
    total_buzzwords = len(job_buzzwords)

    # Calculate technical match score
    if total_tech_skills > 0:
        tech_score = (len(matched_tech_skills) / total_tech_skills) * 100
    else:
        tech_score = 0

    # Adjust weights dynamically
    soft_skills_weight = 20 if total_soft_skills > 0 else 0
    education_weight = 10 if "education" in job_description else 0
    tech_weight = 100 - soft_skills_weight - education_weight

    # Soft skills match score
    soft_skills_score = (len(matched_soft_skills) / total_soft_skills * soft_skills_weight) if total_soft_skills else 0
    
    # Education match score
    education_score = education_weight if PROFILE["education"] in matched_education else 0

    # Combine scores
    match_score = (tech_score * (tech_weight / 100)) + soft_skills_score + education_score

    # Guarantee 100% match if all tech skills are present
    if len(missing_tech_skills) == 0 and total_tech_skills > 0:
        match_score = 100

    return jsonify({
        "match_percentage": f"{match_score:.2f}%",
        "matched_tech_skills": list(matched_tech_skills),
        "missing_tech_skills": list(missing_tech_skills),
        "matched_soft_skills": list(matched_soft_skills),
        "missing_soft_skills": list(missing_soft_skills),
        "matched_buzzwords": list(job_buzzwords),
        "education_match": PROFILE["education"] in matched_education
    })



if Mangum:
    handler = Mangum(app)

if __name__ == '__main__':
    app.run(debug=True)
