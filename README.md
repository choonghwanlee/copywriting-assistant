# Copywriting Assistant

Demo app of enterprise copywriting assistant, built using Amazon Bedrock & FastAPI.

## Week 9 submission:

Deliverables:

Complete application (with frontend, authentication, backend)
Architecture document
User guide
Security documentation

### Architecture Document

1. Frontend: NextJS, hosted via Vercel
2. Backend: FastAPI/AWS Lambda, hosted via AWS API Gateway
3. LLM Usage: Amazon Bedrock (Multimodal Llama3.2)
4. User Auth: JWT Tokens
5. Monitoring: AWS CloudWatch

We did NOT build a separate database for this application. This means that results and user accounts are not persistent across sessions. Please keep this in mind as you use the app!

### User Guide

Users can access the app via https://copywriter-app.vercel.app/, which directs them to a landing page where they can learn more.

They can then sign up or log in via our user authentication system. We gracefully handle errors such as mismatching passwords, missing fields, any server-side errors, etc.

Users are then redirected to the main dashboard. Here, they can either generate a new marketing copy (i.e. social media ad, blog post, etc.) by entering the product name, price, description, competitive advantage, and optionally a product image. For seamless user workflow, warnings are triggered + the submit button is disabled when mandatory fields are left blank or uploaded images exceed the max size of our Bedrock API.

After submitting their request, users will receive a custom copy of their choice within a few seconds, which they can copy to clipboard or download as a .txt file.

Users can also see past copies that they generated for later access. Again, this is not persistent by design so it'll go away with a hard refresh or new session.

### Security Documentation

We use JWT to authenticate our 3 AWS Bedrock API endpoints. JWT tokens are generated on successful user sign-up / log-in and last ~15 minutes, after which the token expires and users would need to log in again to refresh their token. This means that no one can access our APIs outside of the app's workflow, preventing security breaches and attacks. In addition, we enable CORS on our endpoints, allowing just the app's URL as the origin. This means that adversarial attackers cannot remotely exploit the login or signup API endpoints to obtain a JWT token.
