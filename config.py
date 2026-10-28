import os

BOT_TOKEN = os.getenv("8827224396:AAGL05JzxEBrsdybLYjv0hPucuSDoQ_E8BM")

VAULT_CHANNEL_ID = int(os.getenv("VAULT_CHANNEL_ID", "-1003976296600"))  # Channel ID to fetch videos from
FORCE_JOIN_CHANNEL = os.getenv("FORCE_JOIN_CHANNEL", "https://t.me/foreveerrrrr07")       # Must join channel username

ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "8407496019"))  # Owner Telegram ID

# MongoDB connection URI (set in Heroku config vars)
MONGO_URI = os.getenv("mongodb+srv://Senorita_Db_user:Simple_boy@senorita.hiniu0l.mongodb.net/?appName=Senorita")

WELCOME_IMAGE = "https://files.catbox.moe/19j4mc.jpg"

DEVELOPER_LINK = "https://t.me/foreveerrrrr07"
SUPPORT_LINK = "https://t.me/RPShyariwold"
TERMS_LINK = "https://t.me/+C2Rm814XJQs0NDVl"

COOLDOWN_SECONDS = 8
