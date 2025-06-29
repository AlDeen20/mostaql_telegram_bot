import os
import time
import requests
from bs4 import BeautifulSoup
import telegram
import logging
from dotenv import load_dotenv
import asyncio

# Set up logging FIRST
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv() 

# --- CONFIGURATION ---
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
MOSTAQL_URL = 'https://mostaql.com/projects?sort=latest'
SENT_LINKS_FILE = 'sent_projects.txt'
CHECK_INTERVAL = 60

# --- UTILITY FUNCTIONS ---
def escape_markdown(text):
    """Helper function to escape telegram markdown symbols."""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return "".join(['\\' + char if char in escape_chars else char for char in str(text)])

def load_sent_links():
    """Loads the set of already sent project links from a file."""
    if not os.path.exists(SENT_LINKS_FILE): return set()
    with open(SENT_LINKS_FILE, 'r') as f: return set(line.strip() for line in f)

def save_sent_link(link):
    """Appends a new sent project link to our file."""
    with open(SENT_LINKS_FILE, 'a') as f: f.write(link + '\n')


# =========================================================================
# ===                  FIXED SCRAPING FUNCTION                          ===
# =========================================================================
def scrape_mostaql():
    """
    Scrapes the Mostaql projects page, updated for the new HTML structure.
    """
    logger.info("Scraping Mostaql for projects...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(MOSTAQL_URL, headers=headers)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')

        # UPDATED: Look for table rows with class 'project-row' instead of 'card-project'
        project_rows = soup.find_all('tr', class_='project-row')
        
        projects = []
        for row in project_rows:
            # UPDATED: Find title and link from the h2 > a structure
            title_element = row.find('h2').find('a') if row.find('h2') else None
            
            # UPDATED: Find description from the p > a structure
            description_element = row.find('p', class_='project__brief').find('a', class_='details-url') if row.find('p', class_='project__brief') else None

            # Find the number of offers from the list item containing the ticket icon
            offers_text = "0" # Default to 0 if not found
            offers_element = row.find('i', class_='fa-ticket')
            if offers_element and offers_element.parent:
                offers_text = offers_element.parent.get_text(strip=True)

            if title_element and description_element:
                projects.append({
                    'title': title_element.get_text(strip=True),
                    'link': title_element['href'], # The link is now a full URL
                    'description': description_element.get_text(strip=True),
                    'offers': offers_text # Note: Budget is no longer available on this page
                })

        logger.info(f"Found {len(projects)} projects on the page.")
        return projects
    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}", exc_info=True)
        return None

# --- ASYNC FUNCTIONS ---
async def send_startup_notification(bot):
    logger.info("Performing startup sequence...")
    projects = scrape_mostaql()
    if projects:
        latest_project = projects[0]
        logger.info(f"Sending latest project on startup: {latest_project['title']}")
        # UPDATED: Removed 'Budget' from the message as it's no longer available
        message = (f"*🔥 أحدث مشروع حالي*\n\n"
                   f"*{escape_markdown(latest_project['title'])}*\n\n"
                   f"📝 *الوصف:*\n{escape_markdown(latest_project['description'])}\n\n"
                   f"📊 *العروض:* {escape_markdown(latest_project['offers'])}\n\n"
                   f"[🔗 عرض المشروع]({latest_project['link']})")
        try:
            await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='MarkdownV2', disable_web_page_preview=True)
            save_sent_link(latest_project['link'])
        except Exception as e: logger.error(f"Failed to send startup project message: {e}")
    
    try:
        confirmation_message = "🤖 *تم تشغيل البوت بنجاح*\n\nأنا الآن أراقب موقع مستقل وسأقوم بإعلامك فور نزول أي مشاريع جديدة\\."
        await bot.send_message(chat_id=CHAT_ID, text=confirmation_message, parse_mode='MarkdownV2')
        logger.info("Startup confirmation message sent.")
    except Exception as e: logger.error(f"Failed to send startup confirmation message: {e}")

async def check_for_new_projects(bot):
    logger.info("Checking for new projects...")
    projects = scrape_mostaql()
    if projects is None: return
    sent_links = load_sent_links()
    for project in reversed(projects):
        if project['link'] not in sent_links:
            logger.info(f"New project found: {project['title']}")
            # UPDATED: Removed 'Budget' from the message
            message = (f"*📣 مشروع جديد على مستقل*\n\n"
                       f"*{escape_markdown(project['title'])}*\n\n"
                       f"📝 *الوصف:*\n{escape_markdown(project['description'])}\n\n"
                       f"📊 *العروض:* {escape_markdown(project['offers'])}\n\n"
                       f"[🔗 عرض المشروع]({project['link']})")
            try:
                # FIXED: Corrected typo from send__message to send_message
                await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='MarkdownV2', disable_web_page_preview=True)
                save_sent_link(project['link'])
                await asyncio.sleep(1) 
            except Exception as e: logger.error(f"Failed to send message for '{project['title']}': {e}")

# --- MAIN ASYNC EXECUTION ---
async def main():
    if not BOT_TOKEN or not CHAT_ID:
        logger.error("FATAL ERROR: Could not find credentials in .env file. Please check it.")
        exit()
    bot = telegram.Bot(token=BOT_TOKEN)
    await send_startup_notification(bot)
    logger.info("Startup complete. Entering main monitoring loop...")
    while True:
        logger.info(f"Waiting for {CHECK_INTERVAL} seconds before the next check.")
        await asyncio.sleep(CHECK_INTERVAL)
        await check_for_new_projects(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")