from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Body, Depends
from typing import Optional
import re
from monitoring import MonitoringMiddleware
from mangum import Mangum

from prompts import blog_post_prompt, social_media_prompt, email_campaign_prompt
from filters import harmful_words_to_filter
from auth import sign_jwt, UserSchema, UserLoginSchema, JWTBearer, check_user, users
from model import converse_llama

app = FastAPI()
handler = Mangum(app)

# Function to check for harmful words
def contains_harmful_words(text: str):
    text_lower = text.lower()
    return any(re.search(rf"\b{word}\b", text_lower) for word in harmful_words_to_filter)

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
    try:
        system_prompt = """You are a social media marketing expert helping a company create social media ads for their products."""
        user_prompt = social_media_prompt.format(product_description=product_description, competitive_advantage=competitive_advantage, price=price)
        if contains_harmful_words(user_prompt):
            raise HTTPException(status_code=400, detail="Input contains harmful content")
        max_len = 128
        user_content = []
        if image:
            image_bytes = await image.read()
            user_content.append({"image": {"format": get_valid_image_format(image.content_type), "source": {"bytes":image_bytes}}})
        user_content.append({"text": user_prompt})
        response_text = converse_llama(system_prompt, user_content, max_len)
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
    try:
        system_prompt = """You are a content marketing expert helping a company create blog posts for their product."""
        user_prompt = blog_post_prompt.format(product_description=product_description, competitive_advantage=competitive_advantage, price=price)
        if contains_harmful_words(user_prompt):
            raise HTTPException(status_code=400, detail="Input contains harmful content")
        max_len = 2048
        user_content = []
        if image:
            image_bytes = await image.read()
            user_content.append({"image": {"format": get_valid_image_format(image.content_type), "source": {"bytes":image_bytes}}})
        user_content.append({"text": user_prompt})
        response_text = converse_llama(system_prompt, user_prompt, max_len)
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
        if contains_harmful_words(user_prompt):
            raise HTTPException(status_code=400, detail="Input contains harmful content")
        max_len = 512
        user_content = []
        if image:
            image_bytes = await image.read()
            user_content.append({"image": {"format": get_valid_image_format(image.content_type), "source": {"bytes":image_bytes}}})
        user_content.append({"text": user_prompt})
        response_text = converse_llama(system_prompt, user_prompt, max_len)
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
