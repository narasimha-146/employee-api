from pymongo import MongoClient

uri = "mongodb+srv://narashimha987_db_user:Narasimha146@employeescluster.n3vwktz.mongodb.net/assessment_db?retryWrites=true&w=majority"
print("Connecting...")

client = MongoClient(uri, serverSelectionTimeoutMS=5000)  # 5 second timeout
try:
    print("Databases:", client.list_database_names())
except Exception as e:
    print("Error:", e)
