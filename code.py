# import the needed libraries
from telegram.update import Update
from telegram.ext.updater import Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
import sqlite3
import json
import re

channelid='-1001825834732'
supportgroupid='-962336869'

# Variables
support = False
text_con = False
type_con = False
cat_con = False
cat_con2 = False
cat_con2_search = False
user_con = False
cat2 = ""
rules=False
agahis = []
category = ""
type_1 = ""
count = 0
swear = json.load(open("swear.json",encoding='UTF-8'))
count_agahi = 0
new_count = 0
cat_con_search = False

# our database file
DB_FILE = "wedoo.db"

# Create a connection to the database and check connection
try:
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    print("Connected to Database successfully...")
except Exception as e:
    print(e)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()
textrule="""
⛔ حتما مطالعه شود⛔

🚨قوانین ثبت آگهی:

متن آگهی فقط باید برای یک خواسته و نیازمندی باشه یعنی نمیتونی چندتا موضوع مختلف رو توی یه آگهی ثبت کنی. و رعایت موارد زیر نیز الزامی است:

1️⃣ متن آگهی استفاده از لینک و موارد تبلیغاتی مجاز نیست!

2️⃣ گرفتن تست غیر مجاز است.

3️⃣  استفاده از کلمات مستجهن و توهین آمیز ممنوع است.

4️⃣ درج آگهی امتحان ممنوع است و درصورت درج توسط پشتیبانی حذف می‌گردد.


5️⃣ برای درج آگهی توانایی های خود، آگهی استخدامی یا انجام پروژه توسط تیم ویدوو به پشتیبانی پیام دهید.
🆔 @WeDoo_support1



🛑 در صورتی که آگهی تون قوانین ذکر شده رو رعایت نکرده باشه و راهکار پرداختی شما غیر از موارد فوق باشد
مجموعه ویدوو هیچ مسئولیتی در قبال وجه پرداختی شما ندارد 🛑"""

text_price = """⛔ اطلاعیه: تمامی خدمات تا 15 شهریورماه رایگان میباشد ⛔

🟪 تعرفه خدمات ثبت آگهی در ربات و کانال WeDoo
===============================
🔰️ درخواست کننده (آگهی ساده) : 10,000 تومان
🔰️️ انجام دهنده : 15,000 تومان
🔰️️ استخدامی : 15,000 تومان
🔰️️ کارجو : 15,000 تومان
🔰️ دعوت به همکاری : 20,000 تومان
🔰️ فروش محصول،کانال یا کتاب : 20,000 تومان
🔰️ تبلیغات : 40,000 تومان
===============================

✅ در صورت عکس دار بودن آگهی مبلغ 5,000 به هزینه ثبت آگهی اضافه میشود"""

# Admins that can use the admin only commands
Admin_IDs = [366029355, 5342445670,6621731680,6345430841]

# keyboard options for different menus
updater = Updater("6094494835:AAF4A3bTaQpIodvlo7NdoR_ryBO908kEh_E", use_context=True)
kbd_layout = [
    ["مشاهده آگهی ها", "ثبت آگهی"],
    ["آگهی های من", "قیمت آگهی ها"],
    ["پشتیبانی 🗯"],
]
kbd_layout_cat = [
    ["دروس دانشگاهی", "برنامه نویسی", "مهندسی"],
    ["طراحی سایت", "پروژه های گرافیکی", "تایپ و ترجمه"],
    ["سایر", "بازگشت ↪"],
]
keyboards = {
    "kbd_layout_برنامه": [["پایتون", "C", "JAVA", "PHP"], ["سایر💻", "بازگشت"]],
    "kbd_layout_پروژه": [
        ["طراحی 2و3 بعدی", "Photoshop", "Adobe Premiere", "عکس و فیلم"],
        ["سایر✍", "بازگشت"],
    ],
    "kbd_layout_طراحی": [
        ["وردپرس", "تولید محتوا", "سئو"],
        ["جوملا", "html"],
        ["سایر🕶", "بازگشت"],
    ],
    "kbd_layout_دروس": [
        ["دروس پایه", "دروس تخصصی", "دروس عمومی", "آزمایشگاهی"],
        ["سایر🥼", "بازگشت"],
    ],
    "kbd_layout_تایپ": [
        ["تایپ", "ترجمه", "خلاصه نویسی", "پاورپوینت"],
        ["سایر👨‍🎓", "بازگشت"],
    ],
    "kbd_layout_مهندسی": [
        ["متلب", "اتوکد", "سالیدورکس", "کامسول"],
        ["سایر📈", "بازگشت"],
    ],
}
kbd_layout_type = [
    ["انجام دهنده", "درخواست کننده", "تبلیغاتی"],
    ["استخدامی", "کارجو","دعوت به همکاری"],
    [  "فروش کانال یا کتاب","بازگشت ↪"],
]
cat_dict = [
    "دروس دانشگاهی",
    "برنامه نویسی",
    "طراحی سایت",
    "مهندسی",
    "پروژه های گرافیکی",
    "تایپ و ترجمه",
    "سایر",
]
allcat = ["پایتون","C","JAVA","PHP","سایر💻","Photoshop","طراحی 2و3 بعدی","Adobe Premiere","عکس و فیلم","سایر✍","وردپرس","تولید محتوا","سئو","جوملا","html","سایر🕶","دروس پایه","دروس تخصصی","دروس عمومی","آزمایشگاهی","سایر🥼","تایپ","ترجمه","خلاصه نویسی","پاورپوینت","سایر👨‍🎓","متلب","اتوکد","سالیدورکس","کامسول","سایر📈",]

profiles = {}


# start command function
def start(update: Update, context: CallbackContext):
    print("/start called")
    kbd = ReplyKeyboardMarkup(kbd_layout, resize_keyboard=True)
    update.message.reply_text(
        text="""سلام....
🔅 به ربات تلگرامی ویدوو WeDoo خوش اومدي🔅

🟪 اينجا ميتونی به راحتی آگهيتو درج كنی و در هر زمینه ای که مدنظرت هست آگهی پیدا کنی.


چند نكته مهم:

❗ثبت آگهی تا 15 شهریور ماه رایگان میباشد❗

🟪 برای آگهی گذاشتن تو كانال فقط لازمه كه روی گزينه ثبت آگهی كليک كنی و قدم به قدم با راهنمايي ربات جلو بری.

🟪 برای واگذاری پروژه به تيم ما (اگه می خواید ما براتون پروژه رو انجام بدیم) ، آگهی استخدامی، سفارش تبليغات و هر كاري به جز درج آگهی؛ میتونی از طریق آیدی زیر به تیم پشتیبانی ۲۴ ساعته‌ی ما پیام بدی.
🆔 @WeDoo_support1

🔰آدرس کانال:
@WeDoo_board""",
        reply_markup=kbd,
    )


# handler for keyboard menu options
def messagehandler(update: Update, context: CallbackContext):
    message = update.message.text
    reply = update.message.reply_text
    # show sent messages in console
    # declaring global to use the varibles outside the function
    global rules,cat2, text_con, cat_con2_search, user_con, support, type_1, type_con, cat_con, category, text_agahi, user_agahi, listing, agahis, count, count_agahi, new_count, cat_con_search, cat_con2
    # code for main menu buttons
    if message == "ثبت آگهی":
        kbd = ReplyKeyboardMarkup([["ادامه","بازگشت ↪"]], resize_keyboard=True)
        reply(text="""⛔ اطلاعیه
کانال ویدوو برای رشته‌ های مختلف تیم تخصصی داره و میتونی قبل از اینکه اگهی بفرستی کارتو براشون بفرستی تا از بابت انجام آن خیالت راحت تر باشه.
قبل ثبت اگهی یه سر به پی وی ادمین بزن ⬅
@WeDoo_support1

برای ثبت آگهی گزینه ادامه را انتخاب کنید.""",reply_markup=kbd)

    # Return button
    elif message == "ادامه":
        kbd = ReplyKeyboardMarkup(kbd_layout_type, resize_keyboard=True)
        reply(
            text="""نوع آگهی خود را از منو انتخاب کنید ⬇️

📌آگهی غیر از درخواست کنند(آگهی ساده) پس از تایید در کانال قرار میگیرند."""
,
            reply_markup=kbd,
        )
        type_con = True
    elif message == "بازگشت ↪":
        support = False
        text_con = False
        user_con = False
        rules = False
        cat_con2_search = False
        type_con = False
        cat_con = False
        cat_con2 = False
        cat_con_search = False
        cat_con2_search = False
        listing = False
        count = 0
        agahis = []
        count_agahi = 0
        kbd = ReplyKeyboardMarkup(kbd_layout, resize_keyboard=True)
        reply(text="بازگشت به منو", reply_markup=kbd)
    elif message == "بازگشت":
        cat_con = True
        cat_con2 = False
        cat_con2_search == False
        text_con = False
        kbd = ReplyKeyboardMarkup(kbd_layout_cat, resize_keyboard=True)
        reply(text="بازگشت به دسته بندی ها", reply_markup=kbd)
    elif message == "مشاهده آگهی ها":
        kbd = ReplyKeyboardMarkup(kbd_layout_cat, resize_keyboard=True)
        reply("دسته بندی مورد نظر برای مشاهده پروژه را انتخاب کنید:", reply_markup=kbd)
        cat_con_search = True
    # Next button when looking at the projects
    elif message == "بعدی" and listing == True:
        new_count = 0
        if count_agahi == 0:
            kbd = ReplyKeyboardMarkup([["بازگشت ↪"]], resize_keyboard=True)
            reply("آگهی ها تمام شد ")
        else:
            for i in agahis[count:]:
                reply(
                    f"""🔻کد آگهی: {i[0]}

🔘نوع آگهی: {i[1]}
🔘دسته بندی: {i[2]}

💬 {i[3]}
〰〰〰〰〰〰
🆔 {i[4]}
〰〰〰〰〰〰
📌 قیمت توافقی
🔴 @WeDoo_board"""
                )
                count += 1
                new_count += 1
                count_agahi -= 1
                if count_agahi == 0:
                    kbd = ReplyKeyboardMarkup([["بازگشت ↪"]], resize_keyboard=True)
                    reply("اتمام آگهی ها")
                    break
                if new_count == 5:
                    kbd = kbd = ReplyKeyboardMarkup(
                        [["بعدی"], ["بازگشت ↪"]], resize_keyboard=True
                    )
                    reply(
                        text="برای دیدن ادامه آگهی ها بعدی را انتخاب کنید",
                        reply_markup=kbd,
                    )
                    break
    # Selecting category when adding project
    elif type_con == True:
        type_1 = message
        type_con = False
        kbd = ReplyKeyboardMarkup(kbd_layout_cat, resize_keyboard=True)
        reply(" دسته بندی پروژه خود را از منو انتخاب کنید:", reply_markup=kbd)
        cat_con = True
    # Finding projects by their category and printing them
    elif message in cat_dict:
        if cat_con_search == True:
            cat_con_search == False
            if message == "سایر":
                category = message
                cursor.execute(
                    "SELECT * FROM Agahi WHERE Type=? and Category=?",
                    (
                        "درخواست کننده",
                        category,
                    ),
                )
                agahis = cursor.fetchall()
                count_agahi = len(agahis)
                kbd = ReplyKeyboardMarkup([["بازگشت ↪"]], resize_keyboard=True)
                count = 0
                if count_agahi == 0:
                    reply("آگهی در این دسته بندی وجود ندارد")
                else:
                    reply("آگهی ها", reply_markup=kbd)
                    for i in agahis:
                        reply(
                            text=f"""🔻کد آگهی: {i[0]}

🔘نوع آگهی: {i[1]}
🔘دسته بندی: {i[2]}

💬 {i[3]}
〰〰〰〰〰〰
🆔 {i[4]}
〰〰〰〰〰〰
📌 قیمت توافقی
🔴 @WeDoo_board"""
                        )
                        count += 1
                        count_agahi -= 1
                        if count_agahi == 0:
                            kbd = ReplyKeyboardMarkup(
                                [["بازگشت ↪"]], resize_keyboard=True
                            )
                            reply("اتمام آگهی ها")
                        elif count == 5:
                            kbd = kbd = ReplyKeyboardMarkup(
                                [["بعدی"], ["بازگشت ↪"]], resize_keyboard=True
                            )
                            reply(
                                text="برای دیدن ادامه آگهی ها بعدی را انتخاب کنید",
                                reply_markup=kbd,
                            )
                            listing = True
                            break
            else:
                cat2 = message
                m = message.split()
                for i in keyboards:
                    if m[0] in i:
                        kbd_name = i
                        break
                kbd = ReplyKeyboardMarkup(keyboards[kbd_name], resize_keyboard=True)
                reply(text="زیرشاخه دسته بندی را از منو انتخاب کنید:", reply_markup=kbd)
                cat_con2_search = True

        elif cat_con == True:
            cat_con = False
            if message == "سایر":
                category = message
                kbd = ReplyKeyboardMarkup([["پذیرفتن قوانین"],["بازگشت ↪"]], resize_keyboard=True)
                reply(
                    text=textrule,reply_markup=kbd
                )
                rules=True
            else:
                cat2 = message
                m = message.split()
                for i in keyboards:
                    if m[0] in i:
                        kbd_name = i
                        break
                kbd = ReplyKeyboardMarkup(keyboards[kbd_name], resize_keyboard=True)
                reply(text="زیرشاخه دسته بندی را از منو انتخاب کنید:", reply_markup=kbd)
                cat_con2 = True
    elif message=="پذیرفتن قوانین" and rules==True:
        rules=False
        text_con=True
        kbd = ReplyKeyboardMarkup([["بازگشت ↪"]], resize_keyboard=True)
        reply(text="""✅قوانین توسط شما پذیرفته شد.
حالا متن آگهیت رو برام بفرست

مثال 1: به یک نفر مسلط به نرم افزار کامسول برای کمک در انجام پروژه یا تمرین نیازمندم.
مثال 2: نیازمند طراحی سایت با نازلترین قیمت""",reply_markup=kbd)
    elif message in allcat:
        if cat_con2 == True:
            cat_con2 = False
            category = f"{cat2} - {message}"
            kbd = ReplyKeyboardMarkup([["پذیرفتن قوانین"],["بازگشت ↪"]], resize_keyboard=True)
            reply(
                text=textrule,reply_markup=kbd
            )

            rules=True
        elif cat_con2_search == True:
            category = f"{cat2} - {message}"
            cursor.execute(
                "SELECT * FROM Agahi WHERE Type=? and Category=?",
                (
                    "درخواست کننده",
                    category,
                ),
            )
            agahis = cursor.fetchall()
            count_agahi = len(agahis)
            kbd = ReplyKeyboardMarkup([["بازگشت ↪"]], resize_keyboard=True)
            count = 0
            if count_agahi == 0:
                reply("آگهی در این دسته بندی وجود ندارد")
            else:
                reply("آگهی ها", reply_markup=kbd)
                for i in agahis:
                    reply(
                        text=f"""🔻کد آگهی: {i[0]}

🔘نوع آگهی: {i[1]}
🔘دسته بندی: {i[2]}

💬 {i[3]}
〰〰〰〰〰〰
🆔 {i[4]}
〰〰〰〰〰〰
📌 قیمت توافقی
🔴 @WeDoo_board"""
                    )
                    count += 1
                    count_agahi -= 1
                    if count_agahi == 0:
                        kbd = ReplyKeyboardMarkup([["بازگشت ↪"]], resize_keyboard=True)
                        reply("اتمام آگهی ها")
                    elif count == 5:
                        kbd = kbd = ReplyKeyboardMarkup(
                            [["بعدی"], ["بازگشت ↪"]], resize_keyboard=True
                        )
                        reply(
                            text="برای دیدن ادامه آگهی ها بعدی را انتخاب کنید",
                            reply_markup=kbd,
                        )
                        listing = True
                        break
    # Button for showing all of your own projects
    elif "آگهی های من" == message:
        cursor.execute(
            "SELECT * FROM Agahi WHERE user_id=?", (update.effective_user.id,)
        )
        agahis = cursor.fetchall()
        count_agahi = len(agahis)
        reply("آگهی های شما:")
        if len(agahis) == 0:
            reply("شما آگهی ندارید ❌")
        else:
            for i in agahis:
                reply(
                    f"""🔻کد آگهی: {i[0]}

🔘نوع آگهی: {i[1]}
🔘دسته بندی: {i[2]}

💬 {i[3]}
〰〰〰〰〰〰
🆔 {i[4]}
〰〰〰〰〰〰
📌 قیمت توافقی
🔴 @WeDoo_board"""
                )
                count_agahi -= 1
                if count_agahi == 0:
                    kbd = ReplyKeyboardMarkup([["بازگشت ↪"]], resize_keyboard=True)
                    reply("اتمام آگهی ها")
    # Button for showing prices of different listings
    elif message == "قیمت آگهی ها":
        reply(text=text_price)
    elif message == "پشتیبانی 🗯":
        support = True
        kbd = ReplyKeyboardMarkup([["بازگشت ↪"]], resize_keyboard=True)
        reply(text="پیام خود را برای پشتیبانی وارد کنید یا به ایدی @WeDoo_support1 پیام بدهید:", reply_markup=kbd)
    # Button for contacting support
    elif support == True:
        user = update.effective_user
        context.bot.send_message(
            chat_id="-962336869", text=f"کاربر @{user.username} یک پیام فرستاد:"
        )
        context.bot.forward_message(
            chat_id="-962336869",
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id,
        )
        support = False
        kbd = ReplyKeyboardMarkup(kbd_layout, resize_keyboard=True)
        context.bot.send_message(
            chat_id=user.id, text="پیام شما برای پشتیبانی ارسال شد ✅", reply_markup=kbd
        )
    # The projects text when adding a new listing
    elif text_con == True:
        for i in swear["word"]:
            if (
                bool(
                    (
                        re.search(
                            rf"(^|[a-zA-Z0-9]){i}($|[a-zA-Z0-9])",
                            message,
                            re.IGNORECASE,
                        )
                    )
                )
                == True
            ):
                reply(
                    " از کلمات مستهجن در آگهی خود استفاده نکنید ،دوباره متن آگهی خود را وارد کنید:"
                )
                text_con == True
                conx1 = False
                break
            else:
                conx1 = True
        if conx1 == True:
            if type_1 == "درخواست کننده":
                if  len(message.split("\n")) > 3:
                        reply("متن آگهی از 3 خط بیشتر نباشد، دوباره متن آگهی را وارد کنید:")
                        text_con == True
                else:
                    text_agahi = message
                    user = update.effective_user
                    text_con = False
                    user_con = True
                    kbd = ReplyKeyboardMarkup([["بازگشت ↪"]], resize_keyboard=True)
                    context.bot.send_message(
                        chat_id=user.id,
                        text="""حالا آیدی یا شماره تماستو وارد کن.
مثال: @WeDoo_board""",
                        reply_markup=kbd,
                    )
            else:
                text_agahi = message
                user = update.effective_user
                text_con = False
                user_con = True
                kbd = ReplyKeyboardMarkup([["بازگشت ↪"]], resize_keyboard=True)
                context.bot.send_message(
                chat_id=user.id,
                text="""حالا آیدی یا شماره تماستو وارد کن.
مثال: @WeDoo_board""",
                reply_markup=kbd,
                    )
    # Username or number to be displayed under the listing
    elif user_con == True:
        user = update.effective_user
        user_agahi = message
        user_con = False
        kbd = ReplyKeyboardMarkup(kbd_layout, resize_keyboard=True)
        cursor.execute(
            "INSERT INTO Agahi (Type, Category, Text, Contact, user_id ) VALUES (?, ?, ?, ?, ?)",
            (type_1, category, text_agahi, user_agahi, user.id),
        )
        conn.commit()
        cursor.execute(
            "SELECT * FROM Agahi WHERE Id=last_insert_rowid()",
        )
        agahis = cursor.fetchone()
        reply(f"""آگهی شما ثبت شد ✅
🔻کد آگهی: {agahis[0]}

🔘نوع آگهی: {agahis[1]}
🔘دسته بندی: {agahis[2]}

💬 {agahis[3]}

🆔 {agahis[4]}
📌 قیمت توافقی
===============================
❗ثبت آگهی تا 15 شهریور ماه رایگان میباشد❗
✅ آگهی  پس از پرداخت شما و تایید ادمین به صورت آنی در کانال منتشر می شود.
⚠️ برای کند نبودن روند پرداخت بانکی لطفا VPN  خود را خاموش کنید.
""")
        matn =f"""🔻کد آگهی: {agahis[0]}

🔘نوع آگهی: {agahis[1]}
🔘دسته بندی: {agahis[2]}

💬 {agahis[3]}
〰〰〰〰〰〰
🆔 {agahis[4]}
〰〰〰〰〰〰
📌 قیمت توافقی
🔴 @WeDoo_board"""
        if agahis[1] == "درخواست کننده":
            context.bot.send_message(text=matn, chat_id=-1001825834732)
        else:
            context.bot.send_message(text=matn, chat_id=-962336869)

def delete(update: Update, context):
    if update.effective_user.id in Admin_IDs:
        try:
            idagahi = update.message.text.split()[1]
        except Exception as e:
            print(e)
            update.message.reply_text(f"کد آگهی را با فاصله بعد از دیلیت وارد کنید")
        else:
            cursor.execute(
                "DELETE FROM Agahi WHERE Id=?",
                (idagahi,),
            )
            conn.commit()
            update.message.reply_text(f"آگهی {idagahi} پاک شد")
    else:
        update.message.reply_text("Admin only command")


# Command and message handlers
Handler = updater.dispatcher.add_handler
Handler(CommandHandler("start", start))
Handler(CommandHandler("delete", delete))
Handler(MessageHandler(Filters.chat_type.private, messagehandler))

# Starting the bot
try:
    updater.start_polling()
    print("Bot started successfully...")
    updater.idle()
except Exception as e:
    print(e)


### UNUSED CODE ###
# help command
# def help(update: Update, context):
#     update.message.reply_text(
#         """دستورات بات:
# /youtube - لینک یوتیوب
# /linkedin - اکانت لینکدین
# /gmail - آدرس جیمیل
# /url -  وب سایت"آدرس""
#     )
# Profile command
# def profile(update: Update, context: CallbackContext):
#   print("profile called")
#   user = update.effective_user
#   chat_id = update.message.chat_id
#   if chat_id in profiles:
#       context.bot.send_message(
#           chat_id=user.id, text="Your profile is already set up."
#       )
#   else:
#       profiles[chat_id] = {}
#       context.bot.send_message(chat_id=user.id, text="Please enter your full name:")
#       return "NAME"
#
# def gmail_url(update: Update, context):
#    update.message.reply_text("Gmail ==> Wedoo@Gmail.com")

# def youtube_url(update: Update, context):
#     update.message.reply_text("Youtube Link ==> https://www.youtube.com/Wedoo")

# def linkedIn_url(update: Update, context):
#     update.message.reply_text("LinkedIn URL ==> https://www.linkedin.com/in/Wedoo/")

# def WEB_SITE(update: Update, context):
#     update.message.reply_text("Website URL ==> https://www.Wedoo.com")
# Handler(CommandHandler("youtube", youtube_url))
# Handler(CommandHandler("linkedin", linkedIn_url))
# Handler(CommandHandler("gmail", gmail_url))
# Handler(CommandHandler("url", WEB_SITE))
# Handler(CommandHandler("profile", profile))
# Handler(CommandHandler("help", help))