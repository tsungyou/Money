class MongoList:
    DB_LIST = ['PSTAGE', "PDATA"]
    PARENT_DIR = 'financial_statements'
    DIR_NEEDED = [PARENT_DIR, f"{PARENT_DIR}/{DB_LIST[0]}", f"{PARENT_DIR}/{DB_LIST[1]}"]
    CLOUD_URL = "mongodb+srv://doadmin:12VQ3UrM70T695BL@medina-mongo-prod-4d15c7ee.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
    LOCAL_URL = "mongodb://localhost:27017/"
