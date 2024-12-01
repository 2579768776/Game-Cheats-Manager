import gettext
import json
import locale
import os
import re
import shutil
import sys
import tempfile

import pinyin
import polib


# All resources in development mode are relative to `src` folder
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        full_path = os.path.join(sys._MEIPASS, relative_path)
    else:
        full_path = os.path.join(os.path.dirname(__file__), '..', relative_path)

    if not os.path.exists(full_path):
        resource_name = os.path.basename(relative_path)
        formatted_message = tr("Couldn't find {missing_resource}. Please try reinstalling the application.").format(missing_resource=resource_name)
        raise FileNotFoundError(formatted_message)

    return full_path


def apply_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def load_settings():
    locale.setlocale(locale.LC_ALL, '')
    system_locale = locale.getlocale()[0]
    locale_mapping = {
        "English_United States": "en_US",
        "Chinese (Simplified)_China": "zh_CN",
        "Chinese (Simplified)_Hong Kong SAR": "zh_CN",
        "Chinese (Simplified)_Macao SAR": "zh_CN",
        "Chinese (Simplified)_Singapore": "zh_CN",
        "Chinese (Traditional)_Hong Kong SAR": "zh_TW",
        "Chinese (Traditional)_Macao SAR": "zh_TW",
        "Chinese (Traditional)_Taiwan": "zh_TW"
    }
    app_locale = locale_mapping.get(system_locale, 'en_US')

    default_settings = {
        "downloadPath": os.path.join(os.environ["APPDATA"], "GCM Trainers"),
        "language": app_locale,
        "theme": "black",
        "enSearchResults": False,
        "appUpdate": True,
        "autoStart": False,
        "showWarning": True,

        # Trainer management configs
        "downloadServer": "intl",
        "removeBgMusic": True,
        "autoUpdateDatabase": True,
        "autoUpdateFling": True,
        "enableXiaoxing": True,
        "weModPath": wemod_install_path,
        "cePath": ce_install_path
    }

    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except Exception as e:
        print("Error loading settings json" + str(e))
        settings = default_settings

    for key, value in default_settings.items():
        settings.setdefault(key, value)

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

    return settings


def get_translator():
    if not hasattr(sys, 'frozen'):
        for root, dirs, files in os.walk(resource_path("locale/")):
            for file in files:
                if file.endswith(".po"):
                    po = polib.pofile(os.path.join(root, file))
                    po.save_as_mofile(os.path.join(root, os.path.splitext(file)[0] + ".mo"))

    lang = settings["language"]
    gettext.bindtextdomain("Game Cheats Manager", resource_path("locale/"))
    gettext.textdomain("Game Cheats Manager")
    lang = gettext.translation("Game Cheats Manager", resource_path("locale/"), languages=[lang])
    lang.install()
    return lang.gettext


def is_chinese(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False


def sort_trainers_key(name):
    if is_chinese(name):
        return pinyin.get(name, format="strip", delimiter=" ")
    return name


def ensure_trainer_details_exist():
    dst = os.path.join(DATABASE_PATH, "xgqdetail.json")
    if not os.path.exists(dst):
        shutil.copyfile(resource_path("dependency/xgqdetail.json"), dst)


def ensure_trainer_download_path_is_valid():
    try:
        os.makedirs(settings["downloadPath"], exist_ok=True)
    except Exception:
        settings["downloadPath"] = os.path.join(os.environ["APPDATA"], "GCM Trainers")
        apply_settings(settings)
        os.makedirs(settings["downloadPath"], exist_ok=True)


def findCEInstallPath():
    base_path = r'C:\Program Files'
    latest_version = []
    latest_path = None

    if os.path.exists(base_path):
        for folder in os.listdir(base_path):
            if folder.startswith("Cheat Engine"):
                match = re.search(r"Cheat Engine (\d+(?:\.\d+)*)", folder)
                if match:
                    # Parse version into a list of integers (e.g., '7.5.1' -> [7, 5, 1])
                    version = list(map(int, match.group(1).split('.')))
                    while len(version) < 3:
                        version.append(0)
                    if version > latest_version:
                        latest_version = version
                        latest_path = os.path.join(base_path, folder)

    return latest_path


setting_path = os.path.join(os.environ["APPDATA"], "GCM Settings")
os.makedirs(setting_path, exist_ok=True)

SETTINGS_FILE = os.path.join(setting_path, "settings.json")
DATABASE_PATH = os.path.join(setting_path, "db")
os.makedirs(DATABASE_PATH, exist_ok=True)
DOWNLOAD_TEMP_DIR = os.path.join(tempfile.gettempdir(), "GameCheatsManagerTemp", "download")
VERSION_TEMP_DIR = os.path.join(tempfile.gettempdir(), "GameCheatsManagerTemp", "version")
WEMOD_TEMP_DIR = os.path.join(tempfile.gettempdir(), "GameCheatsManagerTemp", "wemod")

wemod_install_path = os.path.join(os.environ["LOCALAPPDATA"], "WeMod")
ce_install_path = findCEInstallPath()

settings = load_settings()
tr = get_translator()

ensure_trainer_details_exist()
ensure_trainer_download_path_is_valid()

if settings["theme"] == "black":
    dropDownArrow_path = resource_path("assets/dropdown-white.png").replace("\\", "/")
elif settings["theme"] == "white":
    dropDownArrow_path = resource_path("assets/dropdown-black.png").replace("\\", "/")
upArrow_path = resource_path("assets/up.png").replace("\\", "/")
downArrow_path = resource_path("assets/down.png").replace("\\", "/")
leftArrow_path = resource_path("assets/left.png").replace("\\", "/")
rightArrow_path = resource_path("assets/right.png").replace("\\", "/")
resourceHacker_path = resource_path("dependency/ResourceHacker.exe")
unzip_path = resource_path("dependency/7z/7z.exe")
binmay_path = resource_path("dependency/binmay.exe")
emptyMidi_path = resource_path("dependency/TrainerBGM.mid")
elevator_path = resource_path("dependency/Elevate.exe")
search_path = resource_path("assets/search.png")

language_options = {
    "English (US)": "en_US",
    "简体中文": "zh_CN",
    "繁體中文": "zh_TW"
}

theme_options = {
    tr("Black"): "black",
    tr("white"): "white"
}

server_options = {
    tr("International"): "intl",
    tr("China") + tr(" (Some trainers cannot be downloaded)"): "china"
}

font_config = {
    "en_US": resource_path("assets/NotoSans-Regular.ttf"),
    "zh_CN": resource_path("assets/NotoSansSC-Regular.ttf"),
    "zh_TW": resource_path("assets/NotoSansTC-Regular.ttf")
}
