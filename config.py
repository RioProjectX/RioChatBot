from os import environ

ENV = True # make it false for heroku

# List of supported languages >>
# https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages

if not ENV:
  bot_token = ""
  ARQ_API_KEY = ""
  LANGUAGE = "id"
  api_id = ""
  api_hash = ""
  ARQ_API_BASE_URL = "https://thearq.tech"
  BOT_USERNAME = "jungkokchatbot"
  KONTOL = "Rio"
  MEMEK = "https://telegra.ph/file/0a766bf53e048281392aa.jpg"
else:
  bot_token = str(environ.get("BOT_TOKEN", None))
  ARQ_API_KEY = str(environ.get("ARQ_API_KEY", None))
  LANGUAGE = str(environ.get("LANGUAGE", "id"))
  api_id = int(environ.get("API_ID", 6))
  api_hash = str(environ.get("API_HASH", "cd350d5d129d8feb5bc35cf109baa284"))
  ARQ_API_BASE_URL = "https://thearq.tech"
  BOT_USERNAME = str(environ.get("BOT_USERNAME", "jungkokchatbot"))
  KONTOL = str(environ.get("BOT_NAME", "Jungkok"))
  MEMEK = str(environ.get("MEDIA", "https://telegra.ph/file/0a766bf53e048281392aa.jpg"))
