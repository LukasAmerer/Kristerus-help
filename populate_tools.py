# Populate database with comprehensive AI tools list
from db_cache import validated_results_manager
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

# Clear database first
connection_string = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
client = MongoClient(connection_string)
db = client["kmu_meet_ki"]
collection = db["validated_results"]
for doc in collection.find({}):
    collection.delete_one({"_id": doc["_id"]})
print("Cleared database")

# Comprehensive AI tools by department
AI_TOOLS = {
    "Marketing": [
        {"name": "Jasper", "url": "https://www.jasper.ai", "desc": "AI content creation for marketing teams"},
        {"name": "Copy.ai", "url": "https://www.copy.ai", "desc": "AI copywriting and content generation"},
        {"name": "HubSpot AI", "url": "https://www.hubspot.com", "desc": "AI-powered marketing automation"},
        {"name": "Surfer SEO", "url": "https://surferseo.com", "desc": "AI SEO content optimization"},
        {"name": "Canva AI", "url": "https://www.canva.com", "desc": "AI-powered design and content creation"},
        {"name": "Writesonic", "url": "https://writesonic.com", "desc": "AI writing assistant for marketing"},
        {"name": "Phrasee", "url": "https://phrasee.co", "desc": "AI for marketing language optimization"},
        {"name": "Persado", "url": "https://www.persado.com", "desc": "AI-generated marketing content"},
        {"name": "Albert AI", "url": "https://albert.ai", "desc": "Autonomous AI marketing platform"},
        {"name": "MarketMuse", "url": "https://www.marketmuse.com", "desc": "AI content strategy platform"},
        {"name": "Hootsuite OwlyWriter", "url": "https://www.hootsuite.com", "desc": "AI social media content"},
        {"name": "Sprout Social AI", "url": "https://sproutsocial.com", "desc": "AI social media management"},
        {"name": "Synthesia", "url": "https://www.synthesia.io", "desc": "AI video generation platform"},
        {"name": "Lumen5", "url": "https://lumen5.com", "desc": "AI video creation from text"},
        {"name": "Pictory", "url": "https://pictory.ai", "desc": "AI video editing and creation"},
        {"name": "Runway ML", "url": "https://runwayml.com", "desc": "AI creative tools for video"},
        {"name": "Midjourney", "url": "https://www.midjourney.com", "desc": "AI image generation"},
        {"name": "DALL-E", "url": "https://openai.com/dall-e-3", "desc": "OpenAI image generation"},
        {"name": "Adobe Firefly", "url": "https://www.adobe.com/products/firefly.html", "desc": "AI design tools"},
        {"name": "Semrush AI", "url": "https://www.semrush.com", "desc": "AI SEO and marketing toolkit"},
    ],
    "Customer Success": [
        {"name": "Intercom", "url": "https://www.intercom.com", "desc": "AI customer messaging platform"},
        {"name": "Zendesk AI", "url": "https://www.zendesk.com", "desc": "AI customer service automation"},
        {"name": "Drift", "url": "https://www.drift.com", "desc": "Conversational AI for customer engagement"},
        {"name": "Freshdesk AI", "url": "https://www.freshworks.com", "desc": "AI-powered customer support"},
        {"name": "Ada", "url": "https://www.ada.cx", "desc": "AI chatbot for automated customer service"},
        {"name": "Kustomer", "url": "https://www.kustomer.com", "desc": "AI-powered CRM platform"},
        {"name": "Gorgias", "url": "https://www.gorgias.com", "desc": "AI helpdesk for e-commerce"},
        {"name": "Tidio", "url": "https://www.tidio.com", "desc": "AI chatbots for customer service"},
        {"name": "LivePerson", "url": "https://www.liveperson.com", "desc": "Conversational AI platform"},
        {"name": "Salesforce Einstein", "url": "https://www.salesforce.com", "desc": "AI for customer relationship management"},
        {"name": "Dialpad AI", "url": "https://www.dialpad.com", "desc": "AI-powered communication platform"},
        {"name": "Aircall AI", "url": "https://aircall.io", "desc": "AI call center solution"},
        {"name": "Chorus.ai", "url": "https://www.chorus.ai", "desc": "AI conversation intelligence"},
        {"name": "Gong", "url": "https://www.gong.io", "desc": "AI revenue intelligence platform"},
        {"name": "Clari", "url": "https://www.clari.com", "desc": "AI revenue operations"},
        {"name": "Gainsight", "url": "https://www.gainsight.com", "desc": "AI customer success platform"},
        {"name": "Totango", "url": "https://www.totango.com", "desc": "AI customer success software"},
        {"name": "ChurnZero", "url": "https://churnzero.com", "desc": "AI customer retention"},
    ],
    "HR": [
        {"name": "HireVue", "url": "https://www.hirevue.com", "desc": "AI video interviewing and assessment"},
        {"name": "Workday AI", "url": "https://www.workday.com", "desc": "AI HR management and analytics"},
        {"name": "Greenhouse", "url": "https://www.greenhouse.com", "desc": "AI-powered recruiting platform"},
        {"name": "Eightfold AI", "url": "https://eightfold.ai", "desc": "AI talent intelligence platform"},
        {"name": "Textio", "url": "https://textio.com", "desc": "AI writing for job descriptions"},
        {"name": "Pymetrics", "url": "https://www.pymetrics.ai", "desc": "AI-based talent matching"},
        {"name": "Beamery", "url": "https://beamery.com", "desc": "AI talent lifecycle management"},
        {"name": "Paradox AI", "url": "https://www.paradox.ai", "desc": "Conversational AI for recruiting"},
        {"name": "Fetcher", "url": "https://fetcher.ai", "desc": "AI recruiting automation"},
        {"name": "Humanly", "url": "https://humanly.io", "desc": "AI for recruiting conversations"},
        {"name": "Lever", "url": "https://www.lever.co", "desc": "AI recruiting and hiring"},
        {"name": "Phenom", "url": "https://www.phenom.com", "desc": "AI talent experience platform"},
        {"name": "SeekOut", "url": "https://seekout.com", "desc": "AI talent sourcing"},
        {"name": "HiredScore", "url": "https://www.hiredscore.com", "desc": "AI talent intelligence"},
        {"name": "AllyO", "url": "https://www.allyo.com", "desc": "AI recruiting assistant"},
        {"name": "Lattice", "url": "https://lattice.com", "desc": "AI performance management"},
        {"name": "Culture Amp", "url": "https://www.cultureamp.com", "desc": "AI employee engagement"},
        {"name": "15Five", "url": "https://www.15five.com", "desc": "AI performance management"},
    ],
    "Product": [
        {"name": "Notion AI", "url": "https://www.notion.so", "desc": "AI-powered workspace and documentation"},
        {"name": "Figma AI", "url": "https://www.figma.com", "desc": "AI design and prototyping tools"},
        {"name": "Miro AI", "url": "https://miro.com", "desc": "AI collaborative whiteboard"},
        {"name": "Aha!", "url": "https://www.aha.io", "desc": "AI product roadmap planning"},
        {"name": "Productboard AI", "url": "https://www.productboard.com", "desc": "AI product management platform"},
        {"name": "Coda AI", "url": "https://coda.io", "desc": "AI-powered collaborative documents"},
        {"name": "Linear", "url": "https://linear.app", "desc": "AI-enhanced issue tracking"},
        {"name": "Amplitude AI", "url": "https://amplitude.com", "desc": "AI product analytics"},
        {"name": "Pendo AI", "url": "https://www.pendo.io", "desc": "AI product experience platform"},
        {"name": "Maze AI", "url": "https://maze.co", "desc": "AI user research platform"},
        {"name": "Hotjar", "url": "https://www.hotjar.com", "desc": "AI user behavior analytics"},
        {"name": "FullStory", "url": "https://www.fullstory.com", "desc": "AI digital experience analytics"},
        {"name": "Heap", "url": "https://heap.io", "desc": "AI product analytics"},
        {"name": "Mixpanel", "url": "https://mixpanel.com", "desc": "AI product analytics platform"},
        {"name": "UserTesting AI", "url": "https://www.usertesting.com", "desc": "AI user testing platform"},
        {"name": "Dovetail", "url": "https://dovetailapp.com", "desc": "AI research repository"},
        {"name": "Sprig", "url": "https://sprig.com", "desc": "AI product experience insights"},
        {"name": "Jira AI", "url": "https://www.atlassian.com/software/jira", "desc": "AI project management"},
    ],
    "General": [
        {"name": "ChatGPT", "url": "https://chat.openai.com", "desc": "OpenAI's conversational AI assistant"},
        {"name": "Claude", "url": "https://claude.ai", "desc": "Anthropic's AI assistant"},
        {"name": "Google Gemini", "url": "https://gemini.google.com", "desc": "Google's multimodal AI"},
        {"name": "Microsoft Copilot", "url": "https://copilot.microsoft.com", "desc": "AI assistant for Microsoft 365"},
        {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "desc": "AI-powered search and research"},
        {"name": "Grammarly", "url": "https://www.grammarly.com", "desc": "AI writing assistant"},
        {"name": "Otter.ai", "url": "https://otter.ai", "desc": "AI meeting transcription"},
        {"name": "Zapier AI", "url": "https://zapier.com", "desc": "AI workflow automation"},
        {"name": "Fireflies.ai", "url": "https://fireflies.ai", "desc": "AI meeting notes and transcription"},
        {"name": "Descript", "url": "https://www.descript.com", "desc": "AI video and podcast editing"},
        {"name": "Notion AI", "url": "https://notion.so", "desc": "AI workspace assistant"},
        {"name": "Mem AI", "url": "https://mem.ai", "desc": "AI-powered notes and knowledge base"},
        {"name": "Taskade AI", "url": "https://taskade.com", "desc": "AI project management"},
        {"name": "Motion", "url": "https://www.usemotion.com", "desc": "AI calendar and task management"},
        {"name": "Reclaim.ai", "url": "https://reclaim.ai", "desc": "AI calendar scheduling"},
        {"name": "Clockwise", "url": "https://www.getclockwise.com", "desc": "AI time management"},
        {"name": "Krisp", "url": "https://krisp.ai", "desc": "AI noise cancellation for calls"},
        {"name": "Murf AI", "url": "https://murf.ai", "desc": "AI voice generation"},
        {"name": "ElevenLabs", "url": "https://elevenlabs.io", "desc": "AI voice synthesis"},
        {"name": "GitHub Copilot", "url": "https://github.com/features/copilot", "desc": "AI coding assistant"},
        {"name": "Cursor", "url": "https://cursor.sh", "desc": "AI-powered code editor"},
        {"name": "Replit AI", "url": "https://replit.com", "desc": "AI coding and development"},
    ],
}

# Add all tools to database
count = 0
for dept, tools in AI_TOOLS.items():
    for tool in tools:
        validated_results_manager.add_pending_result(
            query=f"AI tools for {dept}",
            department=dept,
            llm_analysis=tool["desc"],
            apertus_validation="Curated list",
            tool_name=tool["name"],
            source_url=tool["url"]
        )
        count += 1

print(f"\n=== DONE: Added {count} AI tools ===")
for dept in AI_TOOLS:
    print(f"  {dept}: {len(AI_TOOLS[dept])} tools")
