import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================
# LOGGING SETUP
# ============================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================
# CONFIGURATION
# ============================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN environment variable is required!")
    raise ValueError("BOT_TOKEN environment variable is required!")

BOT_NAME = os.getenv("BOT_NAME", "Topbliss1_bot")
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

logger.info(f"✅ Bot configured: {BOT_NAME}")

# ============================================
# CRYPTO API FUNCTIONS
# ============================================

def get_crypto_price(coin_id="bitcoin", currency="usd"):
    """Fetch current price for a cryptocurrency from CoinGecko"""
    try:
        url = f"{COINGECKO_API_URL}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": currency
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if coin_id in data and currency in data[coin_id]:
            return data[coin_id][currency]
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching price: {e}")
        return None

def get_trending_coins():
    """Get top 7 trending cryptocurrencies"""
    try:
        url = f"{COINGECKO_API_URL}/search/trending"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        trending = []
        for item in data.get("coins", [])[:7]:
            coin = item.get("item", {})
            trending.append({
                "name": coin.get("name", "Unknown"),
                "symbol": coin.get("symbol", "").upper(),
                "market_cap_rank": coin.get("market_cap_rank", 0),
                "price_btc": coin.get("price_btc", 0)
            })
        return trending
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {e}")
        return []
    except Exception as e:
        logger.error(f"Error fetching trending: {e}")
        return []

def get_coin_list():
    """Get list of popular coin IDs"""
    popular_coins = [
        "bitcoin", "ethereum", "solana", "dogecoin", "cardano",
        "polkadot", "avalanche-2", "polygon", "chainlink", "litecoin",
        "binancecoin", "ripple", "tron", "stellar", "uniswap"
    ]
    return popular_coins

# ============================================
# TELEGRAM HANDLERS
# ============================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    keyboard = [
        [
            InlineKeyboardButton("💰 Price", callback_data="price"),
            InlineKeyboardButton("📈 Trending", callback_data="trending"),
        ],
        [
            InlineKeyboardButton("📊 Popular", callback_data="popular"),
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🚀 *Welcome to Crypto Price Bot!*\n\n"
        "I can help you track cryptocurrency prices in real-time.\n\n"
        "*📌 Commands:*\n"
        "• `/price <coin>` - Get current price\n"
        "• `/trending` - See trending coins\n"
        "• `/popular` - View popular coins\n"
        "• `/help` - Show this message\n\n"
        "*💡 Example:* `/price bitcoin`\n\n"
        "Made with ❤️ by @Topbliss1_bot"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    logger.info(f"User {update.effective_user.username} started the bot")

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /price command"""
    if not context.args:
        keyboard = [
            [InlineKeyboardButton("Bitcoin", callback_data="price_bitcoin"),
             InlineKeyboardButton("Ethereum", callback_data="price_ethereum")],
            [InlineKeyboardButton("Solana", callback_data="price_solana"),
             InlineKeyboardButton("Dogecoin", callback_data="price_dogecoin")],
            [InlineKeyboardButton("Cardano", callback_data="price_cardano"),
             InlineKeyboardButton("More...", callback_data="popular")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Please specify a coin or choose one below:\n\n"
            "Example: `/price bitcoin`",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return
    
    coin_id = context.args[0].lower()
    await update.message.reply_text(f"🔍 Fetching price for *{coin_id}*...", parse_mode="Markdown")
    
    price = get_crypto_price(coin_id)
    
    if price is None:
        await update.message.reply_text(
            f"❌ Could not find price for `{coin_id}`.\n\n"
            "Try using the full coin ID:\n"
            "• bitcoin\n"
            "• ethereum\n"
            "• solana\n"
            "• dogecoin\n"
            "• cardano\n\n"
            "Use `/popular` to see more coins.",
            parse_mode="Markdown"
        )
        return
    
    # Get price in USD and BTC
    price_btc = get_crypto_price(coin_id, "btc")
    
    response = f"💰 *{coin_id.title()} Price*\n\n"
    response += f"💵 USD: `${price:,.2f}`\n"
    if price_btc:
        response += f"₿ BTC: {price_btc:.8f}\n"
    
    response += f"\n🕐 Updated: Just now"
    
    await update.message.reply_text(response, parse_mode="Markdown")
    logger.info(f"User {update.effective_user.username} checked price for {coin_id}")

async def trending_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /trending command"""
    await update.message.reply_text("📈 Fetching trending coins...")
    
    trending = get_trending_coins()
    if not trending:
        await update.message.reply_text(
            "❌ Could not fetch trending coins. Please try again later.\n\n"
            "💡 Use `/popular` to see popular coins instead.",
            parse_mode="Markdown"
        )
        return
    
    message = "*🔥 Top Trending Coins*\n\n"
    for i, coin in enumerate(trending, 1):
        message += f"{i}. *{coin['name']}* ({coin['symbol']})\n"
        if coin['price_btc'] > 0:
            message += f"   ₿ BTC: {coin['price_btc']:.8f}\n"
        if coin['market_cap_rank'] > 0:
            message += f"   📊 Rank: #{coin['market_cap_rank']}\n"
        message += "\n"
    
    message += "💡 Use `/price <coin>` to check specific prices"
    
    await update.message.reply_text(message, parse_mode="Markdown")
    logger.info(f"User {update.effective_user.username} checked trending coins")

async def popular_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /popular command"""
    coins = get_coin_list()
    message = "*📊 Popular Cryptocurrencies*\n\n"
    
    # Create buttons for top coins
    keyboard = []
    row = []
    for i, coin in enumerate(coins[:12], 1):
        row.append(InlineKeyboardButton(
            coin.title(), 
            callback_data=f"price_{coin}"
        ))
        if i % 3 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔄 Refresh", callback_data="popular")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Choose a coin to see its price:\n\n"
        "💡 Or use `/price <coin>` directly.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    logger.info(f"User {update.effective_user.username} checked popular coins")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "*🤖 Crypto Bot Commands*\n\n"
        "📌 *Basic Commands*\n"
        "/start - Start the bot\n"
        "/price <coin> - Get current price\n"
        "/trending - See trending coins\n"
        "/popular - View popular coins\n"
        "/help - Show this message\n\n"
        "📌 *Examples*\n"
        "`/price bitcoin`\n"
        "`/price ethereum`\n"
        "`/price solana`\n\n"
        "📌 *Supported Coins*\n"
        "bitcoin, ethereum, solana, dogecoin, cardano, polkadot, "
        "avalanche, polygon, chainlink, litecoin, binancecoin, ripple, "
        "and many more!\n\n"
        "📌 *Tips*\n"
        "• Use full coin names (e.g., 'bitcoin' not 'btc')\n"
        "• Click the buttons for quick access\n"
        "• Prices update in real-time\n\n"
        "Made with ❤️ by @Topbliss1_bot"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Handle price buttons
    if data.startswith("price_"):
        coin_id = data.replace("price_", "")
        await query.edit_message_text(f"🔍 Fetching price for *{coin_id}*...", parse_mode="Markdown")
        
        price = get_crypto_price(coin_id)
        if price is None:
            await query.edit_message_text(
                f"❌ Could not find price for `{coin_id}`.\n\n"
                "Try using `/price <coin>` with a valid coin ID.",
                parse_mode="Markdown"
            )
            return
        
        response = f"💰 *{coin_id.title()} Price*\n\n"
        response += f"💵 USD: `${price:,.2f}`\n"
        
        # Add BTC price
        price_btc = get_crypto_price(coin_id, "btc")
        if price_btc:
            response += f"₿ BTC: {price_btc:.8f}\n"
        
        response += f"\n🕐 Updated: Just now"
        
        # Add back button
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="popular")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            response,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    # Handle trending button
    elif data == "trending":
        trending = get_trending_coins()
        if not trending:
            await query.edit_message_text("❌ Could not fetch trending coins.")
            return
        
        message = "*🔥 Top Trending Coins*\n\n"
        for i, coin in enumerate(trending, 1):
            message += f"{i}. *{coin['name']}* ({coin['symbol']})\n"
            if coin['price_btc'] > 0:
                message += f"   ₿ BTC: {coin['price_btc']:.8f}\n"
            message += "\n"
        
        keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data="trending")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    # Handle popular button
    elif data == "popular":
        coins = get_coin_list()
        keyboard = []
        row = []
        for i, coin in enumerate(coins[:12], 1):
            row.append(InlineKeyboardButton(
                coin.title(), 
                callback_data=f"price_{coin}"
            ))
            if i % 3 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔄 Refresh", callback_data="popular")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📊 *Choose a coin:*\n\nClick a button to see its price.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    # Handle help button
    elif data == "help":
        help_text = (
            "*Commands:*\n"
            "/start - Start\n"
            "/price <coin> - Get price\n"
            "/trending - Trending\n"
            "/popular - Popular coins\n"
            "/help - Help"
        )
        await query.edit_message_text(help_text, parse_mode="Markdown")
    
    # Handle price from menu
    elif data == "price":
        await query.edit_message_text(
            "Use `/price <coin>` or click a popular coin below.",
            parse_mode="Markdown"
        )
        # Trigger popular display
        coins = get_coin_list()
        keyboard = []
        row = []
        for i, coin in enumerate(coins[:12], 1):
            row.append(InlineKeyboardButton(
                coin.title(), 
                callback_data=f"price_{coin}"
            ))
            if i % 3 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔄 Refresh", callback_data="popular")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.message.reply_text(
            "📊 *Popular Coins:*",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# ============================================
# ERROR HANDLING
# ============================================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Run the bot"""
    logger.info("🚀 Starting Crypto Price Bot...")
    logger.info(f"Bot Name: {BOT_NAME}")
    logger.info(f"Bot Token: {BOT_TOKEN[:10]}... (hidden)")
    
    try:
        # Create application
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("price", price_command))
        app.add_handler(CommandHandler("trending", trending_command))
        app.add_handler(CommandHandler("popular", popular_command))
        app.add_handler(CommandHandler("help", help_command))
        
        # Add callback handler for buttons
        app.add_handler(CallbackQueryHandler(button_callback))
        
        # Add error handler
        app.add_error_handler(error_handler)
        
        # Start the bot
        logger.info("✅ Bot is running and ready to respond!")
        logger.info("📍 Press Ctrl+C to stop the bot")
        
        app.run_polling(allowed_updates=["message", "callback_query"])
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()
