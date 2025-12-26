# 🎵🎬 Telegram Media Downloader Bot

A **powerful, fast, and clean Telegram bot** that lets users download **songs and videos from YouTube** using simple commands. Built with **Python**, **python-telegram-bot v20+**, and **yt-dlp**, and fully compatible with **Railway hosting**.

---

## ✨ Features

* 🎵 **/song** – Download high-quality audio (M4A)
* 🎬 **/video** – Download compressed MP4 videos (Telegram-safe size)
* 🔍 Search by **song/video name** or **direct URL**
* 📊 Rich metadata in captions:

  * Title
  * Channel
  * Category
  * Upload date
  * Duration
  * Views, likes & comments
  * File size
  * License
  * Age restriction status
* 🙋 Shows **requester username mention**
* 🧹 Automatically **cleans service messages** (Downloading…)
* 📎 Inline **Developer button** under every upload
* 🚀 Optimized for **Railway / cloud hosting**

---

## 📸 Example Caption Output

```
🎵 Title: SANAM RE Title Song FULL VIDEO
📺 Channel: T-Series
📂 Category: Music
📅 Upload Date: 2016-02-26
⏰ Duration: 4:29
👀 Views: 878,934,773
👍 Likes: 3,772,552
💬 Comments: 99,000
📦 File Size: 4.71 MB
⚖️ License: Standard
🔞 Age Restricted: No

🙋 Requested by: @username
```

---

## 🧾 Commands

| Command             | Description               |
| ------------------- | ------------------------- |
| `/start`            | Show help & usage         |
| `/song <name/url>`  | Download audio            |
| `/video <name/url>` | Download compressed video |

**Examples:**

```
/song sanam re
/video sanam re
```

---

## ⚙️ Tech Stack

* **Python 3.11+**
* **python-telegram-bot v20+**
* **yt-dlp**
* **FFmpeg** (recommended)
* **Railway.app** (hosting)

---

## 🚀 Deployment (Railway)

1. Fork this repository
2. Create a Railway project
3. Add environment variable:

```
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

4. Install FFmpeg in Railway (recommended)
5. Deploy 🎉

---

## 📂 Project Structure

```
├── bot.py
├── downloads/
├── requirements.txt
├── .env
└── README.md
```

---

## 🛡️ Notes

* Telegram bot upload limit: **~50MB**
* Videos are auto-filtered to fit Telegram limits
* Some metadata (likes/comments) may be hidden by YouTube

---

## 👨‍💻 Developer

* **Name:** Maduwa
* **Telegram:** [@deweni2](https://t.me/deweni2)
* **GitHub:** [https://github.com/MaDuWA-LK](https://github.com/MaDuWA-LK)

> Built with ❤️ for the Telegram community

---

## ⭐ Support

If you like this project:

* ⭐ Star this repository
* 🍴 Fork it
* 👤 Follow **@MaDuWA-LK** on GitHub
* 📢 Share with friends

---

## 📜 License

This project is licensed under the **MIT License**.

---

### ⚠️ Disclaimer

This bot is for **educational purposes only**. Downloading copyrighted content may violate YouTube's Terms of Service. Use responsibly.

---

✨ *Happy Downloading!*
