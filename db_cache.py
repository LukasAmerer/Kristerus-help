"""
Azure Cosmos DB (MongoDB API) cache layer for storing and retrieving question-answer pairs.
"""
import os
import hashlib
from datetime import datetime
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

class AnswerCache:
    """Manages caching of question-answer pairs in Azure Cosmos DB (MongoDB API)"""
    
    def __init__(self):
        """Initialize MongoDB client"""
        connection_string = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
        
        if not connection_string:
            print("⚠️ Azure Cosmos DB connection string not found. Caching disabled.")
            self.client = None
            self.collection = None
            return
        
        try:
            self.client = MongoClient(connection_string)
            db = self.client["kmu_meet_ki"]
            self.collection = db["answer_cache"]
            
            # Test connection with a ping
            self.client.admin.command('ping')
            
            print("✅ Azure Cosmos DB (MongoDB) connected successfully")
        except Exception as e:
            print(f"❌ Failed to connect to Cosmos DB: {e}")
            self.client = None
            self.collection = None
    
    def _hash_question(self, question: str, department: str) -> str:
        """Generate a unique hash for a question"""
        combined = f"{department}:{question.lower().strip()}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def get_cached_answer(self, question: str, department: str) -> dict:
        """
        Retrieve cached answer for a question.
        Returns dict with 'answer' key if found, otherwise None.
        """
        if self.collection is None:
            return None
        
        try:
            question_hash = self._hash_question(question, department)
            
            # Query for the cached item
            item = self.collection.find_one({
                "question_hash": question_hash,
                "department": department
            })
            
            if item:
                print(f"✅ Cache HIT for: {question[:50]}...")
                return {
                    'answer': item.get('answer'),
                    'cached': True,
                    'created_at': item.get('created_at')
                }
            else:
                print(f"❌ Cache MISS for: {question[:50]}...")
                return None
        except Exception as e:
            print(f"⚠️ Cache lookup error: {e}")
            return None
    
    def store_answer(self, question: str, department: str, answer: str) -> bool:
        """
        Store a question-answer pair in the cache.
        Returns True if successful, False otherwise.
        """
        if self.collection is None:
            return False
        
        try:
            question_hash = self._hash_question(question, department)
            
            document = {
                'question_hash': question_hash,
                'department': department,
                'question': question,
                'answer': answer,
                'created_at': datetime.utcnow(),
                'validated': True
            }
            
            # Upsert: update if exists, insert if new
            self.collection.update_one(
                {"question_hash": question_hash, "department": department},
                {"$set": document},
                upsert=True
            )
            
            print(f"✅ Cached answer for: {question[:50]}...")
            return True
        except Exception as e:
            print(f"⚠️ Failed to cache answer: {e}")
            return False

# Global cache instance
cache = AnswerCache()
