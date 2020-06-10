from datetime import date, timedelta, datetime
import config

ts = datetime.now().timestamp()
client = config.dev_config.DATABASE_URI

db = client['Lead_Generation']
admin_users = db['admin_users']
users = db['users']
search_results = db["search_results"]

class user:
    def create_user(data):
        try:
            users.insert_one({"name":data['name'],"email":data["email"].lower(),"pswd":data["pswd"], 
                                    "created_datetime":ts, "is_active":True})
            return True
        except Exception as e:
            print(e)
            return False
            
    def check_login(details):
        try:
            user_details = users.find_one({"email":details["id"].lower()})
            if(user_details["pswd"] == details["pswd"] and user_details["is_active"] == True):
                return True
            elif(user_details["pswd"] != details["pswd"]):
                return "wrong password"
            elif(user_details["is_active"] == False):
                return "Agent is not active, please activate agent"
            else:
                return False
        except Exception as e:
            print(e)
            return False

class admin:
    def check_login(data):
        try:
            admin_details = admin_users.find_one({"user_id":data["id"]})
            if(admin_details["password"] == data["pswd"]):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

class search_result:
    pass


