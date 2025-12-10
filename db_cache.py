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


class ValidatedResultsManager:
    """Manages validated research results for the Research Assistant → Anwendungen von KI flow"""
    
    def __init__(self):
        """Initialize MongoDB client for validated results"""
        connection_string = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
        
        if not connection_string:
            print("⚠️ Azure Cosmos DB connection string not found. Validated results disabled.")
            self.client = None
            self.collection = None
            return
        
        try:
            self.client = MongoClient(connection_string)
            db = self.client["kmu_meet_ki"]
            self.collection = db["validated_results"]
            print("✅ ValidatedResultsManager connected to Cosmos DB")
        except Exception as e:
            print(f"❌ Failed to connect ValidatedResultsManager: {e}")
            self.client = None
            self.collection = None
    
    def add_pending_result(self, query: str, department: str, llm_analysis: str, apertus_validation: str, tool_name: str = None, source_url: str = None) -> str:
        """Add a new research result with pending status. Returns the result ID."""
        if self.collection is None:
            return None
        
        try:
            result_id = hashlib.sha256(f"{query}:{department}:{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
            
            document = {
                'result_id': result_id,
                'query': query,
                'tool_name': tool_name or query[:50],  # Use tool_name if provided, else query
                'source_url': source_url or '',
                'department': department,
                'llm_analysis': llm_analysis,
                'apertus_validation': apertus_validation,
                'status': 'pending',
                'approved_by': None,
                'created_at': datetime.utcnow(),
                'approved_at': None
            }
            
            self.collection.insert_one(document)
            print(f"✅ Added pending result: {result_id} - {tool_name}")
            return result_id
        except Exception as e:
            print(f"⚠️ Failed to add pending result: {e}")
            return None
    
    def get_pending_results(self) -> list:
        """Get all results with pending status"""
        if self.collection is None:
            return []
        
        try:
            results = list(self.collection.find({'status': 'pending'}))
            return results
        except Exception as e:
            print(f"⚠️ Failed to get pending results: {e}")
            return []
    
    def get_approved_by_department(self, department: str) -> list:
        """Get all approved results for a specific department"""
        if self.collection is None:
            return []
        
        try:
            results = list(self.collection.find({
                'status': 'approved',
                'department': department
            }))
            return results
        except Exception as e:
            print(f"⚠️ Failed to get approved results: {e}")
            return []
    
    def get_all_approved(self) -> list:
        """Get all approved results across all departments"""
        if self.collection is None:
            return []
        
        try:
            results = list(self.collection.find({'status': 'approved'}))
            return results
        except Exception as e:
            print(f"⚠️ Failed to get all approved results: {e}")
            return []
    
    def approve_result(self, result_id: str, approved_by: str) -> bool:
        """Approve a pending result"""
        if self.collection is None:
            return False
        
        try:
            result = self.collection.update_one(
                {'result_id': result_id, 'status': 'pending'},
                {'$set': {
                    'status': 'approved',
                    'approved_by': approved_by,
                    'approved_at': datetime.utcnow()
                }}
            )
            if result.modified_count > 0:
                print(f"✅ Approved result: {result_id}")
                return True
            return False
        except Exception as e:
            print(f"⚠️ Failed to approve result: {e}")
            return False
    
    def reject_result(self, result_id: str) -> bool:
        """Reject a pending result"""
        if self.collection is None:
            return False
        
        try:
            result = self.collection.update_one(
                {'result_id': result_id, 'status': 'pending'},
                {'$set': {'status': 'rejected'}}
            )
            if result.modified_count > 0:
                print(f"❌ Rejected result: {result_id}")
                return True
            return False
        except Exception as e:
            print(f"⚠️ Failed to reject result: {e}")
            return False
    
    def revoke_approval(self, result_id: str) -> bool:
        """Revoke approval and set back to pending"""
        if self.collection is None:
            return False
        
        try:
            result = self.collection.update_one(
                {'result_id': result_id, 'status': 'approved'},
                {'$set': {
                    'status': 'pending',
                    'approved_by': None,
                    'approved_at': None
                }}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"⚠️ Failed to revoke approval: {e}")
            return False


# Global validated results manager instance
validated_results_manager = ValidatedResultsManager()
