# Author: https://github.com/SastaDev
# Created on: Sun, Sep 3, 2023.
# © Kangers Network ~ https://t.me/KangersNetwork

from typing import BinaryIO, Dict, List
import time
import os
from uuid import uuid4

import httpx

from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram import Client, filters

# Replace `YourRobot` with your robot and import pyrogram client from it.
from SagiriRobot import pbot

API_URL: str = "https://sasta-api.vercel.app/google_reverse"

COMMANDS: List[str] = [
    "reverse",
    "grs",
    "pp"
    ]

async_client: httpx.AsyncClient = httpx.AsyncClient(timeout=120)

class STRINGS:
    REPLY_TO_MEDIA: str = "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍꜱɢ ᴛᴏ ꜱᴛᴀʀᴛ ꜱᴇᴀʀᴄʜɪɴɢ ꜰʀᴏᴍ."
    UNSUPPORTED_MEDIA_TYPE: str = "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍꜱɢ ᴛᴏ ꜱᴛᴀʀᴛ ꜱᴇᴀʀᴄʜɪɴɢ ꜰʀᴏᴍ."
    
    DOWNLOADING_MEDIA: str = "ꜱᴇᴀʀᴄʜɪɴɢ..."
    UPLOADING_TO_API_SERVER: str = "ꜱᴇᴀʀᴄʜɪɴɢ.."
    PARSING_RESULT: str = "ꜱᴇᴀʀᴄʜɪɴɢ...."
    
    EXCEPTION_OCCURRED: str = "ʜᴜʜ <b>Error!</b>\n\n<b>Exception:</b> {}"
    
    RESULT: str = """
 <b>ʀᴇꜱᴜʟᴛ ꜰᴏʀ:</b> <code>{query}</code>
 <b>ʟɪɴᴋ:</b> <a href="{page_url}">Link</a>
 
    """
    OPEN_PAGE: str = "ʟɪɴᴋ"

@pbot.on_message(filters.command(COMMANDS))
async def on_reverse(client: Client, message: Message) -> None:
    if not message.reply_to_message:
        await message.reply(STRINGS.REPLY_TO_MEDIA)
        return
    elif message.reply_to_message.media not in (MessageMediaType.PHOTO, MessageMediaType.STICKER, MessageMediaType.DOCUMENT):
        await message.reply(STRINGS.UNSUPPORTED_MEDIA_TYPE)
        return
    
    start_time: float = time.time()
    status_msg: Message = await message.reply(STRINGS.DOWNLOADING_MEDIA)
    file_path: str = f"temp_download/{uuid4()}"
    try:
        await message.reply_to_message.download(file_path)
    except Exception as exc:
        text: str = STRINGS.EXCEPTION_OCCURRED.format(exc)
        await message.reply(text)
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass
        return
    
    await status_msg.edit(STRINGS.UPLOADING_TO_API_SERVER)
    files: Dict[str, BinaryIO] = {"file": open(file_path, "rb")}
    response: httpx.Response = await async_client.post(API_URL, files=files)
    os.remove(file_path)
    
    if response.status_code == 404:
        text: str = STRINGS.EXCEPTION_OCCURRED.format(response.json()["error"])
        await message.reply(text)
        await status_msg.delete()
        return
    elif response.status_code != 200:
        text: str = STRINGS.EXCEPTION_OCCURRED.format(response.text)
        await message.reply(text)
        await status_msg.delete()
        return
    
    await status_msg.edit(STRINGS.PARSING_RESULT)
    response_json: Dict[str, str] = response.json()
    query: str = response_json["query"]
    page_url: str = response_json["url"]
    
    end_time: float = time.time() - start_time
    time_taken: str = "{:.2f}".format(end_time)
    
    text: str = STRINGS.RESULT.format(
        query=query,
        page_url=page_url,
        time_taken=time_taken
        )
    buttons: List[List[InlineKeyboardButton]] = [
        [InlineKeyboardButton(STRINGS.OPEN_PAGE, url=page_url)]
        ]
    await message.reply(text, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(buttons))
    await status_msg.delete()
