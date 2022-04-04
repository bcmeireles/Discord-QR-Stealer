import json
def load_config(category, setting):
	with open("config.json") as f:
		cfg_data = json.load(f)

	return cfg_data[category][setting]



import pymongo
client = pymongo.MongoClient(load_config("mongodb", "host"), int(load_config("mongodb", "port")))
db = client[load_config("mongodb", "db")]
tokens = db[load_config("mongodb", "collection")]

choice = input(f"""________  .___  __________________  ________ __________ 
\______ \ |   |/   _____/\_   ___ \ \_____  \\______   \\
 |    |  \|   |\_____  \ /    \  \/  /  / \  \|       _/
 |    `   \   |/        \\     \____/   \_/.  \    |   \\
/_______  /___/_______  / \______  /\_____\ \_/____|_  /
        \/            \/         \/        \__>      \/ 
__________  _____    _______  ___________.____     
\______   \/  _  \   \      \ \_   _____/|    |    
 |     ___/  /_\  \  /   |   \ |    __)_ |    |    
 |    |  /    |    \/    |    \|        \|    |___ 
 |____|  \____|__  /\____|__  /_______  /|_______ \\
                 \/         \/        \/         \/
                 
                 
Tokens loaded: {tokens.count_documents({})}""")