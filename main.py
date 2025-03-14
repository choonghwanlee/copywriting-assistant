from fastapi import FastAPI, HTTPException, Body, Depends
from pydantic import BaseModel
import boto3
import json
import re
from monitoring import MonitoringMiddleware

from prompts import blog_post_prompt, social_media_prompt, email_campaign_prompt
from filters import harmful_words_to_filter
from auth import sign_jwt, UserSchema, UserLoginSchema, JWTBearer, check_user, users


app = FastAPI()
app.add_middleware(MonitoringMiddleware)

# Initalize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2', 
)

class PromptRequest(BaseModel):
    product_description: str
    competitive_advantage: str
    price: str

# Function to check for harmful words
def contains_harmful_words(text: str):
    text_lower = text.lower()
    return any(re.search(rf"\b{word}\b", text_lower) for word in harmful_words_to_filter)


def format_llama(system: str, user: str):
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

def invoke_llama(system_prompt: str, user_prompt: str, max_len: int):
    body = {
        "prompt": format_llama(system_prompt, user_prompt),
        "max_gen_len": max_len,
        "top_p": 0.9,
        "temperature": 0.1,
    }
    model_id = "meta.llama3-1-70b-instruct-v1:0"
    response = bedrock.invoke_model(
        contentType='application/json',
        modelId=model_id,
        body=json.dumps(body)
    )
    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["generation"]
    return response_text

@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.post("/generate_social_media_ad", dependencies=[Depends(JWTBearer())])
async def generate_social_media_ad(request: PromptRequest):
    try:
        system_prompt = """You are a social media marketing expert helping a company create social media ads for their products."""
        user_prompt = social_media_prompt.format(product_description=request.product_description, competitive_advantage=request.competitive_advantage, price=request.price)
        if contains_harmful_words(user_prompt):
            raise HTTPException(status_code=400, detail="Input contains harmful content")
        max_len = 128
        response_text = invoke_llama(system_prompt, user_prompt, max_len)
        return {"social_media_ad": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_blog_post", dependencies=[Depends(JWTBearer())])
async def generate_blog_post(request: PromptRequest):
    try:
        system_prompt = """You are a content marketing expert helping a company create blog posts for their product."""
        user_prompt = blog_post_prompt.format(product_description=request.product_description, competitive_advantage=request.competitive_advantage, price=request.price)
        if contains_harmful_words(user_prompt):
            raise HTTPException(status_code=400, detail="Input contains harmful content")
        max_len = 2048
        response_text = invoke_llama(system_prompt, user_prompt, max_len)
        return {"blog_post": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate_email_campaign", dependencies=[Depends(JWTBearer())])
async def generate_email_campaign(request: PromptRequest):
    try:
        system_prompt = """You are an email marketing expert helping a company create email campaigns for their product."""
        user_prompt = email_campaign_prompt.format(product_description=request.product_description, competitive_advantage=request.competitive_advantage, price=request.price)
        if contains_harmful_words(user_prompt):
            raise HTTPException(status_code=400, detail="Input contains harmful content")
        max_len = 512
        response_text = invoke_llama(system_prompt, user_prompt, max_len)
        return {"email_campaign": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/user/signup")
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return sign_jwt(user.email)

@app.post("/user/login")
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return sign_jwt(user.email)
    return {
        "error": "Wrong login details!"
    }
