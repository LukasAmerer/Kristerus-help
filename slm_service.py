"""
Local SLM Service - Shows approved AI tools from Research Assistant to users.
Ranks tools by relevance to the user's question using keyword matching and similarity.
"""
from difflib import SequenceMatcher
import re
from db_cache import validated_results_manager


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate text similarity using SequenceMatcher (0.0 to 1.0)"""
    text1 = text1.lower().strip()
    text2 = text2.lower().strip()
    return SequenceMatcher(None, text1, text2).ratio()


def extract_keywords(text: str) -> set:
    """Extract meaningful keywords from text"""
    # Common German and English stop words to filter out
    stop_words = {
        'der', 'die', 'das', 'und', 'oder', 'für', 'mit', 'von', 'zu', 'in', 'auf', 'ist', 'sind',
        'ein', 'eine', 'einer', 'einem', 'einen', 'wie', 'was', 'wer', 'wo', 'wann', 'warum',
        'the', 'a', 'an', 'and', 'or', 'for', 'with', 'of', 'to', 'in', 'on', 'is', 'are',
        'how', 'what', 'who', 'where', 'when', 'why', 'can', 'could', 'would', 'should',
        'welche', 'welcher', 'welches', 'gibt', 'es', 'ich', 'sie', 'er', 'wir', 'ihr',
        'bitte', 'können', 'kann', 'werden', 'wurde', 'haben', 'hat', 'sein', 'bei', 'am',
        'tools', 'tool', 'ki', 'ai', 'beste', 'best', 'gut', 'good'
    }
    
    # Extract words, lowercase, filter stopwords and short words
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = {w for w in words if w not in stop_words and len(w) > 2}
    
    return keywords


def score_tool_relevance(question: str, tool: dict) -> float:
    """
    Score how relevant a tool is to the user's question.
    Returns a score between 0.0 and 1.0.
    """
    question_keywords = extract_keywords(question)
    
    # Get tool info
    tool_name = tool.get('tool_name', '')
    description = tool.get('llm_analysis', '')
    
    # Combine tool info for matching
    tool_text = f"{tool_name} {description}"
    tool_keywords = extract_keywords(tool_text)
    
    # Calculate keyword overlap
    if question_keywords:
        common_keywords = question_keywords & tool_keywords
        keyword_score = len(common_keywords) / len(question_keywords)
    else:
        keyword_score = 0.5  # Neutral if no keywords
    
    # Calculate name similarity (bonus for direct name matches)
    name_similarity = calculate_similarity(question, tool_name)
    
    # Check for direct tool name mention in question
    name_bonus = 0.3 if tool_name.lower() in question.lower() else 0
    
    # Combined score
    relevance_score = (keyword_score * 0.5) + (name_similarity * 0.2) + name_bonus + 0.3
    
    return min(relevance_score, 1.0)  # Cap at 1.0


def get_approved_tools_response(question: str, department: str) -> dict:
    """
    Get a formatted response listing approved AI tools for a department,
    ranked by relevance to the user's question.
    
    Args:
        question: The user's question (used to rank tools)
        department: The department context (Marketing, HR, etc.)
    
    Returns:
        dict with 'answer' key containing formatted tool list
    """
    # Fetch approved results for this department
    approved_results = validated_results_manager.get_approved_by_department(department)
    
    if not approved_results:
        return {
            "answer": None,
            "no_curated_data": True,
            "message": f"Noch keine empfohlenen Tools für {department} verfügbar. Bitte wenden Sie sich an den Administrator."
        }
    
    # Score and rank tools by relevance to the question
    scored_tools = []
    for tool in approved_results:
        score = score_tool_relevance(question, tool)
        scored_tools.append((tool, score))
    
    # Sort by score (highest first)
    scored_tools.sort(key=lambda x: x[1], reverse=True)
    
    # Build response with ranked tools
    answer_parts = []
    answer_parts.append(f"## 🎯 Empfohlene KI-Tools für {department}\n")
    answer_parts.append(f"Basierend auf Ihrer Anfrage, hier die relevantesten Tools:\n")
    
    for i, (tool, score) in enumerate(scored_tools, 1):
        tool_name = tool.get('tool_name', 'Unbekannt')
        source_url = tool.get('source_url', '')
        description = tool.get('llm_analysis', '')[:100]  # Short description
        
        # Add relevance indicator for top tools
        relevance_badge = ""
        if i == 1 and score > 0.5:
            relevance_badge = " ⭐ TOP-Empfehlung"
        elif i <= 3 and score > 0.4:
            relevance_badge = " 🔥 Sehr relevant"
        
        answer_parts.append(f"### {i}. {tool_name}{relevance_badge}")
        if source_url:
            answer_parts.append(f"🔗 **Website:** [{source_url}]({source_url})")
        if description:
            answer_parts.append(f"📝 {description}")
        answer_parts.append("")  # Empty line between tools
    
    answer_parts.append("---")
    answer_parts.append(f"*{len(approved_results)} Tool(s) von unserem Team geprüft und empfohlen.*")
    
    return {
        "answer": "\n".join(answer_parts),
        "curated": True,
        "tool_count": len(approved_results)
    }


def answer_with_curated_knowledge(question: str, department: str) -> dict:
    """
    Answer user question by showing approved tools for their department,
    ranked by relevance to their question.
    
    Args:
        question: The user's question (used to rank tools by relevance)
        department: The department context (Marketing, HR, etc.)
    
    Returns:
        dict with 'answer' key containing formatted tool list
    """
    return get_approved_tools_response(question, department)


def get_curated_stats(department: str = None) -> dict:
    """Get statistics about curated knowledge for a department or overall."""
    if department:
        approved = validated_results_manager.get_approved_by_department(department)
        return {
            "department": department,
            "approved_count": len(approved),
            "has_data": len(approved) > 0
        }
    else:
        all_approved = validated_results_manager.get_all_approved()
        by_dept = {}
        for result in all_approved:
            dept = result.get('department', 'Unknown')
            by_dept[dept] = by_dept.get(dept, 0) + 1
        
        return {
            "total_approved": len(all_approved),
            "by_department": by_dept
        }
