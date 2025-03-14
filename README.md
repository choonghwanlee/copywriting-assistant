# Copywriting Assistant

Demo app of enterprise copywriting assistant, built using Amazon Bedrock & FastAPI.

## Week 5 submission:

Requirements:

- Working API service
- API Documentation
- Security Measures
- Usage metrics

### API Documentation

#### 1. **POST** `/generate_social_media_ad`

Generates a social media ad caption based on the given product details (max 128 tokens)

##### **Request Body**

```json
{
  "product_description": "string",
  "competitive_advantage": "string",
  "price": "string"
}
```

##### **Response**

```json
{
  "social_media_ad": "Generated ad content here"
}
```

#### 2. **POST** `/generate_blog_post`

Creates a blog post based on the provided product details (max 2048 tokens)

##### **Request Body**

```json
{
  "product_description": "string",
  "competitive_advantage": "string",
  "price": "string"
}
```

##### **Response**

```json
{
  "blog_post": "Generated blog post here"
}
```

#### 3. **POST** `/generate_email_campaign`

Creates an email campaign based on the provided product details (max 512 tokens)

##### **Request Body**

```json
{
  "product_description": "string",
  "competitive_advantage": "string",
  "price": "string"
}
```

##### **Response**

```json
{
  "email_campaign": "Generated email campaign content here"
}
```

### Error Handling

- The API checks for harmful words in user inputs and rejects requests containing inappropriate content with a 400 status.
- Any internal server errors return a 500 status with an error message.

### Usage Logging

- We monitor API usage, specifically # request and request latency, by adding a monitoring middleware to the FastAPI application.
- This middleware then pushes metrics like # requests and latency to AWS CloudWatch where I can monitor metrics from a dashboard

### Security

- Use of Pydantic data model to validate input format prevents naive SQL attacks/injections.
- JWT-based token authentication required on text generation API; limits access to only "logged in" users
