from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

TOKEN = "توکن_ربات_تو_اینجا"
bot = Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

# منوی اصلی دوره‌ها
def start(update, context):
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="سلام! به باشگاه رباتیک خوش آمدید 🤖")
    
    keyboard = [
        [InlineKeyboardButton("کلاس آموزش رباتیک", callback_data="robotics")],
        [InlineKeyboardButton("کلاس هوش مصنوعی", callback_data="ai")],
        [InlineKeyboardButton("کلاس زبان تخصصی رباتیک", callback_data="language")],
        [InlineKeyboardButton("دوره‌های آموزشی سلول خورشیدی", callback_data="solar")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id, text="لطفاً یکی از دوره‌های زیر را انتخاب کنید:", reply_markup=reply_markup)

# پس از انتخاب دوره، منوی رده سنی را نشان می‌دهد
def handle_course_selection(update, context):
    query = update.callback_query
    query.answer()
    
    course = query.data
    course_names = {
        "robotics": "کلاس آموزش رباتیک",
        "ai": "کلاس هوش مصنوعی",
        "language": "کلاس زبان تخصصی رباتیک",
        "solar": "دوره‌های آموزشی سلول خورشیدی"
    }

    keyboard = [
        [InlineKeyboardButton("۸ تا ۱۰ سال", callback_data=f"{course}_age_8_10")],
        [InlineKeyboardButton("۱۱ تا ۱۴ سال", callback_data=f"{course}_age_11_14")],
        [InlineKeyboardButton("۱۵ تا ۲۰ سال", callback_data=f"{course}_age_15_20")],
        [InlineKeyboardButton("۲۱ تا ۳۵ سال", callback_data=f"{course}_age_21_35")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"شما دوره {course_names[course]} را انتخاب کردید.\nلطفاً رده سنی خود را انتخاب کنید:",
        reply_markup=reply_markup
    )

# نهایی‌سازی انتخاب
def handle_age_selection(update, context):
    query = update.callback_query
    query.answer()

    data = query.data
    course_key, _, age_group = data.partition("_age_")
    course_names = {
        "robotics": "کلاس آموزش رباتیک",
        "ai": "کلاس هوش مصنوعی",
        "language": "کلاس زبان تخصصی رباتیک",
        "solar": "دوره‌های آموزشی سلول خورشیدی"
    }

    age_display = {
        "8_10": "۸ تا ۱۰ سال",
        "11_14": "۱۱ تا ۱۴ سال",
        "15_20": "۱۵ تا ۲۰ سال",
        "21_35": "۲۱ تا ۳۵ سال"
    }

    course_title = course_names.get(course_key, "دوره نامشخص")
    age_title = age_display.get(age_group, "رده سنی نامشخص")

    query.edit_message_text(
        text=f"✅ ثبت شد!\nشما در {course_title} برای رده سنی {age_title} ثبت‌نام کردید. 👌"
    )

# ثبت هندلرها
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(handle_course_selection, pattern="^(robotics|ai|language|solar)$"))
dispatcher.add_handler(CallbackQueryHandler(handle_age_selection, pattern="^(robotics|ai|language|solar)_age_.*$"))

@app.route('/')
def home():
    return "ربات فعال است."

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"
