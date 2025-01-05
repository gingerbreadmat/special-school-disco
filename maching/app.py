import json
import boto3
import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

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
    "graphql", "redux", "symfony",

    # Databases and Variations
    "mysql", "sql", "postgresql", "postgres", "mongo", "mongodb", 
    "sqlite", "oracle", "redis", "cassandra", "elasticsearch", 
    "elastic search", "couchdb", "dynamodb", "sql server", 
    "firebase", "hbase", "neo4j", "bigquery", "clickhouse", 
    "redshift", "snowflake", "mariadb",

    # DevOps Tools and Variations
    "docker", "kubernetes", "k8s", "terraform", "cloudformation", "ansible", 
    "puppet", "chef", "jenkins", "git", "github", "github actions", 
    "bitbucket", "bitbucket pipelines", "teamcity", "circleci", 
    "travis ci", "nagios", "prometheus", "grafana", "splunk", 
    "new relic", "spacelift", "serverless", "grafana loki", 
    "aws cloudwatch", "datadog", "appdynamics", "postman", 
    "nginx", "apache", "kafka", "consul",

    # Cloud Platforms and Variations
    "aws", "amazon web services", "azure", "gcp", "google cloud platform", 
    "heroku", "digitalocean", "cloudflare", "openstack", "vmware",

    # Other Tools and Technologies with Variations
    "linux", "windows", "macos", "mac os", "nosql", "webpack", "babel", 
    "eslint", "prettier", "yarn", "npm", "pnpm", "vagrant", 
    "virtualbox", "unity", "unreal engine", "ue", "opencv", 
    "tensorflow", "keras", "pytorch", "torch", "scikit-learn", 
    "hadoop", "spark", "airflow", "drupal"
]


# Soft skills list
SOFT_SKILLS = [
    "communication", "teamwork", "leadership", "problem-solving", 
    "critical thinking", "adaptability", "creativity", "time management",
    "interpersonal skills", "collaboration", "emotional intelligence", 
    "work ethic", "conflict resolution", "decision making", 
    "self-motivation", "organization", "resilience", "flexibility", 
    "reliability", "empathy", "planning", "prioritisation",
    "devops fundamentals", "ci/cd pipelines", "infrastructure as code (iac)",
    "microservices", "containerization", "orchestration", "monitoring",
    "logging", "incident response", "disaster recovery", "load balancing",
    "auto-scaling", "networking basics", "security best practices",
    "firewall configuration", "vulnerability scanning", "DevOps"
]


# User profile
PROFILE = {
    "tech_skills": [
        # Programming Languages
        "python", "bash", "c#", "c++", "groovy", "java", "jquery", "json",
        "mongo", "mysql", "node", "php", "postgresql", "powershell",
        "react", "typescript", "ruby", "go", "javascript", "r", "scala",

        # Web Frameworks
        "symfony", "reactjs", "node.js", "express", "django", "flask", "graphql",

        # DevOps and Tools
        "aws", "docker", "linux", "jenkins", "terraform", "cloudformation",
        "git", "github actions", "bitbucket pipelines", "teamcity", "spacelift",
        "serverless", "circleci", "grafana", "elk stack", "new relic",
        "appdynamics", "datadog", "nginx", "apache", "kafka", "redis",
        "cloudflare", "cloudfront", "grafana loki", "aws cloudwatch",
        "postman", "chef", "puppet", "vagrant",

        # Databases
        "mongodb", "mysql", "mariadb", "postgresql", "elasticsearch",
        "sqlite", "cassandra",

        # Miscellaneous
        "npm", "swagger", "vagrant", "drupal", "consul",

        # specialties
        "devops fundamentals", "ci/cd pipelines", "infrastructure as code (iac)",
        "microservices", "containerization", "orchestration", "monitoring",
        "logging", "incident response", "disaster recovery", "load balancing",
        "auto-scaling", "networking basics", "security best practices",
        "firewall configuration", "vulnerability scanning", "DevOps",
        # platforms
        "macos", "linux", "windows"
    ],
    "soft_skills": [
        "communication", "teamwork", "adaptability", "problem-solving",
        "critical thinking", "leadership", "creativity", "time management",
        "collaboration", "decision making", "resilience", "self-motivation",
        "organization", "flexibility", "reliability", "empathy", "planning",
        "prioritisation"
    ],
    "experience_years": 7,
    "education": "bachelor's degree",
    "location": "london",
}

def lambda_handler(event, context):
    cors_headers = {
        "Access-Control-Allow-Origin": "https://gingerbreadmat.com",
        "Access-Control-Allow-Methods": "OPTIONS,POST",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': 'CORS preflight successful'})
        }
    
    bucket_name = 'gingerbread-matching-ai'
    file_key = 'results.json'
    
    logger.info(f"Bucket Name: {bucket_name}")
    logger.info(f"File Key: {file_key}")
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        body = json.loads(event['body'])
        job_description = body.get('job_description', 'No description provided').lower()
        logger.info(f"Job Description: {job_description}")
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing request body: {str(e)}")
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps({'error': 'Invalid request body'})
        }
    
    words = re.findall(r'\b\w+\b', job_description)
    job_tech_skills = {word for word in words if word in TECH_SKILLS}
    job_soft_skills = {word for word in words if word in SOFT_SKILLS}
    
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

    # Calculate technical match score
    if total_tech_skills > 0:
        tech_score = (len(matched_tech_skills) / total_tech_skills) * 100
    else:
        tech_score = 0

    # Soft skills match score
    soft_skills_weight = 20 if total_soft_skills > 0 else 0
    tech_weight = 100 - soft_skills_weight

    soft_skills_score = (len(matched_soft_skills) / total_soft_skills * soft_skills_weight) if total_soft_skills else 0

    # Combine scores
    match_score = (tech_score * (tech_weight / 100)) + soft_skills_score

    # Guarantee 100% match if all tech skills are present
    if len(missing_tech_skills) == 0 and total_tech_skills > 0:
        match_score = 100
    
    result = {
        'score': f'{match_score:.2f}%'
    }
    
    try:
        logger.info("Fetching the existing JSON file from S3...")
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        existing_data = json.loads(file_content) if file_content.strip() else []
        logger.info(f"Existing data fetched successfully: {existing_data}")
    except s3.exceptions.NoSuchKey:
        logger.warning(f"File {file_key} does not exist. Initializing an empty list.")
        existing_data = []
    except json.JSONDecodeError:
        logger.error(f"File {file_key} contains invalid JSON. Initializing an empty list.")
        existing_data = []
    except Exception as e:
        logger.error(f"Error fetching file from S3: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': f'Error accessing S3: {str(e)}'})
        }
    
    logger.info("Updating the JSON data...")
    existing_data.append(result)
    
    try:
        logger.info("Saving the updated data back to S3...")
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=json.dumps(existing_data))
        logger.info("Data saved successfully.")
    except Exception as e:
        logger.error(f"Error writing file to S3: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': f'Error writing to S3: {str(e)}'})
        }
    
    logger.info("Returning the result to the client.")
    return {
        'statusCode': 200,
        'headers': cors_headers,
        'body': json.dumps(result)
    }