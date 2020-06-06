from datetime import date, timedelta
import config

client = config.dev_config.DATABASE_URI

db = client['Search_Results']
admin_users = db['admin_users']
users = db['users']
search_results = db["search_results"]

class users:
    pass


class search_results:
    pass


