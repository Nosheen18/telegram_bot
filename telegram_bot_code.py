from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
import openai
import os
from dotenv import load_dotenv, find_dotenv
import requests
from bs4 import BeautifulSoup

dotenv_path = find_dotenv()
dotenv_loaded = load_dotenv(dotenv_path=dotenv_path)
print("Dotenv Loaded:", dotenv_loaded)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("BOT_TOKEN:", BOT_TOKEN)
print("OPENAI_API_KEY:", OPENAI_API_KEY)

if not BOT_TOKEN:
    print("Error: BOT_TOKEN is not set!")
    exit()

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY is not set!")
    exit()

openai.api_key = OPENAI_API_KEY

def fetch_ppc_trends():
    url = "https://databox.com/ppc-industry-benchmarks"
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_question}
    ]
)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    cpc_data = soup.find('some_cpc_tag') 
    return cpc_data.text if cpc_data else "Data not available"

def fetch_industry_trends(update: Update, context):
    cpc_data = fetch_ppc_trends()
    update.message.reply_text(f"Based on current benchmarks, the CPC for your industry is: {cpc_data}")

async def start(update: Update, context):
    await update.message.reply_text("Welcome! I can help you with business data analysis and digital marketing. Type /analyze to begin.")


async def analyze(update: Update, context):
    await update.message.reply_text("What industry is your business in?")
    return 1  # Move to the next step


async def industry_input(update: Update, context):
    user_input = update.message.text
    context.user_data['industry'] = user_input
    await update.message.reply_text("What is your business objective?")
    return 2


async def objective_input(update: Update, context):
    user_input = update.message.text
    context.user_data['objective'] = user_input
    await update.message.reply_text("Do you have a website? If yes, please share the URL.")
    return 3


async def website_input(update: Update, context):
    user_input = update.message.text
    context.user_data['website'] = user_input
    await update.message.reply_text("Do you have any social media platforms? If yes, please share the URL.")
    return 4


async def social_media_input(update: Update, context):
    user_input = update.message.text
    context.user_data['social_media'] = user_input
    await update.message.reply_text("Do you use PPC campaigns? If yes, please share relevant details.")
    return 5


async def ppc_campaign_input(update: Update, context):
    user_input = update.message.text
    context.user_data['ppc_campaign'] = user_input
    await update.message.reply_text("Who are you trying to reach? (e.g., young adults, professionals, etc.)")
    return 6


async def target_audience_input(update: Update, context):
    user_input = update.message.text
    context.user_data['target_audience'] = user_input
    await update.message.reply_text("What location would you like to target?")
    return 7


async def location_input(update: Update, context):
    user_input = update.message.text
    context.user_data['location'] = user_input
    await update.message.reply_text("Thank you for providing the details. Analyzing your data...")
    
    industry = context.user_data.get('industry', 'unknown')
    objective = context.user_data.get('objective', 'unknown')
    location =context.user_data.get('location','unknown')
    await update.message.reply_text(f"Analysis complete for {industry} with objective: {objective}.")
    return ConversationHandler.END  


async def ai_faq(update: Update, context):
    user_question = " ".join(context.args)
    if not user_question:
        await update.message.reply_text("Please provide a question after /ask.")
        return    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Answer the following digital marketing question: {user_question}",
            max_tokens=200
        )
        answer = response['choices'][0]['text'].strip()
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Error with OpenAI API: {str(e)}")

def main():

    application = Application.builder().token(BOT_TOKEN).build()

    analyze_conv = ConversationHandler(
        entry_points=[CommandHandler('analyze', analyze)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, industry_input)],  
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, objective_input)], 
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, website_input)],  
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, social_media_input)],  
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, ppc_campaign_input)],  
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, target_audience_input)],  
            7: [MessageHandler(filters.TEXT & ~filters.COMMAND, location_input)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    application.add_handler(CommandHandler('start', start))
    application.add_handler(analyze_conv)
    application.add_handler(CommandHandler('ask', ai_faq))  
    application.add_handler(CommandHandler('ask', ai_faq))  

    application.run_polling()


if __name__ == '__main__':
    main()
