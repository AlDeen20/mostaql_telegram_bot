# Mostaql Telegram Bot 🤖

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

A simple yet powerful Python bot that scrapes the [Mostaql](https://mostaql.com/) freelancing website for new projects and sends instant notifications to a specified Telegram chat.

This project was created to help freelancers stay ahead of the competition by getting notified of new opportunities the moment they are posted.

## ✨ Features

-   **24/7 Monitoring:** Runs continuously on a server to watch for new projects.
-   **Instant Notifications:** Sends a formatted message to your Telegram account or channel for every new project.
-   **Duplicate Prevention:** Keeps a memory of sent projects (`sent_projects.txt`) to ensure you never receive the same notification twice.
-   **Secure:** Uses a `.env` file to keep your API tokens and private information safe and out of the codebase.
-   **Easy to Deploy:** Can be deployed on free hosting services like Render or PythonAnywhere.

## 🚀 How It Works

The bot operates in a simple loop:
1.  **Scrape:** It sends a request to Mostaql's project page and parses the HTML to find all listed projects.
2.  **Compare:** It checks the unique link of each scraped project against its memory file (`sent_projects.txt`).
3.  **Notify & Remember:** If a project's link is not in its memory, it's considered new. The bot sends a notification to Telegram and then adds the project's link to its memory file to prevent future duplicates.
4.  **Wait:** It sleeps for a configured interval before starting the process again.

## 🛠️ Setup and Installation

To run this bot on your own machine, follow these steps:

1.  **Prerequisites:**
    -   Make sure you have Python 3.10+ installed.
    -   Get a Telegram Bot Token from [@BotFather](https://t.me/BotFather).
    -   Get your Telegram Chat ID from [@userinfobot](https://t.me/userinfobot).

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/AlDeen20/mostaql_telegram_bot.git
    cd mostaql_telegram_bot
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    -   Create a file named `.env` in the project root.
    -   Add your credentials to this file. **This file is ignored by Git and should never be shared.**

    ```
    # .env file
    TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
    TELEGRAM_CHAT_ID="YOUR_CHAT_ID_HERE"
    ```

5.  **Run the Bot:**
    ```bash
    python mostaql_bot.py
    ```

## 🤝 Contributing

Contributions are welcome and highly encouraged! This project can be a great tool for the freelance community, and your help can make it even better.

Whether you're fixing a bug, improving the documentation, or adding a new feature, your efforts are appreciated.

**How to Contribute:**
1.  **Fork** the repository.
2.  Create a new **branch** for your feature (`git checkout -b feature/AmazingNewFeature`).
3.  **Commit** your changes (`git commit -m 'Add some AmazingNewFeature'`).
4.  **Push** to the branch (`git push origin feature/AmazingNewFeature`).
5.  Open a **Pull Request**.

## 💡 Future Tasks & Roadmap

Here are some ideas for features that would make this bot even more powerful. Feel free to pick one up or suggest your own!

-   [ ] **Interactive Bot Commands:**
    -   [ ] `/start` & `/help`: Display a welcome message and a list of available commands.
    -   [ ] `/status`: Check if the bot is currently running and when the last check was performed.
    -   [ ] `/latest`: Manually request the 5 most recent projects.
    -   [ ] `/pause` & `/resume`: Allow the user to temporarily stop and restart notifications.

-   [ ] **Dynamic Search Filters via Commands:**
    -   [ ] **Keyword Search:** Add a command like `/search <keyword>` to find projects containing a specific word.
    -   [ ] **Category Filtering:** Allow users to set a preferred category (e.g., `/set_category برمجة`). The bot would then scrape `mostaql.com/projects/development` instead.
    -   [ ] **Budget Range:** Allow users to specify a budget (e.g., `/set_budget 100-500`). The bot would then modify the scraping URL accordingly.
    -   [ ] **Saving Preferences:** Store each user's filter preferences so they persist even after a restart.

-   [ ] **Advanced Features:**
    -   [ ] **Daily Summary:** A command `/summary` that sends a summary of all projects posted in the last 24 hours.
    -   [ ] **Multi-Language Support:** Add the ability to change the bot's notification language.
    -   [ ] **Error Notifications:** If the bot fails to scrape the site for any reason, it should send a notification to the admin/user.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).