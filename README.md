# Copywriting Assistant

Demo app of enterprise copywriting assistant, built using Amazon Bedrock & FastAPI.

## Week 6 submission:

Requirements:

- Working service with image and text processing
- Architecture documentation
- Performance Analysis
- Deployment Guide

### API Service

We expand on Week 5's work by first adding multi-modal support for user image upload, then deploying the app via AWS Lambda for high scalability & availability. Now, users can not only add text descriptions of a product but also add reference images

Specifically, we refactored the FastAPI endpoints to take multipart form data as input instead of a Pydantic object. This allows users to upload an image from their local directory as input to the POST requests. In addition, we make images optional, maintaining backwards compatibility with Week 5.

### Deployment Guide

To deploy the app to AWS Lambda, follow the following instructons.

##### 1. Create a zip file of repository content

First, run the following command:

`pip3 install -t dependencies -r requirements.txt --platform manylinux2014_x86_64 --python-version 3.12 --only-binary=:all:`

This creates a new folder called `dependencies` with all the dependencies installed. We specify platform to x86_64 to ensure it is consistent with AWS Lambda architecture.

`(cd dependencies; zip ../aws_lambda_artifact.zip -r .)`

This will zip the dependencies into a zip file called `aws_lambda_artifact.zip`. To this, we add our python files with the following comands:

`zip aws_lambda_artifact.zip -u NAME_OF_FILE.py`, where NAME_OF_FILE refers to a .py file in our directory.

##### 2. Create a new AWS Lambda Function

In the AWS Lambda console, create a new function. Change the runtime to your Python runtime (in my case, it was Python 3.12), and under Additional Configurations, 'Enable Function URL' then set Auth type to NONE.

After pressing 'Create function', a new AWS Lambda function will be created.

Change the handler from the default value to `main.handler`, specifying the filename and variable name of our Mangum handler.

##### 3. Upload zip file to AWS Lambda Function

Finally, under 'Code Source', select upload from .zip file and upload the `aws_lambda_artifact.zip` you created in Step 1. This will load our repository into AWS Lambda

Finally, in the 'ENVIRONMENT VARIABLES' section of the built-in IDE, add a new environment variable for the `JWT_SECRET` key that we use for authentication/hashing.

You can now test the app as follows:

Create a new account:

```bash
curl -X POST "YOUR_FUNCTION_URL/user/signup" \
 -H "Content-Type: application/json" \
 -d '{
 "fullname": "Jason Lee",
 "email": "jasonlee@gmail.com",
"password": "aweakpassword"
}
```

This will return a 'access_token' variable. Use this in the Authorization Bearer of any POST request:

```bash
curl -X POST "YOUR_FUNCTION_URL/generate_social_media_ad" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -F "product_description=Eco-friendly water bottle made from bamboo" \
  -F "competitive_advantage=Biodegradable, stylish, and keeps drinks cold for 24 hours" \
  -F "price=$29.99" \
  -F "image=@/path/to/image.jpg"
```

### Performance Analysis

AWS Lambda has built-in integration with AWS CloudWatch and AWS X-Ray, allowing us to easily monitor the performance of our application.

This includes latency of each function call, total concurrent executions, error %, and a running log of each invocation.

Our service has relatively low latency, with an average of roughly 700ms per invocation / request.
