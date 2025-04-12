from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import re
from monitoring import MonitoringMiddleware
from mangum import Mangum
import base64
import json
from logger import logger
from dotenv import load_dotenv
import os


from prompts import blog_post_prompt, social_media_prompt, email_campaign_prompt
from auth import sign_jwt, UserSchema, UserLoginSchema, JWTBearer, check_user, users
from model import converse_llama

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://copywriter-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)

guardrailConfig = {
    "guardrailIdentifier": os.getenv('GUARDRAIL_ID'),
    "guardrailVersion": '3', 
    "trace": "enabled"
}    

def get_valid_image_format(content_type: str) -> str:
    # Map MIME types to accepted formats
    format_mapping = {
        'image/jpeg': 'jpeg',
        'image/jpg': 'jpeg',
        'image/png': 'png',
        'image/gif': 'gif',
        'image/webp': 'webp'
    }
    return format_mapping.get(content_type.lower())


@app.get("/")
async def hello():
    return {"message": "Hello World"}

@app.post("/generate_social_media_ad", dependencies=[Depends(JWTBearer())])
async def generate_social_media_ad(
    product_description: str = Form(...),
    competitive_advantage: str = Form(...),
    price: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    logger.info("Received request to generate social media ad.")
    try:
        system_prompt = """You are a social media marketing expert helping a company create social media ads for their products."""
        user_prompt = social_media_prompt.format(product_description=product_description, competitive_advantage=competitive_advantage, price=price)
        max_len = 128
        user_content = []
        if image:
            image_bytes = await image.read()
            if len(image_bytes) == 0:
                raise HTTPException(status_code=400, detail="Image is empty or failed to decode")
            user_content.append({"image": {"format": get_valid_image_format(image.content_type), "source": {"bytes":image_bytes}}})
        user_content.append({"text": user_prompt})
        response = converse_llama(system_prompt, user_content, max_len, guardrailConfig)
        response_text = response['output']['message']['content'][0]['text']
        if response['stopReason'] == "guardrail_intervened":
            trace = response['trace']
            logger.warning(f"Guardrail intervened in response generation: {json.dumps(trace['guardrail'], indent=4)}")
        if isinstance(response_text, dict) and "error" in response_text:
            raise HTTPException(status_code=500, detail=response_text["error"])
        logger.info("Successfully generated social media ad.")
        return {"social_media_ad": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_blog_post", dependencies=[Depends(JWTBearer())])
async def generate_blog_post(
    product_description: str = Form(...),
    competitive_advantage: str = Form(...),
    price: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    logger.info("Received request to generate blog post.")
    try:
        system_prompt = """You are a content marketing expert helping a company create blog posts for their product."""
        user_prompt = blog_post_prompt.format(product_description=product_description, competitive_advantage=competitive_advantage, price=price)
        max_len = 2048
        user_content = []
        if image:
            image_bytes = await image.read()
            if len(image_bytes) == 0:
                raise HTTPException(status_code=400, detail="Image is empty or failed to decode")
            user_content.append({"image": {"format": get_valid_image_format(image.content_type), "source": {"bytes":image_bytes}}})
        user_content.append({"text": user_prompt})
        response = converse_llama(system_prompt, user_content, max_len, guardrailConfig)
        response_text = response['output']['message']['content'][0]['text']
        if response['stopReason'] == "guardrail_intervened":
            trace = response['trace']
            logger.warning(f"Guardrail intervened in response generation: {json.dumps(trace['guardrail'], indent=4)}")
        if isinstance(response_text, dict) and "error" in response_text:
            raise HTTPException(status_code=500, detail=response_text["error"])
        logger.info("Successfully generated blog post.")
        return {"blog_post": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate_email_campaign", dependencies=[Depends(JWTBearer())])
async def generate_email_campaign(
    product_description: str = Form(...),
    competitive_advantage: str = Form(...),
    price: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    try:
        system_prompt = """You are an email marketing expert helping a company create email campaigns for their product."""
        user_prompt = email_campaign_prompt.format(product_description=product_description, competitive_advantage=competitive_advantage, price=price)
        max_len = 512
        user_content = []
        if image:
            image_bytes = await image.read()
            if len(image_bytes) == 0:
                raise HTTPException(status_code=400, detail="Image is empty or failed to decode")
            user_content.append({"image": {"format": get_valid_image_format(image.content_type), "source": {"bytes":image_bytes}}})
        user_content.append({"text": user_prompt})
        response = converse_llama(system_prompt, user_content, max_len, guardrailConfig)
        response_text = response['output']['message']['content'][0]['text']
        if response['stopReason'] == "guardrail_intervened":
            trace = response['trace']
            print("Guardrail trace:")
            print(json.dumps(trace['guardrail'], indent=4))
            logger.warning(f"Guardrail intervened in response generation: {json.dumps(trace['guardrail'], indent=4)}")
        if isinstance(response_text, dict) and "error" in response_text:
            raise HTTPException(status_code=500, detail=response_text["error"])
        logger.info("Successfully generated email campaign.")
        return {"email_campaign": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/user/signup")
async def create_user(
    fullname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    user = UserSchema(fullname=fullname, email=email, password=password)
    users.append(user)
    return sign_jwt(user.email)

@app.post("/user/login")
async def user_login(
    email: str = Form(...),
    password: str = Form(...)
):
    logger.info("Login attempt", extra={"email": email})
    user = UserLoginSchema(email=email, password=password)
    if check_user(user):
        logger.info("Login successful", extra={"email": email})
        return sign_jwt(user.email)
    logger.warning("Login failed", extra={"email": email})
    return {
        "error": "Wrong login details!"
    }


