# import the needed libraries
from telegram.ext.updater import Updater
from telegram.ext import CallbackQueryHandler
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from text import text_price
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# keyboard options for different menus
updater = Updater("6101394042:AAFxN5cS-sKG7dJrkN2RwWXSudoUd9qURHo", use_context=True)
kbd_layout = [["دسته بندی", "ثبت آگهی"], ["آگهی های من", "قیمت آگهی ها"], ["پشتیبانی"]]
kbd = ReplyKeyboardMarkup(kbd_layout, resize_keyboard=True)


menu_options_group = [
    {"name": "دروس دانشگاه", "callback_data_group": "1"},
    {"name": "برنامه نویسی", "callback_data_group": "2"},
    {"name": "سایت نویسی", "callback_data_group": "3"},
    {"name": "طراح گرافیک ", "callback_data_group": "4"},
]
menu_options_agahi = [
    {"name": "انجام دهنده", "callback_data": "option1"},
    {"name": "درخواست کننده", "callback_data": "option2"},
]


# start command function
def start(update: Update, context: CallbackContext):
    print("/start called")
    update.message.reply_text(
        "به بات کانال Wedo  خوش آمدید! ,از /help برای مشاهده دستورات استفاده کنید و براس ثبت آگهی از منو استفاده کنید."
    )
    update.message.reply_text(
        text="از منو برا ثبت آگهی استفاده کنید:", reply_markup=kbd
    )


# handler for keyboard menu options
def messagehandler(update: Update, context: CallbackContext):
    #show sent messages in console
    print(update.message.chat.username, "sent a message")

    if "ثبت آگهی" in update.message.text:
        menu_keyboard = [
            [
                InlineKeyboardButton(
                    option["name"], callback_data=option["callback_data"]
                )
            ]
            for option in menu_options_agahi
        ]
        # Create an InlineKeyboardMarkup object from the menu keyboard
        menu_markup = InlineKeyboardMarkup(menu_keyboard)
        # Send the menu to the user
        update.message.reply_text(
            "نوع آگهی خود را انتخاب کنید:", reply_markup=menu_markup
        )
    elif "دسته بندی" in update.message.text:
        menu_keyboard = [
            [
                InlineKeyboardButton(
                    option["name"], callback_data=option["callback_data_group"]
                )
            ]
            for option in menu_options_group
        ]
        # Create an InlineKeyboardMarkup object from the menu keyboard
        menu_markup = InlineKeyboardMarkup(menu_keyboard)
        # Send the menu to the user
        update.message.reply_text(":دسته بندی پروژه ها", reply_markup=menu_markup)
    elif "آگهی های من" in update.message.text:
        update.message.reply_text(text="آگهی های من")
    elif "قیمت آگهی ها" in update.message.text:
        update.message.reply_text(text=text_price)
    elif "پشتیبانی" in update.message.text:
        update.message.reply_text(text="پشتیبانی")


def menu_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    # Find the selected menu option
    try:
        selected_option = next(
            (
                option
                for option in menu_options_agahi
                if option["callback_data"] == data
            ),
            None,
        )
        if selected_option:`
            # Send a message to the user with the selected option
            query.edit_message_text(f"آگهی شما {selected_option['name']} است.")
            menu_keyboard = [
            [
                InlineKeyboardButton(
                    option["name"], callback_data=option["callback_data_group"]
                )
            ]
            for option in menu_options_group
            ]
            # Create an InlineKeyboardMarkup object from the menu keyboard
            menu_markup = InlineKeyboardMarkup(menu_keyboard)
            # Send the menu to the user
            query.edit_message_text(" دسته بندی پروژه خود را انتخاب کنید:", reply_markup=menu_markup)
    except Exception as e:
        print(e)
    try:
        selected_option = next(
            (
                option
                for option in menu_options_group
                if option["callback_data_group"] == data
            ),
            None,
        )
        if selected_option:
            # Send a message to the user with the selected option
            query.edit_message_text(f"دسته بندی {selected_option['name']}")
    except:
        print("fail")


def help(update: Update, context):
    update.message.reply_text(
        """دستورات بات:
/youtube - لینک یوتیوب
/linkedin - اکانت لینکدین
/gmail - آدرس جیمیل
/url - آدرس وب سایت"""
    )


def gmail_url(update: Update, context):
    update.message.reply_text("Gmail ==> Wedo@Gmail.com")


def youtube_url(update: Update, context):
    update.message.reply_text("Youtube Link ==> https://www.youtube.com/Wedo")


def linkedIn_url(update: Update, context):
    update.message.reply_text("LinkedIn URL ==> https://www.linkedin.com/in/Wedo/")


def WEB_SITE(update: Update, context):
    update.message.reply_text("Website URL ==> https://www.Wedo.com")


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("youtube", youtube_url))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("linkedin", linkedIn_url))
updater.dispatcher.add_handler(CommandHandler("gmail", gmail_url))
updater.dispatcher.add_handler(CommandHandler("url", WEB_SITE))
updater.dispatcher.add_handler(MessageHandler(Filters.text, messagehandler))
updater.dispatcher.add_handler(CallbackQueryHandler(menu_callback))


updater.start_polling()
