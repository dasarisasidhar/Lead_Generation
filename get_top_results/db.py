from datetime import date, timedelta
import config

client = config.dev_config.DATABASE_URI

db = client['Lead_Generation']
admin_users = db['admin_users']
users = db['users']
search_results = db["search_results"]

class users:
    pass

class admin:
    def check_login(data):
        try:
            admin_users.insert_one({"user_id":"admin@telyport.com", "password":"Telyport@123"})
            admin_details = admin_users.find_one({"user_id":data["id"]})
            if(admin_details["password"] == data["pswd"]):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

class search_results:
    pass


