print("[INFO]: INITIALIZING ...")
import re
from time import time
from datetime import datetime
from asyncio import (gather, get_event_loop, sleep)
import requests
from aiohttp import ClientSession
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import (Client, filters, idle)
from Python_ARQ import ARQ
from config import bot_token, ARQ_API_KEY, LANGUAGE, api_id, api_hash, ARQ_API_BASE_URL, BOT_USERNAME, KONTOL, MEMEK


print("[INFO]: INITIALIZING BOT CLIENT ...")
luna = Client(":memory:",
              bot_token=bot_token,
              api_id=api_id,
              api_hash=api_hash,
)
bot_id = int(bot_token.split(":")[0])
print("[INFO]: INITIALIZING ...")
arq = None


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


async def lunaQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "en"
        else (await arq.translate(query, "en")).result.translatedText
    )
    resp = (await arq.luna(query, user_id)).result
    return (
        resp
        if LANGUAGE == "en"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )


async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(2))
    if "Luna" in response:
        responsee = response.replace("Luna", f"{KONTOL}")
    else:
        responsee = response
    if "Aco" in responsee:
        responsess = responsee.replace("Aco", f"{KONTOL}")
    else:
        responsess = responsee
    if "Siapa rio?" in responsess:
        responsess2 = responsess.replace("Siapa rio?", "duh cute beut?👀")
    else:
        responsess2 = responsess
    await message.reply_text(responsess2)
    await message._client.send_chat_action(chat_id, "cancel")


@luna.on_message(filters.command(["start", f"start@{BOT_USERNAME}"]) & ~filters.edited)
async def start(client: Client, message: Message):
    start = time()
    delta_ping = time() - start
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    PM_IMG = f"{MEMEK}"
    kontol = await client.send_video(message.chat.id, PM_IMG, 
        caption=f"**Time Taken:** `{delta_ping * 1000:.3f} ms`\n"
        f"**Uptime:** `{uptime}`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Channel", url="https://t.me/riobotsupport"
                    ),
                    InlineKeyboardButton(
                        "Group", url="https://t.me/RioGroupSupport"
                    )
                ]
            ]
        )
    )


@luna.on_message(
    ~filters.private
    & filters.text
    & ~filters.command(["start", f"start@{BOT_USERNAME}"])
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            f"[.|\n]{0,}feri[.|\n]{0,}",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)


@luna.on_message(
    filters.private
    & ~filters.command(["start", f"start@{BOT_USERNAME}"])
    & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        await message.reply_text("Ufff... ignoring ....")
        return
    await type_and_send(message)


@luna.on_message(filters.command(["asupan", f"asupan@{BOT_USERNAME}"]))
async def asupan(client, message):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/asupan/ptl").json()
        results = f"{resp['url']}"
        return await client.send_video(message.chat.id, video=results)
    except Exception:
        await message.reply_text("`404 asupan videos not found`")


@luna.on_message(filters.command(["wibu", f"wibu@{BOT_USERNAME}"]))
async def wibu(client, message):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/asupan/wibu").json()
        results = f"{resp['url']}"
        return await client.send_video(message.chat.id, video=results)
    except Exception:
        await message.reply_text("`404 wibu not found`")


@luna.on_message(filters.command(["truth", f"truth@{BOT_USERNAME}"]))
async def truth(client, message):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/truth").json()
        results = f"{resp['message']}"
        return await message.reply_text(results)
    except Exception:
        await message.reply_text("something went wrong...")


@luna.on_message(filters.command(["dare", f"dare@{BOT_USERNAME}"]))
async def dare(client, message):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/dare").json()
        results = f"{resp['message']}"
        return await message.reply_text(results)
    except Exception:
        await message.reply_text("something went wrong...")


@luna.on_message(filters.command(["chika", f"chika@{BOT_USERNAME}"]))
async def chika(client, message):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/chika").json()
        results = f"{resp['url']}"
        return await client.send_video(message.chat.id, video=results)
    except Exception:
        await message.reply_text("`404 chika videos not found`")


async def main():
    global arq
    session = ClientSession()
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await luna.start()
    print(
        """
    -----------------
  | Chatbot Started! |
    -----------------
"""
    )
    await idle()


loop = get_event_loop()
loop.run_until_complete(main())
