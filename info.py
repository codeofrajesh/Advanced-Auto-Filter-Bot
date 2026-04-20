import re
import os
from os import environ, getenv

from dotenv import load_dotenv
load_dotenv()

from Script import script
id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


SESSION = environ.get('SESSION', 'media_search')
API_ID = int(environ.get('API_ID', '35057086'))
API_HASH = environ.get('API_HASH', '344c241bb482993a8b318848421319f3')
BOT_TOKEN = environ.get('BOT_TOKEN', "8797721372:AAFt-cO74ja4qihp4xQw0QVLHTzHLgqc4to")

CACHE_TIME = int(environ.get('CACHE_TIME', 600))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

PICS = (environ.get('PICS', 'https://i.ibb.co/ch3n9wsf/x.jpg')).split() 
NOR_IMG = environ.get("NOR_IMG", "https://graph.org/file/62efbcc4e7580b76530ba.jpg")
MELCOW_VID = environ.get("MELCOW_VID", "https://graph.org/file/e215d12bfd4fa2155e90e.mp4")
SPELL_IMG = environ.get("SPELL_IMG", "https://graph.org/file/13702ae26fb05df52667c.jpg")
SUBSCRIPTION = (environ.get('SUBSCRIPTION', 'https://telegra.ph/file/f983d857f3ce40795e4b8.jpg'))
FSUB_IMG = (environ.get('FSUB_IMG', 'https://i.ibb.co/cShkPjcZ/x.jpg')).split() 

ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '7811733658').split()] 
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1003879025493').split()]
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1003830765716'))  
BIN_CHANNEL = int(environ.get('BIN_CHANNEL', '-1003955878897'))  
MOVIE_UPDATE_CHANNEL = int(environ.get('MOVIE_UPDATE_CHANNEL', '-1003617164211'))  
PREMIUM_LOGS = int(environ.get('PREMIUM_LOGS', '-1003389032197')) 
auth_grp = environ.get('AUTH_GROUP')
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None
reqst_channel = environ.get('REQST_CHANNEL_ID', '-1003626780031') 
REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None
support_chat_id = environ.get('SUPPORT_CHAT_ID', '-1003835943477') 
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None

DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://Devil:Devil01@cluster0.ubtq55d.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = environ.get('DATABASE_NAME', "SMS_Movies")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'SilentXBotz_files')

# If MULTIPLE_DB Is True Then Fill DATABASE_URI2 Value Else You Will Get Error.
MULTIPLE_DB = is_enabled(os.environ.get('MULTIPLE_DB', "False"), True) # Type True For Turn On MULTIPLE DB FUNTION 
DATABASE_URI2 = environ.get('DATABASE_URI2', "")
DB_CHANGE_LIMIT = int(environ.get('DB_CHANGE_LIMIT', "432")) 

GRP_LNK = environ.get('GRP_LNK', 'https://t.me/SparkX_MRTech')
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/SparkX_MR_Tech')
OWNER_LNK = environ.get('OWNER_LNK', 'https://t.me/MR_TechRobot')
UPDATE_CHANNEL_LNK = environ.get('UPDATE_CHANNEL_LNK', 'https://t.me/Movie_Flix_SMS')

AUTH_CHANNEL = environ.get("AUTH_CHANNEL", "-1003786228829") # add multiple channels here, separated by single space
AUTH_REQ_CHANNEL = environ.get('AUTH_REQ_CHANNEL', '-1003715330284')

IS_VERIFY = is_enabled('IS_VERIFY', False)
LOG_VR_CHANNEL = int(environ.get('LOG_VR_CHANNEL', '-1003820681956'))
LOG_API_CHANNEL = int(environ.get('LOG_API_CHANNEL', '-1003595418056'))
VERIFY_IMG = environ.get("VERIFY_IMG", "https://telegra.ph/file/9ecc5d6e4df5b83424896.jpg")

TUTORIAL = environ.get("TUTORIAL", "https://youtube.com/shorts/b0ynxP9Ybfc")
TUTORIAL_2 = environ.get("TUTORIAL_2", "https://youtube.com/shorts/b0ynxP9Ybfc")
TUTORIAL_3 = environ.get("TUTORIAL_3", "https://youtube.com/shorts/b0ynxP9Ybfc")

SHORTENER_API = environ.get("SHORTENER_API", "055917691bbc26774e10e1f1dea4c828580225ec")
SHORTENER_WEBSITE = environ.get("SHORTENER_WEBSITE", "arolinks.com")

SHORTENER_API2 = environ.get("SHORTENER_API2", "055917691bbc26774e10e1f1dea4c828580225ec")
SHORTENER_WEBSITE2 = environ.get("SHORTENER_WEBSITE2", "arolinks.com")

SHORTENER_API3 = environ.get("SHORTENER_API3", "055917691bbc26774e10e1f1dea4c828580225ec")
SHORTENER_WEBSITE3 = environ.get("SHORTENER_WEBSITE3", "arolinks.com")

TWO_VERIFY_GAP = int(environ.get('TWO_VERIFY_GAP', "12800"))
THREE_VERIFY_GAP = int(environ.get('THREE_VERIFY_GAP', "54000"))

MOVIE_UPDATE_NOTIFICATION = bool(environ.get("MOVIE_UPDATE_NOTIFICATION", True))
NO_RESULTS_MSG = bool(environ.get("NO_RESULTS_MSG", True))
MAX_B_TN = environ.get("MAX_B_TN", "8")
MAX_BTN = is_enabled((environ.get('MAX_BTN', "True")), True)
PORT = environ.get("PORT", "8080")
MSG_ALRT = environ.get('MSG_ALRT', 'Share & Support Us ♥️ Spark X - MR Tech')
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'https://t.me/SparkX_MRTech') 
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
IMDB = is_enabled((environ.get('IMDB', "True")), False)
AUTO_FFILTER = is_enabled((environ.get('AUTO_FFILTER', "True")), True)
AUTO_DELETE = is_enabled((environ.get('AUTO_DELETE', "True")), True)
AUTO_DELETE_TIME = int(environ.get("AUTO_DELETE_TIME", "600"))  
BUTTON_MODE = is_enabled((environ.get('BUTTON_MODE', "True")), True)
IS_LANDSCAPE_POSTER = is_enabled((environ.get('IS_LANDSCAPE_POSTER', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", f"{script.IMDB_TEMPLATE_TXT}")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = int(environ.get("MAX_LIST_ELM") or 10) or None # Maximum number of elements in a list (default: 10, set 0 for no limit)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '-1003358666263')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "False")), False)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), True)
PM_SEARCH = bool(environ.get('PM_SEARCH', True)) 
EMOJI_MODE = bool(environ.get('EMOJI_MODE', True)) 
PAID_STREAM = bool(environ.get('PAID_STREAM', False)) 
STREAM_MODE = bool(environ.get('STREAM_MODE', True))
MAINTENANCE_MODE = bool(environ.get('MAINTENANCE_MODE', False)) 

IGNORE_WORDS = (list(os.environ.get("IGNORE_WORDS").split(",")) if os.environ.get("IGNORE_WORDS") else []) #Remove Words While Searching Files
IGNORE_WORDS = [
    "movies", "movie", "episode", "episodes", "south indian", "south indian movie",
    "south movie", "south indian", "web-series", "web series", "webseries", "hindi me bhejo",
    "ful", ",", "!", "kro", "jaldi", "audio", "language", "mkv", "mp4", "web", "series",
    "hollywood", "all", "bollywood", "south", "hd", "karo", "upload", "bhejo",
    "fullepisode", "please", "plz", "send", "link", "dabbed", "dubbed", "season",
]

BAD_WORDS = [
    "Hdhub4u", "cinevood", "skymoviedHD", "skymovieshd", "filmyzilla", "filmywap", 
    "filmyhit", "moviesda", "tamilyogi", "isaimini", "tamilrockers", "tamilblasters",
    "mkvmoviespoint", "mkvcinemas", "bolly4u", "9xmovies", "worldfree4u", "khatrimaza",
    "pagalworld", "pagalmovies", "jio rockers", "teluguwap", "moviezwap", "dvdvilla",
    "ssr movies", "vegamovies", "moviesflix", "hdmovieshub", "hdhub4u", "hdpopcorns",
    "moviescounter", "coolmoviez", "fzmovies", "netnaija", "wawacity", "zone-telechargement",
    "rarbg", "tigole", "qxit", "pxhd", "psa", "joy", "utr", "dtone", "mzabi", "chd",
    "hon3y", "sparks", "shaanig", "daddy", "mkvcage", "yify", "yts", "ettv", "eztv",
    "torrenting", "galaxyrg", "galaxtyy", "cpg", "propers", "remux", "webrip", "hdtv",
    "official", "original", "dubbed", "dual audio", "multi audio", "hq", "hdrip",
    "predvd", "dvdscr", "hdts", "camrip", "hdcam", "hdrip", "brrip", "bdrip",
]

LANGUAGES = ["malayalam", "mal", "tamil", "tam", "english", "eng", "hindi", "hin", "telugu", "tel", "kannada", "kan", "gujarati", "guj", "marathi", "mar", "punjabi", "pun"]
QUALITIES = ["360P", "", "480P", "", "560P", "", "720P", "", "1080P", "", "1440P", "", "2160P", ""]
SEASONS = ["Season 1", "S01", "Season 2", "S02", "Season 3", "S03", "Season 4", "S04", "Season 5", "S05", "Season 6", "S06", "Season 7", "S07", "Season 8", "S08", "Season 9", "S09", "Season 10", "S10"]


NO_PORT = bool(environ.get('NO_PORT', False))
APP_NAME = None
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = environ.get('APP_NAME')
else:
    ON_HEROKU = False
BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', 'SparkXMoviesBot.onrender.com'))
FQDN = str(getenv('FQDN', BIND_ADRESS)) if not ON_HEROKU or getenv('FQDN') else APP_NAME+'.herokuapp.com'
URL = "https://{}/".format(FQDN) if ON_HEROKU or NO_PORT else "https://{}/".format(FQDN, PORT)
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
WORKERS = int(environ.get('WORKERS', '4'))
SESSION_NAME = str(environ.get('SESSION_NAME', 'SilentXBotz'))
MULTI_CLIENT = False
name = str(environ.get('name', 'SilentX'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = str(getenv('APP_NAME'))
else:
    ON_HEROKU = False
HAS_SSL = bool(getenv('HAS_SSL', False))
if HAS_SSL:
    URL = "https://{}/".format(FQDN)
else:
    URL = "http://{}/".format(FQDN)


REACTIONS = ["🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡", "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"]

STAR_PREMIUM_PLANS = {
    1: "7day",
    30: "15day",    
    60: "1month", 
    120: "2month",   
}

Bot_cmds = {
    "start": "ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ",
    "trendlist": "ɢᴇᴛ ᴛᴏᴘ ꜱᴇᴀʀᴄʜ ʟɪꜱᴛ",
    "myplan" : "ᴄʜᴇᴄᴋ ᴘʀᴇᴍɪᴜᴍ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ",
    "plan" :"ᴄʜᴇᴄᴋ ᴘʀᴇᴍɪᴜᴍ ᴘʀɪᴄᴇ",
    "settings": "ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs",
    "group_cmd": "ᴅᴇʟᴇᴛᴇ ᴀ ꜱᴘᴇᴄɪꜰɪᴄ ꜰɪʟᴇ ꜰʀᴏᴍ ᴅʙ.",
    "admin_cmd": "ᴅᴇʟᴇᴛᴇ ᴀ ꜱᴘᴇᴄɪꜰɪᴄ ꜰɪʟᴇ ꜰʀᴏᴍ ᴅʙ.",
    "details": "ꜱᴇᴇ ɢʀᴏᴜᴘ ꜱᴇᴛᴛɪɴɢꜱ",
    "reset_group": "ʀᴇꜱᴇᴛ ɢʀᴏᴜᴘ ꜱᴇᴛᴛɪɴɢꜱ", 
    "stats": "ᴄʜᴇᴄᴋ ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ.",
    "delete": "ᴅᴇʟᴇᴛᴇ ᴀ ꜱᴘᴇᴄɪꜰɪᴄ ꜰɪʟᴇ ꜰʀᴏᴍ ᴅʙ.",
    "movie_update": "ᴏɴ ᴏғғ ᴀᴄᴄᴏʀᴅɪɴɢ ʏᴏᴜʀ ɴᴇᴇᴅᴇᴅ...",
    "pm_search": "ᴘᴍ sᴇᴀʀᴄʜ ᴏɴ ᴏғғ ᴀᴄᴄᴏʀᴅɪɴɢ ʏᴏᴜʀ ɴᴇᴇᴅᴇᴅ...",
    "restart": "ʀᴇꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ."
}

#Don't Change Anything Here

if MULTIPLE_DB == False:
    DATABASE_URI = DATABASE_URI
    DATABASE_URI2 = DATABASE_URI
else:
    DATABASE_URI = DATABASE_URI
    DATABASE_URI2 = DATABASE_URI2

AUTH_CHANNEL = [int(ch) for ch in AUTH_CHANNEL.strip().split()] if AUTH_CHANNEL else []
AUTH_REQ_CHANNEL = [int(ch) for ch in AUTH_REQ_CHANNEL.strip().split()] if AUTH_REQ_CHANNEL else []
