# Copywriting Assistant

Demo app of enterprise copywriting assistant, built using Llama-CPP-Python, FastAPI.

The `main` branch will contain the most up-to-date code. To find submissions for a specific week, please navigate to the respective branch.

## Week 8 submission:

We use the course's suggested approach of using a dedicated EC2 instance to run a GGUF-optimized LLM with Llama-CPP inference.

Project Requirements:

- Deploy open source LLM: Deployed a 8-bit quantized Qwen2.5-1.5B-Instruct model using Llama-CPP Python binding on an AWS EC2 instance
- Create API wrapper: Wrapped the LLM inference calls with FastAPI endpoints
- Implement caching: Caching with Redis allows us to save results from the past hour, allowing faster inference
- Document deployment process: see below

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

### Deployment Process & Usage

Step 1. Create an EC2 instance on AWS

- We used a standard Ubuntu AMI with a `c7g.2xlarge` instance type, which leverages AWS's high-performance AWS Graviton3 processors
- Under Security, configure inbound rules to include HTTPS/HTTP/SSH requests, and in addition, add Custom TCP rules for Redis and FastAPI API calls (ports **6379** and **8000**, respecitvely)
- Connect to the instance via SSH in your local VSCode environment: `ssh -i your-pem.pem ubuntu@ec2-your-ec2-ip.compute-1.amazonaws.com`

Step 2. Write `main.py`

- Use `nano main.py` to create/open the main FastAPI application (see the application code in the branch)
- We use Llama-CPP Python binding to 1. load an 8-bit quantized Qwen2.5-1.5B-Instruct from HuggingFace and 2. invoke a chat completion with the local LLM, adhering to the LLM's chat template
- We use Redis to cache requests
- Copy the new application code into the nano environment, and save/escape afterwards!

Step 3. Test the app

- To test the app, you can run the following command, using your EC2 IP address, to access the FastAPI endpoints:

```bash
curl -X POST "http://your-ec2-ip:8000/generate_social_media_ad" \
     -H "Content-Type: application/json" \
     -d '{
           "product_description": "A lightweight and stylish smartwatch with health tracking features.",
           "competitive_advantage": "Long battery life and real-time health monitoring.",
           "price": "$199"
         }'
```

### Performance Monitoring:

1. In your EC2 instance, run `htop`, `df-h`, or `nvidia-smi` to check the CPU, GPU, memory, and disk usage
2. You can check the Redis performance metrics by running `redis-cli info memory` and `redis-cli monitor`
