from pydantic import BaseModel
from llama_cpp import Llama
from fastapi import FastAPI, HTTPException, Body, Depends
import redis
import hashlib
import json

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

app = FastAPI()

social_media_prompt = """Below is information about the company's product.
Product Description: {product_description}
Competitive Advantage: {competitive_advantage}
Price: {price}

You may also be given an image of the product for reference.

Using the image and information provided, create a short, compelling social media ad caption that is catchy and has a clear call to action (i.e. subscribe to newsletter, find out more, buy now). Include just the generated ad caption, and nothing else."""

blog_post_prompt = """Below is information about the company's product.
Product Description: {product_description}
Competitive Advantage: {competitive_advantage}
Price: {price}

You may also be given an image of the product for reference.

Using the image and information provided, create a blog post that naturally & indirectly markets the product. Include just the generated blog post, and nothing else."""

email_campaign_prompt = """Below is information about the company's product.
Product Description: {product_description}
Competitive Advantage: {competitive_advantage}
Price: {price}

You may also be given an image of the product for reference.

Using the image and information provided, create a catchy email campaign that hooks potential buyers into buying a product or clicking into the company's website. Include just the generated email campaign, and nothing else."""

# Initalize Llama.CPP client
llm = Llama.from_pretrained(
  repo_id="Qwen/Qwen2.5-1.5B-Instruct-GGUF",
  filename="qwen2.5-1.5b-instruct-q8_0.gguf",
  chat_format="qwen",
)

def converse_qwen(system_prompt: str, user_content: str, max_len: int):
    response = llm.create_chat_completion(
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_content
            }
        ],
        temperature=0.1,
        top_p=0.9,
        max_tokens=max_len
    )
    return response['choices'][0]['message']['content']

class PromptRequest(BaseModel):
    product_description: str
    competitive_advantage: str
    price: str

@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.post("/generate_social_media_ad")
async def generate_social_media_ad(request: PromptRequest):
    try:
        cache_key = hashlib.sha256(json.dumps(request.dict(), sort_keys=True).encode()).hexdigest()

        # Check if the result is already in the cache
        cached_result = r.get(cache_key)
        if cached_result:
            # If cache hit, return the cached response
            return {"social_media_ad": cached_result}

        system_prompt = """You are a social media marketing expert helping a company create social media ads for their products."""
        user_prompt = social_media_prompt.format(product_description=request.product_description, competitive_advantage=request.competitive_advantage, price=request.price)
        max_len = 128
        response_text = converse_qwen(system_prompt, user_prompt, max_len)
        r.setex(cache_key, 3600, response_text)
        return {"social_media_ad": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate_blog_post")
async def generate_blog_post(request: PromptRequest):
    try:
        cache_key = hashlib.sha256(json.dumps(request.dict(), sort_keys=True).encode()).hexdigest()

        # Check if the result is already in the cache
        cached_result = r.get(cache_key)
        if cached_result:
            # If cache hit, return the cached response
            return {"blog_post": cached_result}

        system_prompt = """You are a content marketing expert helping a company create blog posts for their product."""
        user_prompt = blog_post_prompt.format(product_description=request.product_description, competitive_advantage=request.competitive_advantage, price=request.price)
        max_len = 2048
        response_text = converse_qwen(system_prompt, user_prompt, max_len)
        r.setex(cache_key, 3600, response_text)

        return {"blog_post": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_email_campaign")
async def generate_email_campaign(request: PromptRequest):
    try:
        cache_key = hashlib.sha256(json.dumps(request.dict(), sort_keys=True).encode()).hexdigest()

        # Check if the result is already in the cache
        cached_result = r.get(cache_key)
        if cached_result:
            # If cache hit, return the cached response
            return {"blog_post": cached_result}

        system_prompt = """You are an email marketing expert helping a company create email campaigns for their product."""
        user_prompt = email_campaign_prompt.format(product_description=request.product_description, competitive_advantage=request.competitive_advantage, price=request.price)
        max_len = 512
        response_text = converse_qwen(system_prompt, user_prompt, max_len)
        r.setex(cache_key, 3600, response_text)
        return {"email_campaign": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))