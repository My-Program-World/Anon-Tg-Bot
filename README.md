# Anon-Tg-Bot

# Telegram Bot with Replies, Buttons, and Reactions

A Telegram bot built with **Python** and **aiogram**, supporting message replies, inline/reply keyboards, user queues. Designed to be easy to extend and customize.

---

## Features

- Reply to messages (replies)
- Inline and Reply keyboards
- User queue management
- Command handling
- Easy to configure and extend

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/My-Program-World/Anon-Tg-Bot
cd bot
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux / MacOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 4. Start Redis Server

This bot uses **Redis** to store user queues and other temporary data.  

### Install Redis

- **Windows:**  
[Redis for Windows](https://github.com/tporadowski/redis/releases)

- **Linux / MacOS:**  
```bash
# Ubuntu / Debian
sudo apt install redis-server

# MacOS
brew install redis
```

### Start Redis
```bash
redis-server
```

> **Note:** By default, the bot connects to Redis at `localhost:6379`.  
> You can change these settings in `storage.py` if needed.

## 5. Create `.env` File

Create a `.env` file in the project root and add your Telegram bot token as a variable:

```env
TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
```

### 6. Run `main.py`