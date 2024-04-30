from decouple import config
DB_URL = config("MONGO_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)
DB_COLLECTION = config("COLLECTION_NAME", cast=str)