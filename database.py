from pymongo import MongoClient
import sys
# Password for the database user
PASSWORD = "ooXzGZ2jVCTl5hkN" 

CLUSTER_URL = "fyndassignment.y9iyyae.mongodb.net"


MONGO_URI = f"mongodb+srv://Admin_db_user:{PASSWORD}@{CLUSTER_URL}/?retryWrites=true&w=majority&appName=FYNDAssignment"

def test_connection():

    print("Connecting to MongoDB Atlas")
    print(f"Target: {CLUSTER_URL}")
    
    try:
      
        client = MongoClient(MONGO_URI)
        
       
        client.admin.command('ping')
        
        print("✅ SUCCESS! Connection established.")

        
    except Exception as e:
        print("❌ FAILED to connect.")
        print(f"Error Message: {e}")

if __name__ == "__main__":
    test_connection()