from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums 

class BUTTONS(object):
    ABUTTON = [
    [
        InlineKeyboardButton("⌯ sᴜᴘᴘᴏꝛᴛ ⌯", url="https://t.me/kedi_update"),
        InlineKeyboardButton("⌯ ᴜᴘᴅᴧᴛᴇ ⌯", url="https://t.me/Sprzn_arora_appeal")
    ],
    [
        InlineKeyboardButton("⌯ sᴏᴜʀᴄᴇ ⌯", callback_data="gib_source"),
        InlineKeyboardButton("⌯ ʙᴀᴄᴋ ⌯", callback_data=f"settingsback_helper")
    ]
    ]

    UBUTTON = [[InlineKeyboardButton("⌯ ᴍᴜsɪᴄ ⌯", callback_data="settings_back_helper"),InlineKeyboardButton("⌯ ᴛᴏᴏʟs ⌯", callback_data=f"tbot_cb")],[InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data=f"settingsback_helper"),
    ]]

    TBUTTON = [[InlineKeyboardButton("⌯ ᴀᴄᴛɪᴠᴇ ⌯", callback_data="cplus HELP_active"),InlineKeyboardButton("⌯ ᴀᴜᴛʜ ⌯", callback_data="cplus HELP_auth"),InlineKeyboardButton("⌯ ʙʟᴏᴄᴋ ⌯", callback_data="cplus HELP_block")],[InlineKeyboardButton("⌯ ᴄʜᴀᴛ ʙᴏᴛ ⌯", callback_data="cplus HELP_chat"),
    InlineKeyboardButton("⌯ ɢ-ᴄᴀsᴛ ⌯", callback_data="cplus HELP_gcast")],[InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data=f"ubot_cb"),
    ]]
