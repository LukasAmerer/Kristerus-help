"""
Local SLM (Small Language Model) Service.
This module handles the logic for retrieving, ranking, and presenting "approved" AI tools to the user.
It simulates an intelligent assistant by matching user questions against the description/metadata of known tools.

Key Features:
- Keyword extraction (German/English stop word removal).
- Text similarity scoring (using sequence matching).
- Relevance-based ranking of tools.
"""
from difflib import SequenceMatcher
import re
from db_cache import validated_results_manager


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate text similarity between two strings using Python's built-in SequenceMatcher.
    
    Args:
        text1 (str): First string.
        text2 (str): Second string.
        
    Returns:
        float: A ratio between 0.0 (no match) and 1.0 (perfect match).
    """
    text1 = text1.lower().strip()
    text2 = text2.lower().strip()
    return SequenceMatcher(None, text1, text2).ratio()


def extract_keywords(text: str) -> set:
    """
    Extract meaningful keywords from a given text string.
    Removes common "stop words" (the, and, und, der, etc.) to focus on content words.
    
    Args:
        text (str): The input text (e.g., user question or tool description).
        
    Returns:
        set: A set of unique keywords strings.
    """
    # Common German and English stop words to filter out
    # These words carry little semantic weight for matching purposes.
    stop_words = {
        'der', 'die', 'das', 'und', 'oder', 'für', 'mit', 'von', 'zu', 'in', 'auf', 'ist', 'sind',
        'ein', 'eine', 'einer', 'einem', 'einen', 'wie', 'was', 'wer', 'wo', 'wann', 'warum',
        'the', 'a', 'an', 'and', 'or', 'for', 'with', 'of', 'to', 'in', 'on', 'is', 'are',
        'how', 'what', 'who', 'where', 'when', 'why', 'can', 'could', 'would', 'should',
        'welche', 'welcher', 'welches', 'gibt', 'es', 'ich', 'sie', 'er', 'wir', 'ihr',
        'bitte', 'können', 'kann', 'werden', 'wurde', 'haben', 'hat', 'sein', 'bei', 'am',
        'tools', 'tool', 'ki', 'ai', 'beste', 'best', 'gut', 'good'
    }
    
    # Use Regex to isolate words, convert to lowercase
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter: Keep word if NOT in stop_words AND length > 2
    keywords = {w for w in words if w not in stop_words and len(w) > 2}
    
    return keywords


def score_tool_relevance(question: str, tool: dict) -> float:
    """
    Score how relevant a specific tool is to the user's question.
    Uses a hybrid approach of Keyword Overlap + String Similarity.
    
    Args:
        question (str): The user's query.
        tool (dict): The tool data object (must contain 'tool_name' and 'llm_analysis').
        
    Returns:
        float: A relevance score between 0.0 and 1.0.
    """
    # 1. Extract keywords from user question
    question_keywords = extract_keywords(question)
    
    # 2. Prepare tool text (Name + Description)
    tool_name = tool.get('tool_name', '')
    description = tool.get('llm_analysis', '')
    
    tool_text = f"{tool_name} {description}"
    tool_keywords = extract_keywords(tool_text)
    
    # 3. Calculate Keyword Score (Jaccard-like containment)
    # What % of the question's keywords appear in the tool's text?
    if question_keywords:
        common_keywords = question_keywords & tool_keywords
        keyword_score = len(common_keywords) / len(question_keywords)
    else:
        keyword_score = 0.5  # Neutral default if question has no meaningful keywords
    
    # 4. Calculate Name Similarity Score
    # Direct fuzzy match between the question and the tool name.
    # Helpful if user asks "What is Notion?"
    name_similarity = calculate_similarity(question, tool_name)
    
    # 5. Name Bonus
    # Extra points if the tool name appears literally in the question text.
    name_bonus = 0.3 if tool_name.lower() in question.lower() else 0
    
    # 6. Combined Weighted Score
    # Weights: 50% Keyword Match, 20% Name Similarity, + Bonuses
    relevance_score = (keyword_score * 0.5) + (name_similarity * 0.2) + name_bonus + 0.3
    
    return min(relevance_score, 1.0)  # Ensure score doesn't exceed 1.0


def get_approved_tools_response(question: str, department: str) -> dict:
    """
    Core function: Returns a list of approved AI tools for a specific department,
    ranked by their relevance to the user's specific question.
    
    Args:
        question (str): The user's input question.
        department (str): The department context (Marketing, HR, etc.) to filter tools.
    
    Returns:
        dict: A dictionary with:
            - 'answer': Markdown formatted string response.
            - 'curated': Boolean (True).
            - 'tool_count': Number of tools found.
            - 'no_curated_data': Boolean (True if no tools found).
    """
    # Fetch all "approved" results for this department from the database
    approved_results = validated_results_manager.get_approved_by_department(department)
    
    # If no tools exist for this department yet
    if not approved_results:
        return {
            "answer": None,
            "no_curated_data": True,  # Flags that we should fall back to generic LLM
            "message": f"Noch keine empfohlenen Tools für {department} verfügbar. Bitte wenden Sie sich an den Administrator."
        }
    
    # Rank all available tools against the question
    scored_tools = []
    for tool in approved_results:
        score = score_tool_relevance(question, tool)
        scored_tools.append((tool, score))
    
    # Sort findings by score descending (most relevant first)
    scored_tools.sort(key=lambda x: x[1], reverse=True)
    
    # Build the final Markdown response string
    answer_parts = []
    answer_parts.append(f"## 🎯 Empfohlene KI-Tools für {department}\n")
    answer_parts.append(f"Basierend auf Ihrer Anfrage, hier die relevantesten Tools:\n")
    
    # Loop through ranked tools and format them
    for i, (tool, score) in enumerate(scored_tools, 1):
        tool_name = tool.get('tool_name', 'Unbekannt')
        source_url = tool.get('source_url', '')
        description = tool.get('llm_analysis', '')[:100]  # Truncate description for brevity
        
        # Add "badges" based on relevance score
        relevance_badge = ""
        if i == 1 and score > 0.5:
            relevance_badge = " ⭐ TOP-Empfehlung"
        elif i <= 3 and score > 0.4:
            relevance_badge = " 🔥 Sehr relevant"
        
        # Add tool details to output
        answer_parts.append(f"### {i}. {tool_name}{relevance_badge}")
        if source_url:
            answer_parts.append(f"🔗 **Website:** [{source_url}]({source_url})")
        if description:
            answer_parts.append(f"📝 {description}")
        answer_parts.append("")  # Empty line between tools for spacing
    
    # Footer
    answer_parts.append("---")
    answer_parts.append(f"*{len(approved_results)} Tool(s) von unserem Team geprüft und empfohlen.*")
    
    return {
        "answer": "\n".join(answer_parts),
        "curated": True,
        "tool_count": len(approved_results)
    }


def answer_with_curated_knowledge(question: str, department: str) -> dict:
    """
    Public API endpoint for this module.
    Delegates to get_approved_tools_response.
    """
    return get_approved_tools_response(question, department)


def get_curated_stats(department: str = None) -> dict:
    """
    Get statistics about the curated knowledge base.
    Used for dashboard or status checks.
    
    Args:
        department (str, optional): If provided, returns stats for only that department.
        
    Returns:
        dict: Stats object (counts, booleans, etc.)
    """
    if department:
        # Get count for specific department
        approved = validated_results_manager.get_approved_by_department(department)
        return {
            "department": department,
            "approved_count": len(approved),
            "has_data": len(approved) > 0
        }
    else:
        # Get aggregated stats for all departments
        all_approved = validated_results_manager.get_all_approved()
        by_dept = {}
        for result in all_approved:
            dept = result.get('department', 'Unknown')
            by_dept[dept] = by_dept.get(dept, 0) + 1
        
        return {
            "total_approved": len(all_approved),
            "by_department": by_dept
        }
