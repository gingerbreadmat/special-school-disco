#!/bin/bash

# Check if logged in to the correct account
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

if [ "$ACCOUNT_ID" != "507844679777" ]; then
    echo "Error: You are not logged into the correct AWS account. Expected account ID: 507844679777, but got $ACCOUNT_ID."
    exit 1
fi

echo "Logged into the correct AWS account: $ACCOUNT_ID"

# Sync the current bucket to the backup bucket
echo "Backing up files from gingerbreadmat.com to gingerbread-cv..."
aws s3 sync s3://gingerbreadmat.com s3://gingerbread-cv

# Create an array of files to upload
FILES=("base.html" "cv.pdf" "script.js" "styles.css")

# Loop through the files and upload them
echo "Uploading files to gingerbreadmat.com..."
for FILE in "${FILES[@]}"; do
    if [ -f "$FILE" ]; then
        aws s3 cp "$FILE" s3://gingerbreadmat.com/
        echo "Uploaded $FILE"
    else
        echo "Warning: File $FILE does not exist. Skipping."
    fi
done

echo "All operations completed successfully."
