from os import environ

ENV = True # make it false for heroku

# List of supported languages >>
# https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages

if not ENV:
  bot_token = ""
  ARQ_API_KEY = ""
  LANGUAGE = ""
  api_id = ""
  api_hash = ""
  ARQ_API_BASE_URL = "https://thearq.tech"
else:
  bot_token = str(environ.get("bot_token", None))
  ARQ_API_KEY = str(environ.get("ARQ_API_KEY", None))
  LANGUAGE = str(environ.get("LANGUAGE", "id"))
  api_id = int(environ.get("api_id", 6))
  api_hash = str(environ.get("api_hash", "eb06d4abfb49dc3eeb1aeb98ae0f581e"))
  ARQ_API_BASE_URL = str(environ.get("ARQ_API_BASE_URL", None))
