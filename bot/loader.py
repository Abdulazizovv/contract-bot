from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.data import config
from bot.utils.db_api.db import DBcommands
from bot.utils.didox_utils import DidoxManager, GoogleDocsProcessor

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DBcommands()

didox_manager = DidoxManager.new()
google_docs_processor = GoogleDocsProcessor(credentials_path=config.GOOGLE_SERVICE_ACCOUNT_FILE, template_id=config.GOOGLE_DOC_ID, destination_folder_id=config.GOOGLE_DRIVE_FOLDER_ID)


