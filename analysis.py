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
    Analyzes content from scraped websites using simple keyword matching heuristics.
    Counts mentions of known AI tools (defined in COMMON_AI_TOOLS) to determine popularity nearby.
    
    Args:
        scraped_results (list): A list of dictionaries containing 'content' from scraped pages.
        
    Returns:
        list: A list of tuples (tool_name, count) sorted by frequency in descending order.
    """
    tool_counts = Counter()
    
    # Concatenate all scraped content into one large text block for analysis
    combined_text = ""
    for res in scraped_results:
        if 'content' in res:
            combined_text += res['content'] + "\n"
            
    # Normalize text to lowercase for case-insensitive matching
    text_lower = combined_text.lower()
    
    # Iterate through the predefined list of common AI tools
    for tool in COMMON_AI_TOOLS:
        # Create a regex pattern to match the tool name as a whole word
        # \b ensures we don't match partial words (e.g., "gem" for "Gemini")
        pattern = r'\b' + re.escape(tool.lower()) + r'\b'
        matches = re.findall(pattern, text_lower)
        count = len(matches)
        
        # If the tool is mentioned, record the count
        if count > 0:
            tool_counts[tool] = count
            
    # Return the most frequently mentioned tools first
    sorted_tools = tool_counts.most_common()
    
    return sorted_tools

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def analyze_content_llm(scraped_results, query):
    """
    Analyzes scraped content using OpenAI's GPT model (representing 'The Council').
    Synthesizes information from multiple sources to answer a specific user query.
    
    Args:
        scraped_results (list): List of scraped page data.
        query (str): The user's original question.
        
    Returns:
        dict: Contains 'analysis' (the LLM's answer) or 'error'.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "No API key found"}

    client = OpenAI(api_key=api_key)

    # 1. Construct the context for the LLM
    # Aggregate content from the top search results
    context = ""
    for i, res in enumerate(scraped_results):
        context += f"--- Source {i+1}: {res.get('title', 'Unknown')} ---\n"
        context += f"URL: {res.get('url', 'Unknown')}\n"
        # Truncate content to roughly 2000 chars to save tokens and fit in context window
        content = res.get('content', '')[:2000] 
        context += f"Content: {content}\n\n"

    # 2. Define the System Persona
    # The 'Council' is an expert advisory board for SMEs
    system_prompt = (
        "You are the 'KMUmeetKI Council', an expert AI advisory board for SMEs. "
        "Your goal is to analyze the provided search results and answer the user's query "
        "with practical, actionable advice. "
        "Identify the best tools or strategies mentioned. "
        "Structure your response clearly with markdown."
    )

    # 3. Define the User Task
    user_prompt = (
        f"User Query: {query}\n\n"
        f"Based on the following search results, provide a comprehensive answer.\n\n"
        f"{context}"
    )

    try:
        # 4. Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using a cost-effective model (GPT-4o Mini)
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7 # Slight creativity allowed
        )
        return {"analysis": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}


def extract_tool_names(scraped_results, department):
    """
    Extracts structured AI tool data from unstructured web content using an LLM.
    Used to populate the Research Assistant's database with new candidates.
    
    Args:
        scraped_results (list): Raw search results.
        department (str): The department context (e.g., "Marketing") to verify relevance.
        
    Returns:
        list: A list of dicts, each containing 'tool_name' and 'description'.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return []

    client = OpenAI(api_key=api_key)

    # Prepare context
    context = ""
    for i, res in enumerate(scraped_results):
        context += f"--- Page {i+1} ---\n"
        context += f"Title: {res.get('title', 'Unknown')}\n"
        context += f"URL: {res.get('url', 'Unknown')}\n"
        content = res.get('content', '')[:1500]
        context += f"Content: {content}\n\n"

    # Strict system instruction to ensure clean data extraction
    system_prompt = (
        "You are an AI tool researcher. Extract the names of specific AI tools mentioned in the content. "
        "Focus on actual product/tool names (like ChatGPT, Jasper, HubSpot, Salesforce Einstein, etc.), "
        "not generic terms like 'AI' or 'machine learning'. "
        "For each tool, provide a one-line description of what it does."
    )

    # Prompt requesting a specific pipe-delimited format for easy parsing
    user_prompt = (
        f"Department context: {department}\n\n"
        f"Extract AI tool names from this content:\n\n{context}\n\n"
        "Return the tools in this exact format (one per line):\n"
        "TOOL: [Tool Name] | DESC: [Brief description]\n"
        "Only return real, specific tool names. Maximum 5 tools."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3 # Lower temperature for more deterministic/factual output
        )
        
        # Parse the structured response
        text = response.choices[0].message.content
        tools = []
        
        for line in text.split('\n'):
            if 'TOOL:' in line and '|' in line:
                # Basic string parsing based on the requested format
                parts = line.split('|')
                tool_name = parts[0].replace('TOOL:', '').strip()
                description = parts[1].replace('DESC:', '').strip() if len(parts) > 1 else ''
                
                # Sanity check: Ignore empty or overly long garbage names
                if tool_name and len(tool_name) < 60:
                    tools.append({
                        'tool_name': tool_name,
                        'description': description
                    })
        
        return tools
    except Exception as e:
        print(f"⚠️ Tool extraction failed: {e}")
        return []

from huggingface_hub import InferenceClient

def validate_with_apertus(council_analysis, query):
    """
    Validates the Council's analysis using the Swiss AI 'Apertus' model.
    This provides a 'second opinion' with a focus on Swiss context and neutrality.
    
    Args:
        council_analysis (str): The output from the primary LLM analysis.
        query (str): The original user query.
        
    Returns:
        dict: 'validation' string or 'error' message.
    """
    # Use the free Hugging Face Inference API (rate limits apply)
    # Ideally, the user should provide a HF_TOKEN in .env
    hf_token = os.getenv("HF_TOKEN")
    
    # Model ID for the Swiss 'Apertus' model
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
        # Apertus uses a specific chat template, but InferenceClient handles chat completion generally.
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
