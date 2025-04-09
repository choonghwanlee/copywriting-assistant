import boto3
import json

# Initalize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1', 
)

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

def converse_llama(system_prompt: str, user_content: list, max_len: int):
    try:
        response = bedrock.converse(
                modelId="us.meta.llama3-2-90b-instruct-v1:0",
                messages=[
                    {
                        'role': 'user',
                        'content': user_content
                    }
                ],
                system=[
                    {
                        'text': system_prompt
                    }
                ],
                inferenceConfig={
                    'maxTokens': max_len,
                    'temperature': 0.1,
                    'topP': 0.9
                }
            )
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": e}
    return response['output']['message']['content'][0]['text']