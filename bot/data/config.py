from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS") 

BOT_PASSWORD = env.str("BOT_PASSWORD")

# Google Docs API sozlamalari
GOOGLE_SERVICE_ACCOUNT_FILE = env.str("GOOGLE_SERVICE_ACCOUNT_FILE")
GOOGLE_DOC_ID = env.str("GOOGLE_DOC_ID")
GOOGLE_DRIVE_FOLDER_ID = env.str("GOOGLE_DRIVE_FOLDER_ID")

JSHIR = env.str("JSHIR")

