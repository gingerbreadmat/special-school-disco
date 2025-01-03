import json
import boto3
import logging
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

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
        job_description = body.get('job_description', 'No description provided')
        logger.info(f"Job Description: {job_description}")
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing request body: {str(e)}")
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps({'error': 'Invalid request body'})
        }
    
    random_score = random.randint(60, 100)
    
    result = {
        'score': f'{random_score}%',
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
    existing_data.append({
        'score': f'{random_score}%',
    })
    
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
