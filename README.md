<div align="center">

# 🔵 BLUE MOON — Username Sniper v1.0

### *Snipe the rarest names under the moonlight.*

A high-performance, multi-threaded tool for checking rare **4-character** and **4-letter** username availability across **Discord**, **TikTok**, and **Roblox**.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-Educational%20Use%20Only-red?style=for-the-badge)
![Threads](https://img.shields.io/badge/Threads-100%2B-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

</div>

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🚨 Security Warning](#-security-warning)
- [🛠️ Installation](#️-installation)
- [📖 How to Use](#-how-to-use)
- [🔑 Discord Token Guide](#-discord-token-guide)
- [🧠 API Endpoints](#-api-endpoints)
- [🖼️ Screenshots](#️-screenshots)
- [📜 License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Multi-Platform** | Simultaneously check usernames on Discord, TikTok, and Roblox |
| ⚡ **Blazing Fast** | Multi-threaded architecture supporting **100+ concurrent threads** |
| 🔒 **Proxy Engine** | Auto-scrapes from **8+ free proxy sources** or loads custom lists. Auto-removes dead proxies |
| 🔔 **Webhook Alerts** | Instant Discord embed notifications on every hit |
| 🧮 **Mass Generation** | Generates **456,976** (4-letter) or **500,000+** (4-char alphanumeric) combinations |
| 🖥️ **Sleek UI** | Dark blue-purple theme with live scan log and real-time stats |
| 💾 **Auto-Save** | Hits saved instantly to `hits.txt` — zero data loss on crash |
| 🛡️ **Rate-Limit Handler** | Smart exponential backoff to avoid IP bans and handle 429 errors |

---

## 🚨 Security Warning

> [!WARNING]
> **READ THIS BEFORE USING THE TOOL**
>
> - ❌ **NEVER** use your main Discord account token — always use a **burner account**.
> - ❌ **NEVER** share your token in chats, forums, or screenshots.
> - ✅ **HIGHLY RECOMMENDED** to run with an active **VPN** for extra security and to prevent ISP throttling.

---

## 🛠️ Installation

### Prerequisites

- **Python 3.11+** (for source execution)
- **Git** (for cloning)

---

### Option 1: Running from Source (Python)

```bash
# 1. Clone the repository
git clone https://github.com/jakubic769/BLUE-MOON-Sniper.git
cd BLUE-MOON-Sniper

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the tool
python blue_moon_sniper.py
