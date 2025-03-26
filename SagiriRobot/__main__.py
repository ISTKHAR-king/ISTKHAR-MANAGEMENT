import importlib
import re
import time
import random
import asyncio

from telethon import __version__ as tlhver
from platform import python_version as y
from sys import argv

from pyrogram import __version__ as pyrover
from telegram import __version__ as telever
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver


from SagiriRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    PM_START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from SagiriRobot.modules import ALL_MODULES
from SagiriRobot.modules.helper_funcs.chat_status import is_user_admin
from SagiriRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

Sagiri_IMG = (
    "https://telegra.ph/file/b8a02e0b010714a1bba34.jpg",
    "https://telegra.ph/file/5406ed880a8089c6add3b.jpg",
    "https://te.legra.ph/file/1de42c29380053da56aed.jpg",
    "https://te.legra.ph/file/4481071e3d119bbf0f54f.jpg",
)  

PM_START_TEX = """
Wᴇʟᴄᴏᴍᴇ `{}`,  . 
"""


PM_START_TEXT = """ 
ʜᴇʏ {}, [🫧]({})

*𝙸'ᴍ 𝙶ᴏᴊᴏ ᴏꜰ ꜱɪx ᴇʏᴇꜱ!*

⌥ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ & ꜰᴀꜱᴛ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴡɪᴛʜ ᴀɴɪᴍᴇ ꜰᴜɴᴄᴛɪᴏɴᴀʟɪᴛʏ ᴡɪᴛʜ sᴏᴍᴇ ᴄᴏᴏʟ ғᴇᴀᴛᴜʀᴇs ʟɪᴋᴇ:
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
*・ᴍᴜꜱɪᴄ ᴘʟᴀʏᴇʀ.*
*・ɪᴍᴘᴏꜱᴛᴇʀ ᴅᴇᴛᴇᴄᴛᴏʀ.*
*・ꜱᴘᴀᴍ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ.*
*・ᴘʜ-ʟᴏɢᴏ ᴍᴀᴋᴇʀ.*
*・ʙᴇᴛᴛɪɴɢ ᴅᴏʟʟᴀʀ ɢᴀᴍᴇꜱ.*
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
▸ ᴛᴀᴘ ᴏɴ ʜᴇʟᴘ ᴍᴇɴᴜ ᴀɴᴅ ᴍᴜꜱɪᴄ ʙᴜᴛᴛᴏɴ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ.
"""

buttons = [
    [
        InlineKeyboardButton(
            text="⛩ ꜱᴜᴍᴍᴏɴ ᴍᴇ ⛩ ",
            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="🍁ᴄᴏᴍᴍᴀɴᴅꜱ🍁", callback_data="help_back"),
        InlineKeyboardButton(text="🎵ᴍᴜsɪᴄ ʜᴇʟᴘ🎵", callback_data="Music_"),
    ],
    [
        InlineKeyboardButton(text="sᴜᴩᴩᴏʀᴛ", url=f"https://t.me/Gojosupportchat"),
        InlineKeyboardButton(text="ᴀʙᴏᴜᴛ", callback_data="sagiri_"), 
    ],
    [
        InlineKeyboardButton(text="👾ᴀɴɪᴍᴇ ꜰᴜɴᴄᴛɪᴏɴᴀʟɪᴛʏ👾", callback_data="Gojoanime_"),  
        
    ],
    
]

HELP_STRINGS = f"""
[ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ](https://telegra.ph/file/80c35656e795bc58d58fc.jpg)
» ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴀʙᴏᴜᴛ sᴘᴇᴄɪғɪᴄ ᴄᴏᴍᴍᴀɴᴅs."""

DONATE_STRING = """ʜᴇʏ ᴅᴜᴅᴇ,
  ʜᴀᴩᴩʏ ᴛᴏ ʜᴇᴀʀ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴅᴏɴᴀᴛᴇ.

ʏᴏᴜ ᴄᴀɴ ᴅɪʀᴇᴄᴛʟʏ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ [ᴅᴇᴠᴇʟᴏᴩᴇʀ](f"tg://user?id={OWNER_ID}") ғᴏʀ ᴅᴏɴᴀᴛɪɴɢ ᴏʀ ʏᴏᴜ ᴄᴀɴ ᴠɪsɪᴛ ᴍʏ [sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ](f"https://t.me/{SUPPORT_CHAT}") ᴀɴᴅ ᴀsᴋ ᴛʜᴇʀᴇ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪᴏɴ."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("SagiriRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    
        

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@run_async
def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    update.effective_message.reply_text(
        "Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN
    )
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            
            x=update.effective_message.reply_sticker(
                "CAACAgUAAxkBAAEEDmVk6ZBdk0ldUBR7j5V0AAHOTF9p3iMAAlcJAAJtslFXGvhj-Smiu1wwBA")
            x.delete()
            usr = update.effective_user
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            
            time.sleep(0.2)
            lol.edit_text("ꜱᴛᴀʀᴛɪɴɢ.")
            time.sleep(0.0)
            lol.edit_text("ꜱᴛᴀʀᴛɪɴɢ..")
            time.sleep(0.0)
            lol.edit_text("ꜱᴛᴀʀᴛɪɴɢ...")
            time.sleep(0.0)
            lol.delete()
            
            
            update.effective_message.reply_text(
                PM_START_TEXT.format(escape_markdown(first_name), random.choice(Sagiri_IMG), BOT_NAME),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            random.choice(Sagiri_IMG),
            caption="◎𝙷ᴇʏ ʙᴜᴅᴅʏ ᴛʜɪꜱ ɪꜱ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ !\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ \n🫧 ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ. \n​˹ᴡᴏʀᴋɪɴɢ ᴘʀᴏᴘᴇʟʏ ꜱɪɴᴄᴇ˼ : <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ꜱᴜᴘᴘᴏʀᴛ",
                            url=f"https://t.me/Gojo_support_chat",
                        ),
                        InlineKeyboardButton(
                            text="ᴜᴘᴅᴀᴛᴇꜱ",
                            url=f"https://t.me/gojo_satoru_updates",
                        ),
                    ]
                ]
            ),
        )
            



def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "▸ *𝙰ᴠᴀɪʟᴀʙʟᴇ 𝙲𝙾𝙼𝙼𝙰𝙽𝙳𝚂 𝙵𝙾𝚁​​* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


def Sagiri_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "sagiri_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*ᴋᴏɴɪᴄʜɪᴡᴀ,*\n👤  *ᴛʜɪs ɪs {dispatcher.bot.first_name}*"
            "\n\n◸ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ & ᴍᴜꜱɪᴄ ʀᴏʙᴏᴛ ᴡɪᴛʜ ᴀɴɪᴍᴇ ꜰᴜɴᴄᴛɪᴏɴᴀʟɪᴛʏ ᴡʜɪᴄʜ ʜᴀꜱ ʟᴏꜱᴛ ᴏꜰ ꜰᴇᴀᴛᴜʀᴇꜱ ᴀɴᴅ ɢᴀᴍᴇꜱ!"
            "\n\n▸ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ ʜᴀꜱ ᴀᴅᴠᴀɴᴄᴇ ꜰᴇᴀᴛᴜʀᴇꜱ ʟɪᴋᴇ ᴅᴇᴛᴇᴄᴛ ɪᴍᴘᴏꜱᴛᴇʀ, ᴘʜ-ʟᴏɢᴏ ᴍᴀᴋᴇʀ, ʙᴇᴛᴛɪɴɢ ɢᴀᴍᴇꜱ ᴇᴛᴄ." 
            "\n\n▸ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ ʜᴀꜱ ᴡᴇʟᴄᴏᴍᴇ ᴛᴇᴍᴘʟᴀᴛᴇ ᴡʜɪᴄʜ ɢʀᴇᴇᴛ ᴜꜱᴇʀꜱ."
            "\n\n▸ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ ʜᴀꜱ ʟᴏᴛꜱ ᴏꜰ ꜰᴜɴ ꜰᴇᴀᴛᴜʀᴇꜱ ʟɪᴋᴇ ʙᴀᴛᴍᴀɴ, ꜱɪɢᴍᴀ, ᴘꜱʏᴄʜᴏ ᴇᴛᴄ."
            "\n\n▸  ꜱᴀᴛᴏʀᴜ ꜰʀᴇᴀᴋɪɴɢ ɢᴏᴊᴏ ᴄᴀɴ ᴘʟᴀʏ ꜱᴏɴɢ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀɴᴅ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴄʜᴀᴛ ᴡɪᴛʜ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴏꜰ ꜱɪx ᴇʏᴇꜱ.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴡʜᴏ ɪꜱ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ ⎋", url=f"https://t.me/Gojo_Satoru_botx/13"
                        ),
                        InlineKeyboardButton(
                            text="ꜰᴏʀ ᴍᴏʀᴇ 𝚀ᴜᴇʀʏ ☇", 
                            url="https://t.me/nexius_support",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="ʜᴏᴍᴇ🔙", callback_data="sagiri_back"),
                    ],
                ]
            ),
        )
    elif query.data == "sagiri_back":
        first_name = update.effective_user.first_name 
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), random.choice(Sagiri_IMG), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )


def Music_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Music_":
        query.message.edit_text(
            text=f"""
 **ʜᴇʏ   \n\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {dispatcher.bot.first_name} \n\nɪ ᴀᴍ ᴀɴ ꜰᴀꜱᴛ ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇ ᴠᴄ ᴘʟᴀʏᴇʀ ᴡɪᴛʜ 24x7 ᴀᴄᴛɪᴠᴇᴇ ꜰᴏʀ  ᴛᴇʟᴇɢʀᴀᴍ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ɢʀᴏᴜᴘꜱ \n\nꜰᴇᴇʟ ʟᴀɢ ꜰʀᴇᴇ ᴛᴏ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴇɴᴊᴏʏ ʜɪɢʜ Qᴜᴀʟɪᴛʏ ᴀᴜᴅɪᴏ ᴀɴᴅ ᴠɪᴅᴇᴏ ** 
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        
                InlineKeyboardButton(
                    text=" Aᴅᴍɪɴꜱ ",
                    callback_data="Music_1",
                ),
                InlineKeyboardButton(
                    text=" Aᴜᴛʜ ",
                    callback_data="Music_2",
                ),
            
                InlineKeyboardButton(
                    text=" Bʟᴏᴄᴋ ",
                    callback_data="Music_3",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=" G-ᴄᴀꜱᴛ ",
                    callback_data="Music_4",
                ),
                InlineKeyboardButton(
                    text=" Gʙᴀɴ ",
                    callback_data="Music_5",
                ),
                InlineKeyboardButton(
                    text=" Lʏʀɪᴄꜱ ",
                    callback_data="Music_6",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=" Pʟᴀʏʟɪꜱᴛ ",
                    callback_data="Music_7",
                ),
                InlineKeyboardButton(
                    text=" Vᴏɪᴄᴇ-ᴄʜᴀᴛ ",
                    callback_data="Music_8",
                ),
                InlineKeyboardButton(
                    text=" Pʟᴀʏ ",
                    callback_data="Music_9",
                ),
            ],   
            [
                InlineKeyboardButton(
                    text=" Sᴜᴅᴏ ",
                    callback_data="Music_10",
                ),
                InlineKeyboardButton(
                    text=" Sᴛᴀʀᴛ ",
                    callback_data="Music_11",
                ),
                InlineKeyboardButton(
                    text=" Pɪɴɢ ",
                    callback_data="Music_12",
                ),
            ],        
                    [
                        InlineKeyboardButton(text="ʜᴏᴍᴇ🔙", callback_data="sagiri_back"),
                    ],
                ]
           ),
        )
    elif query.data == "Music_1":
        query.message.edit_text(
            text=f"*» ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅꜱ «*"
            f"""


ᴊᴜsᴛ ᴀᴅᴅ ᴄ ɪɴ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜᴇᴍ ғᴏʀ ᴄʜᴀɴɴᴇʟ.

/pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.

/resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.

/skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ.

/end ᴏʀ /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.

/player : ɢᴇᴛ ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴩʟᴀʏᴇʀ ᴩᴀɴᴇʟ.

/queue : sʜᴏᴡs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ʟɪsᴛ.


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_2":
        query.message.edit_text(
            text=f"*» ᴀᴜᴛʜ ᴜsᴇʀs «*"
            f"""

ᴀᴜᴛʜ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ʙᴏᴛ ᴡɪᴛʜᴏᴜᴛ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ᴄʜᴀᴛ. [ᴀᴅᴍɪɴs ᴏɴʟʏ]

/auth [ᴜsᴇʀɴᴀᴍᴇ] : ᴀᴅᴅ ᴀ ᴜsᴇʀ ᴛᴏ ᴀᴜᴛʜ ʟɪsᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.

/unauth [ᴜsᴇʀɴᴀᴍᴇ] : ʀᴇᴍᴏᴠᴇ ᴀ ᴀᴜᴛʜ ᴜsᴇʀs ғʀᴏᴍ ᴛʜᴇ ᴀᴜᴛʜ ᴜsᴇʀs ʟɪsᴛ.

/authusers : sʜᴏᴡs ᴛʜᴇ ᴀᴜᴛʜ ᴜsᴇʀs ʟɪsᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴩ.


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_3":
        query.message.edit_text(
            text=f"*» ʙʟᴀᴄᴋʟɪsᴛ ᴄʜᴀᴛ «*"
            f""" 

ʙʟᴀᴄᴋʟɪsᴛ ғᴇᴀᴛᴜʀᴇ [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs]

/blacklistchat [ᴄʜᴀᴛ ɪᴅ] : ʙʟᴀᴄᴋʟɪsᴛ ᴀ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.

/whitelistchat [ᴄʜᴀᴛ ɪᴅ] : ᴡʜɪᴛᴇʟɪsᴛ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ.

/blacklistedchat : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs.


 ʙʟᴏᴄᴋ ᴜsᴇʀs:

/block [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴄʜᴜᴛɪʏᴀ] : sᴛᴀʀᴛs ɪɢɴᴏʀɪɴɢ ᴛʜᴇ ᴄʜᴜᴛɪʏᴀ, sᴏ ᴛʜᴀᴛ ʜᴇ ᴄᴀɴ'ᴛ ᴜsᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs.

/unblock [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ᴜɴʙʟᴏᴄᴋs ᴛʜᴇ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ.

/blockedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs.


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_4":
        query.message.edit_text(
            text=f"*» ʙʀᴏᴀᴅᴄᴀsᴛ ғᴇᴀᴛᴜʀᴇ «*"
            f"""

/broadcast , /gcast  [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ] : ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.

ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴏᴅᴇs:

-pin : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs.
-pinloud : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ sᴇɴᴅ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴛᴏ ᴛʜᴇ ᴍᴇᴍʙᴇʀs.
-user : ʙʀᴏᴀᴅᴄᴀsᴛs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʜᴇ ᴜsᴇʀs ᴡʜᴏ ʜᴀᴠᴇ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ.
-assistant : ʙʀᴏᴀᴅᴄᴀsᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴀssɪᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.
-nobot : ғᴏʀᴄᴇs ᴛʜᴇ ʙᴏᴛ ᴛᴏ ɴᴏᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ᴛʜᴇ ᴍᴇssᴀɢᴇ..

ᴇxᴀᴍᴩʟᴇ: /broadcast -user -assistant -pin ᴛᴇsᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_5":
        query.message.edit_text(
            text=f"*» ɢʙᴀɴ ғᴇᴀᴛᴜʀᴇ «*"
            f"""

/gban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴄʜᴜᴛɪʏᴀ] : ɢʟᴏʙᴀʟʟʏ ʙᴀɴs ᴛʜᴇ ᴄʜᴜᴛɪʏᴀ ғʀᴏᴍ ᴀʟʟ ᴛʜᴇ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ ʙʟᴀᴄᴋʟɪsᴛ ʜɪᴍ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.

/ungban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ᴜɴʙᴀɴs ᴛʜᴇ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ.

/gbannedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇʀ ᴜsᴇʀs.


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_6":
        query.message.edit_text(
            text=f"*» ʟʏʀɪᴄꜱ ꜰᴇᴇᴀᴛᴜʀᴇꜱ «*"
            f"""

/loop [ᴅɪsᴀʙʟᴇ/ᴇɴᴀʙʟᴇ] ᴏʀ [ʙᴇᴛᴡᴇᴇɴ 1:10] 
: ᴡʜᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʙᴏᴛ ᴡɪʟʟ ᴩʟᴀʏ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ɪɴ ʟᴏᴏᴩ ғᴏʀ 10 ᴛɪᴍᴇs ᴏʀ ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ʀᴇǫᴜᴇsᴛᴇᴅ ʟᴏᴏᴩs.

/shuffle : sʜᴜғғʟᴇ ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs.

/seek : sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ.

/seekback : ʙᴀᴄᴋᴡᴀʀᴅ sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ.

/lyrics [sᴏɴɢ ɴᴀᴍᴇ] : sᴇᴀʀᴄʜ ʟʏʀɪᴄs ғᴏʀ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ sᴏɴɢ ᴀɴᴅ sᴇɴᴅ ᴛʜᴇ ʀᴇsᴜʟᴛs.

/shayri , /love , /gf , /bf : 𝙶𝙴𝚃 𝚂𝙷𝙰𝚈𝚁𝙸 𝙵𝙾𝚁 𝙲𝙾𝚄𝙿𝙻𝙴𝚂


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_7":
        query.message.edit_text(
            text=f"*» 🎄ᴩʟᴀʏʟɪsᴛs ғᴇᴀᴛᴜʀᴇ🎄 «*"
            f"""

/playlist : ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴩʟᴀʏʟɪsᴛ ᴏɴ sᴇʀᴠᴇʀs.

/deleteplaylist : ᴅᴇʟᴇᴛᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴛʀᴀᴄᴋ ɪɴ ʏᴏᴜʀ ᴩʟᴀʏʟɪsᴛ.

/play : sᴛᴀʀᴛs ᴩʟᴀʏɪɴɢ ғʀᴏᴍ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴩʟᴀʏʟɪsᴛ ᴏɴ sᴇʀᴠᴇʀ.


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_8":
        query.message.edit_text(
            text=f"*»  ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛs «*"
            f"""

/activevoice : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛs ᴏɴ ᴛʜᴇ ʙᴏᴛ.
/activevideo : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛs ᴏɴ ʙᴏᴛ.
/autoend [ᴇɴᴀʙʟᴇ|ᴅɪsᴀʙʟᴇ] : ᴇɴᴀʙʟᴇ sᴛʀᴇᴀᴍ ᴀᴜᴛᴏ ᴇɴᴅ ɪғ ɴᴏ ᴏɴᴇ ɪs ʟɪsᴛᴇɴɪɴɢ.


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_9":
        query.message.edit_text(
            text=f"*»  ᴩʟᴀʏ ғᴇᴀᴛᴜʀᴇ  «*"
            f"""

•c sᴛᴀɴᴅs ғᴏʀ ᴄʜᴀɴɴᴇʟ ᴩʟᴀʏ.
•v sᴛᴀɴᴅs ғᴏʀ ᴠɪᴅᴇᴏ ᴩʟᴀʏ.
•force sᴛᴀɴᴅs ғᴏʀ ғᴏʀᴄᴇ ᴩʟᴀʏ.

/play ᴏʀ /vplay ᴏʀ /cplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.

/playforce ᴏʀ /vplayforce ᴏʀ /cplayforce : ғᴏʀᴄᴇ ᴩʟᴀʏ sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ.

/channelplay [ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪsᴀʙʟᴇ] : ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀ ɢʀᴏᴜᴩ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʀᴀᴄᴋs ʙʏ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴄᴏᴍᴍᴀɴᴅs sᴇɴᴛ ɪɴ ɢʀᴏᴜᴩ.


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_10":
        query.message.edit_text(
            text=f"*» 🌲ɢᴇᴛ sᴛᴀʀᴛᴇᴅ ᴡɪᴛʜ ʙᴏᴛ🌲 «*"
            f"""

 ʜᴇʀᴏᴋᴜ :

/usage : sʜᴏᴡs ᴛʜᴇ ᴅʏɴᴏ ᴜsᴀɢᴇ ᴏғ ᴛʜᴇ ᴍᴏɴᴛʜ.

 ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs:

/restart : ʀᴇsᴛᴀʀᴛs ʏᴏᴜʀ ʙᴏᴛ.

/update : ᴜᴩᴅᴀᴛᴇs ᴛʜᴇ ʙᴏᴛ ғʀᴏᴍ ᴛʜᴇ ᴜᴩsᴛʀᴇᴀᴍ ʀᴇᴩᴏ.

/speedtest : ᴄʜᴇᴄᴋ ʙᴏᴛ's sᴇʀᴠᴇʀ sᴩᴇᴇᴅ.

/maintenance [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ᴏғ ʏᴏᴜʀ ʙᴏᴛ.

/logger [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ʙᴏᴛ ᴡɪʟʟ sᴛᴀʀᴛ ʟᴏɢɢɪɴɢ ᴛʜᴇ ᴀᴄᴛɪᴠɪᴛɪᴇs ʜᴀᴩᴩᴇɴ ᴏɴ ʙᴏᴛ.

/logs [ɴᴜᴍʙᴇʀ ᴏғ ʟɪɴᴇs] : ɢᴇᴛ ʟᴏɢs ᴏғ ʏᴏᴜʀ ʙᴏᴛ [ᴅᴇғᴀᴜʟᴛ ᴠᴀʟᴜᴇ ɪs 100 ʟɪɴᴇs]



""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_11":
        query.message.edit_text(
            text=f"*» ɢᴇᴛ sᴛᴀʀᴛᴇᴅ ᴡɪᴛʜ ʙᴏᴛ «*"
            f"""

/start : sᴛᴀʀᴛs ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ.

/help : ɢᴇᴛ ʜᴇʟᴩ ᴍᴇɴᴜ ᴡɪᴛʜ ᴇxᴩʟᴀɴᴀᴛɪᴏɴ ᴏғ ᴄᴏᴍᴍᴀɴᴅs.

/reboot : ʀᴇʙᴏᴏᴛs ᴛʜᴇ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ.

/settings : sʜᴏᴡs ᴛʜᴇ ɢʀᴏᴜᴩ sᴇᴛᴛɪɴɢs ᴡɪᴛʜ ᴀɴ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ɪɴʟɪɴᴇ ᴍᴇɴᴜ.

/sudolist : sʜᴏᴡs ᴛʜᴇ sᴜᴅᴏ ᴜsᴇʀs ᴏғ ᴍᴜsɪᴄ ʙᴏᴛ.

""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ʜᴏᴍᴇ🔙", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_12":
        query.message.edit_text(
            text=f"*» ᴛᴏ ᴄʜᴇᴄᴋ ᴘɪɴɢ ᴏꜰ ʙᴏᴛ «*"
            f"""

/ping : ᴄʜᴇᴄᴋ ᴛʜᴇ ᴘɪɴɢ ᴏꜰ ᴍᴜꜱɪᴄᴄ ʙᴏᴛ .


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Music_"),
                    ]
                ]
            ),
        )        
    elif query.data == "Music_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), random.choice(Sagiri_IMG), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )


def Gojoanime_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Gojoanime_":
        query.message.edit_text(
            text=f"""
 **ᴋᴏɴɪᴄʜɪɪᴡᴀ 🍁   \n\n⋄ ʜᴇʏᴏ ᴡᴇᴇʙꜱ ɪ'ᴍ ᴛʜᴇ ꜱᴀᴛᴏʀᴜ ɢᴏᴊᴏ ᴏꜰ ꜱɪx ᴇʏᴇꜱ ! \n\n⊳ ɪ ʜᴀᴠᴇ ʟᴏᴛꜱ ᴏꜰ ꜰᴜɴ ꜰᴇᴀᴛᴜʀᴇꜱ ᴀʟꜱᴏ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀꜱ ᴀᴛᴛᴀᴄʜᴇᴅ ᴀɴɪᴍᴇ ꜰᴜɴᴄᴛɪᴏɴꜱ ꜰᴏʀ ᴏᴛᴀᴋᴜꜱ! \n\n⊳ ᴡʜɪᴄʜ ʜᴇʟᴘꜱ ᴡᴇᴇʙꜱ ᴛᴏ ꜰɪɴᴅ ᴅɪꜰꜰᴇʀᴇɴᴛ ᴛʏᴘᴇꜱ ᴏꜰ ᴀɴɪᴍᴇ & ᴍᴀɴɢᴀ ᴀʟꜱᴏ ᴘʀᴏᴠɪᴅᴇ ᴀɴɪᴍᴇ ɢɪʀʟꜱ ᴄᴏꜱᴘʟᴀʏꜱ! \n\n⊳ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀɴɪᴍᴇ, ᴛʜɪᴇʀ ᴄʜᴀʀᴀᴄᴛᴇʀꜱ & ᴍᴏʀᴇ! ** 
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        
                InlineKeyboardButton(
                    text="ᴀɪʀɪɴɢ",
                    callback_data="Gojoanime_1",
                ),
                InlineKeyboardButton(
                    text="ᴡᴀɪꜰᴜꜱ",
                    callback_data="Gojoanime_2",
                ),
            
                InlineKeyboardButton(
                    text="ʟᴇᴡᴅ",
                    callback_data="Gojoanime_3",
                ),
            ], 
            [
                InlineKeyboardButton(
                    text="ᴀɴɪᴍᴇ",
                    callback_data="Gojoanime_4",
                ),
                InlineKeyboardButton(
                    text="ᴍᴀɴɢᴀ",
                    callback_data="Gojoanime_5",
                ),
                InlineKeyboardButton(
                    text="ᴄʜᴀʀᴀᴄᴛᴇʀ",
                    callback_data="Gojoanime_6",
                ),
            ],   
                    [
                        InlineKeyboardButton(text="ʜᴏᴍᴇ🔙", callback_data="sagiri_back"),
                    ],
                ]
           ),
        )
    elif query.data == "Gojoanime_1":
        query.message.edit_text(
            text=f"*⛩ᴀɴɪᴍᴇ ꜰᴜɴᴄᴛɪᴏɴꜱ ᴏꜰ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ⛩*"
            f"""


⋄ ᴛʏᴘᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴀɴᴅ ɢᴇᴛ ɪɴꜰᴏ ᴏɴ ᴀɪʀɪɴɢ ꜱᴛᴀᴛᴜꜱ ᴏꜰ ᴀɴɪᴍᴇ 

*ꜰᴏʀ ᴇxᴀᴍᴘʟᴇ*

/airing ► /ᴀɪʀɪɴɢ ᴊᴜ ᴊᴜᴛꜱᴜ ᴋᴀɪꜱᴇɴ

◬ɴᴏᴛᴇ  ► ᴛʏᴘᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ 𝚀ᴜᴇʀʏ ɪɴ ɴᴏʀᴍᴀʟ ꜰᴏɴᴛꜱ!


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Gojoanime_"),
                    ]
                ]
            ),
        )
    elif query.data == "Gojoanime_2":
        query.message.edit_text(
            text=f"*⛩ᴀɴɪᴍᴇ ꜰᴜɴᴄᴛɪᴏɴꜱ ᴏꜰ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ⛩*"
            f"""

⋄ ᴛᴏ ɢᴇᴛ ʀᴀɴᴅᴏᴍ ɪᴍᴀɢᴇꜱ ᴏꜰ ᴡᴀɪꜰᴜ'ꜱ ʟɪᴋᴇ :-

/ꜱʜɪɴᴏʙᴜ               /ꜱᴍɪʟᴇ
/ꜰᴏxɢɪʀʟ               /ʜᴀᴘᴘʏ
/ᴡᴀɪꜰᴜꜱ                /ᴅᴀɴᴄᴇ
/ɴᴇᴋᴏ                   /ʙɪᴛᴇ
/ᴀᴡᴏᴏ                  /ᴡɪɴᴋ

ꜰᴏʀ ᴇxᴀᴍᴘʟᴇ

► /shinobu

◬ɴᴏᴛᴇ  ► ᴛʏᴘᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ 𝚀ᴜᴇʀʏ ɪɴ ɴᴏʀᴍᴀʟ ꜰᴏɴᴛꜱ!

""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Gojoanime_"),
                    ]
                ]
            ),
        )
    elif query.data == "Gojoanime_3":
        query.message.edit_text(
            text=f"*⛩ᴀɴɪᴍᴇ ꜰᴜɴᴄᴛɪᴏɴꜱ ᴏꜰ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ⛩*"
            f""" 

⋄ ᴛʀʏ ᴛʜɪꜱ ᴇxᴄʟᴜꜱɪᴠᴇ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɢᴇᴛ ᴘɪᴄᴛᴜʀᴇꜱ ᴏꜰ ᴀɴɪᴍᴇ ᴄᴏꜱᴘʟᴀʏᴇʀꜱ!

ꜰᴏʀ ᴇxᴀᴍᴘʟᴇ

/ᴄᴏꜱᴘʟᴀʏ ► ᴛᴏ ɢᴇᴛ ɪᴍᴀɢᴇꜱ ᴏꜰ ᴀɴɪᴍᴇ ɢɪʀʟꜱ ᴄᴏꜱᴘʟᴀʏᴇʀꜱ.

/ʟᴇᴡᴅ ► ᴛᴏ ɢᴇᴛ 18+ ɪᴍᴀɢᴇꜱ ᴏꜰ ᴀɴɪᴍᴇ  ɢɪʀʟ ᴄᴏꜱᴘʟᴀʏᴇʀꜱ.

◬ ɴᴏᴛᴇ  ► ᴛʏᴘᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ 𝚀ᴜᴇʀʏ ɪɴ ɴᴏʀᴍᴀʟ ꜰᴏɴᴛꜱ!


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ʜᴏᴍᴇ🔙", callback_data="Gojoanime_"),
                    ]
                ]
            ),
        )
    elif query.data == "Gojoanime_4":
        query.message.edit_text(
            text=f"*⛩ᴀɴɪᴍᴇ ꜰᴜɴᴄᴛɪᴏɴꜱ ᴏꜰ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ⛩*"
            f"""

⋄ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɢᴇᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀɴʏ ᴀɴɪᴍᴇ

ꜰᴏʀ ᴇxᴀᴍᴘʟᴇ

/anime ► /ᴀɴɪᴍᴇ ᴊᴜꜱ ᴊᴜᴛꜱᴜ ᴋᴀɪꜱᴇɴ

◬ ɴᴏᴛᴇ  ► ᴛʏᴘᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ 𝚀ᴜᴇʀʏ ɪɴ ɴᴏʀᴍᴀʟ ꜰᴏɴᴛꜱ!


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Gojoanime_"),
                    ]
                ]
            ),
        )
    elif query.data == "Gojoanime_5":
        query.message.edit_text(
            text=f"*⛩ᴀɴɪᴍᴇ ꜰᴜɴᴄᴛɪᴏɴꜱ ᴏꜰ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ⛩*"
            f"""

⋄ ᴛʀʏ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɢᴇᴛ ᴋɴᴏᴡʟᴇᴅɢᴇ ᴀʙᴏᴜᴛ ᴀɴɢ ᴋɪɴᴅ ᴏꜰ ᴍᴀɴɢᴀ

ꜰᴏʀ ᴇxᴀᴍᴘʟᴇ

/manga ► /ᴍᴀɴɢᴀ ᴏɴᴇ ᴘᴜɴᴄʜ ᴍᴀɴ

◬ ɴᴏᴛᴇ  ► ᴛʏᴘᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ 𝚀ᴜᴇʀʏ ɪɴ ɴᴏʀᴍᴀʟ ꜰᴏɴᴛꜱ!


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Gojoanime_"),
                    ]
                ]
            ),
        )
    elif query.data == "Gojoanime_6":
        query.message.edit_text(
            text=f"*⛩ᴀɴɪᴍᴇ ꜰᴜɴᴄᴛɪᴏɴꜱ ᴏꜰ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ⛩*"
            f"""

⋄ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɢᴇᴛ ɪɴꜰᴏ ᴀʙᴏᴜᴛ ᴀɴɪᴍᴇ & ᴍᴀɴɢᴀ ᴄʜᴀʀᴀᴄᴛᴇʀꜱ!

ꜰᴏʀ ᴇxᴀᴍᴘʟᴇ

/character ► /ᴄʜᴀʀᴀᴄᴛᴇʀ ɢᴏᴊᴏ ꜱᴀᴛᴏʀᴜ

◬ ɴᴏᴛᴇ  ► ᴛʏᴘᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ 𝚀ᴜᴇʀʏ ɪɴ ɴᴏʀᴍᴀʟ ꜰᴏɴᴛꜱ!


""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔙ʙᴀᴄᴋ", callback_data="Gojoanime_"),
                    ]
                ]
            ),
        )  
    elif query.data == "Gojoanime_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), random.choice(Sagiri_IMG), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )     

                        
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=" ʜᴇʟᴘ ",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "» ᴄʜᴏᴏꜱᴇ ᴀɴ.ᴏᴘᴛɪᴏɴ ꜰᴏʀ ɢᴇᴛᴛɪɴɢ ʜᴇʟᴘ ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="G𝙴ᴛ ʜᴇʟᴘ",
                            url="https://t.me/{}?start=help".format(
                                context.bot.username
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="H𝙴ʟᴘ ᴍᴇɴᴜ",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="◁",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sᴇᴛᴛɪɴɢs​",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != {OWNER_ID} and DONATION_LINK:
            update.effective_message.reply_text(
                f"» ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴏғ {dispatcher.bot.first_name} sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪs [PIRO OWNER](tg://user?id={OWNER_ID})"
                f"\n\nʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴩᴇʀsᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ : [ʜᴇʀᴇ]({DONATION_LINK})",
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "ɪ'ᴠᴇ ᴘᴍ'ᴇᴅ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪɴɢ ᴛᴏ ᴍʏ ᴄʀᴇᴀᴛᴏʀ!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғɪʀsᴛ ᴛᴏ ɢᴇᴛ ᴅᴏɴᴀᴛɪᴏɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendAnimation(
                f"@Gojo_support_chat",
                animation="https://telegra.ph/file/884a4158f0d0b56105e3b.mp4",
                caption=f"""
ㅤ 🧃ㅤ{dispatcher.bot.first_name} ɪs ᴀʟɪᴠᴇ.

 ✠ᚚᚚᚚᚚᚚᚚᚚᚚᚚᚚᚚᚚᚚᚚᚚᚚᚚᚚᚚ☇
  🫧 ᴍʏ ᴏᴡɴᴇʀ : [𝙶ᴏᴊᴏ ꜱᴀᴛᴏʀᴜ](https://t.me/Gojo_Satoru_botx)
  ◎ **ᴘʏᴛʜᴏɴ :** `{y()}`
  ◎ **ʟɪʙʀᴀʀʏ :** `{telever}`
  ◎ **ᴛᴇʟᴇᴛʜᴏɴ :** `{tlhver}`
  ◎ **ᴩʏʀᴏɢʀᴀᴍ :** `{pyrover}`
  ◎ **ʙᴏᴛ ᴠᴇʀꜱɪᴏɴ :** 1.0
∝╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺╺⟳

""",
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @Gojo_support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    CommandHandler("test", test)
    start_handler = CommandHandler("start", start)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(
        Sagiri_about_callback, pattern=r"sagiri_"
    )
    Music_callback_handler = CallbackQueryHandler(
        Music_about_callback, pattern=r"Music_"
    )
    Gojoanime_callback_handler = CallbackQueryHandler(
        Gojoanime_about_callback, pattern=r"Gojoanime_"
    )
    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(Music_callback_handler)
    dispatcher.add_handler(Gojoanime_callback_handler)  
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    LOGGER.info("🌹𝐁𝐎𝐓 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐔🌱\n\n╔═════ஜ۩۞۩ஜ════╗\n\nmade by anonymous and jashan\n\n╚═════ஜ۩۞۩ஜ════╝")
    updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
