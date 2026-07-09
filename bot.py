import os
import json
import logging
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# File to store user data
DATA_FILE = "user_data.json"

# Motivational quotes
QUOTES = [
    "✨ The only way to do great work is to love what you do. - Steve Jobs",
    "💪 Believe you can and you're halfway there. - Theodore Roosevelt",
    "🌟 It does not matter how slowly you go as long as you do not stop. - Confucius",
    "🔥 Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "🌈 Happiness is not something ready made. It comes from your own actions. - Dalai Lama",
    "🚀 The secret of getting ahead is getting started. - Mark Twain",
    "💎 Your time is limited, don't waste it living someone else's life. - Steve Jobs",
    "🌟 Be the change you wish to see in the world. - Gandhi",
    "⚡ If you can dream it, you can achieve it. - Zig Ziglar",
    "🌻 Act as if what you do makes a difference. It does. - William James",
    "🌺 The best time to plant a tree was 20 years ago. The second best time is now.",
    "💫 You are braver than you believe, stronger than you seem, and smarter than you think.",
    "🌟 Success is not the key to happiness. Happiness is the key to success.",
    "💪 The only impossible journey is the one you never begin."
]

# Daily affirmations
AFFIRMATIONS = [
    "I am worthy of all good things.",
    "I am strong, capable, and resilient.",
    "Every day I am growing and improving.",
    "I deserve happiness and peace.",
    "I am grateful for all that I have.",
    "My potential is unlimited.",
    "I am in charge of my own happiness.",
    "Positive energy flows through me.",
    "I am exactly where I need to be.",
    "I radiate love, joy, and peace.",
    "I trust the journey of my life.",
    "I am enough, just as I am.",
    "I attract positive opportunities into my life.",
    "Every challenge makes me stronger."
]

# Meditation tips
MEDITATION_TIPS = [
    "🧘 Find a quiet place and sit comfortably.",
    "🧘 Close your eyes and take 5 deep breaths.",
    "🧘 Focus on your breathing - in and out.",
    "🧘 Let go of all thoughts and just be present.",
    "🧘 Do this for 5 minutes every morning.",
    "🧘 Stretch your body gently before meditation.",
    "🧘 Use a mantra like 'Peace' or 'Calm'.",
    "🧘 Practice gratitude before you start.",
    "🧘 Focus on the sensation of your breath.",
    "🧘 When your mind wanders, gently bring it back.",
    "🧘 Visualize a peaceful place in your mind.",
    "🧘 End your meditation with a smile."
]

# Wellness tips
WELLNESS_TIPS = [
    "🌅 Start your day with 5 minutes of deep breathing.",
    "🥗 Drink a glass of water first thing in the morning.",
    "🚶 Take a 10-minute walk in nature daily.",
    "📵 Take a break from screens every hour.",
    "😴 Get 7-8 hours of quality sleep each night.",
    "✍️ Write 3 things you're grateful for each day.",
    "🧘 Practice mindfulness for 5 minutes daily.",
    "🤝 Connect with a friend or loved one.",
    "🎵 Listen to calming music or nature sounds.",
    "📚 Read something inspiring every day.",
    "🌿 Spend time outdoors in green spaces.",
    "🍵 Drink herbal tea to relax your mind.",
    "💪 Exercise for 20 minutes daily.",
    "🌙 Create a relaxing bedtime routine."
]

# Load user data
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save user data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Initialize data
user_data = load_data()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "Friend"
    first_name = update.effective_user.first_name or "Friend"
    
    # Initialize user data
    if user_id not in user_data:
        user_data[user_id] = {
            "username": username,
            "first_name": first_name,
            "joined": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "affirmation_count": 0,
            "meditation_count": 0,
            "mood_logs": []
        }
        save_data(user_data)
    
    welcome_text = (
        f"🌸 *Welcome to Top Bliss Bot, {first_name}!* 🌸\n\n"
        "Your personal companion for wellness, motivation, and happiness.\n\n"
        "📌 *Commands:*\n"
        "/quote - Get a motivational quote\n"
        "/affirm - Receive a daily affirmation\n"
        "/meditate - Get a meditation tip\n"
        "/mood - Log your current mood\n"
        "/stats - View your wellness stats\n"
        "/tips - Get wellness tips\n"
        "/about - Learn about this bot\n"
        "/help - Show this message\n\n"
        "✨ *Stay positive and blissful!* ✨"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📋 *Top Bliss Bot Commands*\n\n"
        "/start - Start the bot\n"
        "/quote - Get a motivational quote\n"
        "/affirm - Receive a daily affirmation\n"
        "/meditate - Get a meditation tip\n"
        "/mood - Log your current mood\n"
        "/stats - View your wellness stats\n"
        "/tips - Get wellness tips\n"
        "/about - Learn about this bot\n"
        "/help - Show this help message\n\n"
        "💡 *Quick tip:* Use /mood regularly to track your emotional well-being!\n\n"
        "🌟 *Your wellness journey starts here!*"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# About command
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "🌟 *About Top Bliss Bot*\n\n"
        "Top Bliss Bot is your daily companion for:\n"
        "✨ Motivation & Inspiration\n"
        "🧘 Mindfulness & Meditation\n"
        "💫 Daily Affirmations\n"
        "🎭 Mood Tracking\n"
        "🌿 Wellness Tips\n\n"
        "Created with ❤️ to help you live your best life.\n\n"
        "📊 Track your progress with /stats\n"
        "🎯 Set your intention with /affirm\n\n"
        "Version 1.0\n"
        "Made with love for Telegram 🌸"
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")

# Quote command
async def get_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote = random.choice(QUOTES)
    await update.message.reply_text(
        f"📖 *Quote of the Moment*\n\n{quote}\n\n✨ *Stay inspired!*",
        parse_mode="Markdown"
    )

# Affirmation command
async def get_affirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    affirmation = random.choice(AFFIRMATIONS)
    
    # Track affirmation count
    if user_id in user_data:
        user_data[user_id]["affirmation_count"] += 1
        save_data(user_data)
    
    await update.message.reply_text(
        f"💫 *Daily Affirmation*\n\n_{affirmation}_\n\n"
        f"✨ Repeat this to yourself today!\n"
        f"📊 You've received {user_data[user_id]['affirmation_count']} affirmations so far!",
        parse_mode="Markdown"
    )

# Meditation tip command
async def get_meditation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    tip = random.choice(MEDITATION_TIPS)
    
    # Track meditation count
    if user_id in user_data:
        user_data[user_id]["meditation_count"] += 1
        save_data(user_data)
    
    meditation_text = (
        f"🧘 *Meditation Guide*\n\n{tip}\n\n"
        "🌿 Take a moment to breathe deeply and relax.\n"
        "You deserve this moment of peace.\n\n"
        f"🧘 You've meditated {user_data[user_id]['meditation_count']} times with me!"
    )
    await update.message.reply_text(meditation_text, parse_mode="Markdown")

# Mood logging with inline buttons
async def log_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("😊 Happy", callback_data="mood_happy"),
            InlineKeyboardButton("😌 Calm", callback_data="mood_calm"),
        ],
        [
            InlineKeyboardButton("😤 Stressed", callback_data="mood_stressed"),
            InlineKeyboardButton("😔 Sad", callback_data="mood_sad"),
        ],
        [
            InlineKeyboardButton("😴 Tired", callback_data="mood_tired"),
            InlineKeyboardButton("🤗 Grateful", callback_data="mood_grateful"),
        ],
        [
            InlineKeyboardButton("🤩 Excited", callback_data="mood_excited"),
            InlineKeyboardButton("😕 Confused", callback_data="mood_confused"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎭 *How are you feeling right now?*\n\nSelect your mood:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Handle mood button callback
async def mood_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    mood = query.data.replace("mood_", "")
    
    # Save mood log
    if user_id in user_data:
        user_data[user_id]["mood_logs"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mood": mood
        })
        save_data(user_data)
    
    mood_emojis = {
        "happy": "😊",
        "calm": "😌",
        "stressed": "😤",
        "sad": "😔",
        "tired": "😴",
        "grateful": "🤗",
        "excited": "🤩",
        "confused": "😕"
    }
    
    emoji = mood_emojis.get(mood, "🌟")
    
    await query.edit_message_text(
        f"✅ *Mood logged!*\n\n{emoji} You're feeling *{mood.capitalize()}*\n\n"
        "Thank you for checking in with yourself. 💙\n"
        "Remember, all feelings are valid and temporary.\n\n"
        f"📊 You've logged {len(user_data[user_id]['mood_logs'])} moods total!\n\n"
        "✨ You're doing great!",
        parse_mode="Markdown"
    )

# Stats command
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    if user_id not in user_data:
        await update.message.reply_text(
            "📊 No data found yet. Start using the bot with /start!"
        )
        return
    
    data = user_data[user_id]
    total_moods = len(data["mood_logs"])
    
    # Calculate mood breakdown
    mood_counts = {}
    for log in data["mood_logs"]:
        mood = log["mood"]
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    
    stats_text = (
        f"📊 *Your Wellness Stats*\n\n"
        f"👤 User: {data['first_name']} (@{data['username']})\n"
        f"📅 Joined: {data['joined']}\n"
        f"💫 Affirmations: {data['affirmation_count']}\n"
        f"🧘 Meditations: {data['meditation_count']}\n"
        f"🎭 Moods logged: {total_moods}\n"
    )
    
    # Show mood breakdown if any
    if mood_counts:
        stats_text += "\n📈 *Mood Breakdown:*\n"
        for mood, count in mood_counts.items():
            emoji = {
                "happy": "😊", "calm": "😌", "stressed": "😤",
                "sad": "😔", "tired": "😴", "grateful": "🤗",
                "excited": "🤩", "confused": "😕"
            }.get(mood, "🌟")
            stats_text += f"{emoji} {mood.capitalize()}: {count} times\n"
    
    # Show last mood if exists
    if total_moods > 0:
        last_mood = data["mood_logs"][-1]
        emoji = {
            "happy": "😊", "calm": "😌", "stressed": "😤",
            "sad": "😔", "tired": "😴", "grateful": "🤗",
            "excited": "🤩", "confused": "😕"
        }.get(last_mood['mood'], "🌟")
        stats_text += f"\n🕐 *Last mood:* {emoji} {last_mood['mood'].capitalize()} ({last_mood['date']})"
    
    stats_text += "\n\n💪 *Keep going! Every small step matters.*\n"
    stats_text += "🌟 *You're doing amazing!*"
    
    await update.message.reply_text(stats_text, parse_mode="Markdown")

# Tips command
async def get_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tip = random.choice(WELLNESS_TIPS)
    await update.message.reply_text(
        f"🌟 *Wellness Tip*\n\n{tip}\n\n"
        "🌿 Small habits create big changes!\n"
        "You've got this! 💪",
        parse_mode="Markdown"
    )

# Handle plain text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    first_name = update.effective_user.first_name or "Friend"
    
    if any(word in text for word in ["hello", "hi", "hey", "howdy"]):
        await update.message.reply_text(
            f"👋 Hey {first_name}! Type /start to begin your wellness journey.\n"
            "I'm here to help you stay positive! 🌸"
        )
    elif "thank" in text or "thanks" in text:
        await update.message.reply_text(
            "🤗 You're welcome, {first_name}! Stay blissful and keep shining!\n"
            "Remember, gratitude attracts more blessings! ✨"
        )
    elif "love" in text:
        await update.message.reply_text(
            f"❤️ Sending love and positive vibes your way, {first_name}!\n"
            "You are amazing and worthy of all good things! ✨"
        )
    elif any(word in text for word in ["sad", "depressed", "down", "unhappy", "lonely"]):
        await update.message.reply_text(
            f"🌻 I'm sorry you're feeling down, {first_name}.\n"
            "Remember, it's okay to feel this way.\n"
            "Try /affirm for encouragement or /meditate to relax.\n"
            "You are not alone. 💙\n\n"
            "This too shall pass. Better days are coming! 🌈"
        )
    elif any(word in text for word in ["happy", "great", "good", "awesome", "wonderful"]):
        await update.message.reply_text(
            f"😊 That's wonderful to hear, {first_name}!\n"
            "Keep spreading that positive energy! ✨\n"
            "You're making the world a better place. 🌍"
        )
    elif "how are you" in text or "how are you doing" in text:
        await update.message.reply_text(
            "🤖 I'm doing great, thanks for asking!\n"
            f"How are you feeling today, {first_name}? Try /mood to let me know!\n"
            "I'm here for you! 💙"
        )
    elif "help" in text:
        await update.message.reply_text(
            "🆘 Type /help to see all available commands!\n"
            "I'm here to support your wellness journey! 🌸"
        )
    else:
        await update.message.reply_text(
            f"🤔 I'm here to support you, {first_name}!\n"
            "Try /help to see all available commands.\n\n"
            "💫 You're doing amazing, keep going!\n"
            "🌟 Every day is a new opportunity!"
        )

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ Oops! Something went wrong. Please try again.\n"
            "If the problem persists, try /start to reset.\n\n"
            "🙏 Thank you for your patience!"
        )

# Main function
def main():
    # Get bot token from environment variable
    token = os.environ.get("TELEGRAM_TOKEN")
    
    if not token:
        logger.error("❌ No TELEGRAM_TOKEN found in environment variables!")
        logger.error("Please add TELEGRAM_TOKEN in Railway Variables.")
        return
    
    # Create application
    app = ApplicationBuilder().token(token).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("quote", get_quote))
    app.add_handler(CommandHandler("affirm", get_affirmation))
    app.add_handler(CommandHandler("meditate", get_meditation))
    app.add_handler(CommandHandler("mood", log_mood))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(CommandHandler("tips", get_tips))
    
    # Callback query handler for mood buttons
    app.add_handler(CallbackQueryHandler(mood_callback, pattern="^mood_"))
    
    # Message handler for non-command messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handler
    app.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("🚀 Starting Top Bliss Bot with long polling...")
    logger.info("🤖 Bot @Topbliss1_bot is now active!")
    logger.info("💚 Ready to spread positivity and wellness!")
    app.run_polling()

if __name__ == "__main__":
    main()
