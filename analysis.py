import re
from collections import Counter

COMMON_AI_TOOLS = [
    "ChatGPT", "Jasper", "Copy.ai", "Midjourney", "DALL-E", "Stable Diffusion",
    "Claude", "Bard", "Gemini", "Llama", "Mistral", "Falcon", "Notion AI",
    "Grammarly", "Otter.ai", "Fireflies.ai", "Synthesia", "Descript", "Runway",
    "GitHub Copilot", "Tabnine", "Replit", "Hugging Face", "LangChain"
]

def analyze_content_heuristics(scraped_results):
    """
    Analyzes scraped content using simple heuristics to find mentioned tools.
    Returns a list of tools sorted by mention frequency.
    """
    tool_counts = Counter()
    
    combined_text = ""
    for res in scraped_results:
        if 'content' in res:
            combined_text += res['content'] + "\n"
            
    # Normalize text slightly but keep case for tool matching if needed, 
    # though case-insensitive matching is usually safer for counting.
    text_lower = combined_text.lower()
    
    for tool in COMMON_AI_TOOLS:
        # Simple regex to find whole words
        pattern = r'\b' + re.escape(tool.lower()) + r'\b'
        matches = re.findall(pattern, text_lower)
        count = len(matches)
        if count > 0:
            tool_counts[tool] = count
            
    # Sort by count descending
    sorted_tools = tool_counts.most_common()
    
    return sorted_tools

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def analyze_content_llm(scraped_results, query):
    """
    Analyzes scraped content using OpenAI's GPT model (The Council).
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "No API key found"}

    client = OpenAI(api_key=api_key)

    # Prepare context from results
    context = ""
    for i, res in enumerate(scraped_results):
        context += f"--- Source {i+1}: {res.get('title', 'Unknown')} ---\n"
        context += f"URL: {res.get('url', 'Unknown')}\n"
        # Limit content length to avoid token limits (rough truncation)
        content = res.get('content', '')[:2000] 
        context += f"Content: {content}\n\n"

    system_prompt = (
        "You are the 'KMUmeetKI Council', an expert AI advisory board for SMEs. "
        "Your goal is to analyze the provided search results and answer the user's query "
        "with practical, actionable advice. "
        "Identify the best tools or strategies mentioned. "
        "Structure your response clearly with markdown."
    )

    user_prompt = (
        f"User Query: {query}\n\n"
        f"Based on the following search results, provide a comprehensive answer.\n\n"
        f"{context}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using a cost-effective model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return {"analysis": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

from huggingface_hub import InferenceClient

def validate_with_apertus(council_analysis, query):
    """
    Validates the Council's analysis using the Swiss AI 'Apertus' model.
    """
    # Use the free Hugging Face Inference API (rate limits apply)
    # Ideally, the user should provide a HF_TOKEN in .env
    hf_token = os.getenv("HF_TOKEN")
    
    model_id = "swiss-ai/Apertus-8B-Instruct-2509"
    
    client = InferenceClient(model=model_id, token=hf_token)

    system_prompt = (
        "You are 'Apertus', a Swiss AI model designed for accuracy and neutrality. "
        "Your task is to review the provided analysis from an 'LLM Council' regarding a user's query. "
        "Validate the advice. Is it accurate? Is it relevant for a Swiss context (if applicable)? "
        "Are there missing Swiss-specific tools or regulations? "
        "Provide a concise second opinion."
    )

    user_prompt = (
        f"User Query: {query}\n\n"
        f"Council Analysis to Review:\n{council_analysis}\n\n"
        "Please provide your validation."
    )

    try:
        # Apertus uses a specific chat template, but InferenceClient handles chat completion usually.
        # If not, we might need to format it manually. Let's try chat completion first.
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return {"validation": response.choices[0].message.content}
    except Exception as e:
        return {"error": f"Apertus validation failed: {str(e)}"}
