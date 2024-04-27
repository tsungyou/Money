class MongoList:
    DB_LIST = ['PSTAGE', "PDATA"]
    DIR_NEEDED = ["financial_statements", f"financial_statements/{DB_LIST[0]}", f"financial_statements/{DB_LIST[1]}"]
    CLOUD_URL = "mongodb+srv://doadmin:12VQ3UrM70T695BL@medina-mongo-prod-4d15c7ee.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
    LOCAL_URL = "mongodb://localhost:27017/"
