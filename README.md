🔵 BLUE MOON — Username Sniper v1.0

A high-speed, multi-threaded multi-tool for checking rare 4-character and 4-letter username availability across Discord, TikTok, and Roblox. Built with a sleek dark blue-purple "Blue Moon" UI, proxy rotation, live scanning logs, and instant Discord webhook notifications for hits.

✨ Features

🎯 Multi-Platform: Simultaneously check usernames on Discord, TikTok, and Roblox.
⚡ Blazing Fast: Multi-threaded architecture (up to 100+ threads) for rapid scanning.
🔒 Proxy Engine: Scrapes from 8+ free proxy sources or loads your own list. Auto-removes dead proxies on the fly.
🔔 Webhook Alerts: Get instant Discord embed notifications the second a hit is found.
🧮 Mass Generation: Generates 456,976 (4-letter) or 500,000+ (4-char alphanumeric) username combinations.
🖥️ Sleek UI: Dark theme with blue-purple accents, live scan log, and real-time statistics (CPS, ETA, hits).
💾 Auto-Save: Hits are appended to hits.txt instantly—no data lost if the app crashes.
🛡️ Rate-Limit Handler: Smart exponential backoff to prevent IP bans and handle 429 errors.
⚠️ SECURITY WARNING (READ FIRST!)

NEVER use your main Discord account token. Always use a burner Discord account.
NEVER share your token in chats, forums, or screenshots.
It is highly recommended to run this tool with an active VPN for an extra layer of security and to prevent ISP throttling.

🛠️ Installation

Option 1: Running from Source (Python)

Clone the repository:
git clone https://github.com/jakubic769/BLUE-MOON-Sniper.git
cd BLUE-MOON-Sniper

Install dependencies:
pip install -r requirements.txt

Run the tool:
python blue_moon_sniper.py

Option 2: Compiling to .exe (Windows)

If you want to build a standalone executable that you can run on any Windows machine without installing Python:

Ensure Python and dependencies are installed (follow Option 1, steps 1 & 2).

Run the included build script:
build.bat
(Or compile manually using Pyinstaller:)
pyinstaller --onefile --console --name "BLUE_MOON_Sniper" blue_moon_sniper.py

Your standalone executable will be generated in the dist/ folder: dist\BLUE_MOON_Sniper.exe

Option 3: Download Pre-Built EXE

Go to the Releases page on the repository.
Download the latest BLUE_MOON_Sniper.zip.
Extract the zip and run BLUE_MOON_Sniper.exe.
📖 How-To-Use Tutorial

Step 1: Set Up Proxies
Proxies are required to scan fast without getting your IP blocked.

Option A (Auto-Scrape): Click the 🔍 Scrape Proxies button. The tool will fetch thousands of free proxies from 8 different sources.
Option B (Your own list): Click 📁 Load Proxies and select a .txt file containing proxies in ip:port format (one per line).
Wait for the "Proxies: XXXX" counter to populate.
Step 2: Generate Usernames
You need a list of usernames to check.

Choose your mode in the Platforms section:
4 Letters (a-z): Generates all 456,976 combinations (aaaa → zzzz).
4 Chars (a-z+0-9): Generates 500,000+ alphanumeric combinations (e.g., a1b2, z9x8).
Click ⚡ Generate.
A file named usernames_...txt will be created in the folder. The "Generated" counter will update.
(Alternatively, click 📂 Load Usernames to use your own custom .txt file).

Step 3: Configure Platforms & Auth
Check the boxes for the platforms you want to scan:

☑️ Roblox: Works out of the box. No auth needed.
☑️ TikTok: Works out of the box. Uses API + HTML fallback.
☑️ Discord: Requires a User Token. Paste a token from a burner account into the Discord Token field.
Step 4: Set Up Webhooks (Optional)
If you want to receive notifications when an available username is found:

Create a Discord channel webhook.
Paste the Webhook URL into the Webhook URL field.
Step 5: Start Sniping!

Adjust Threads (Recommended: 50 for Roblox/TikTok, 15 for Discord) and Timeout (Default: 10).
Hit ▶ START.
Watch the Live Scan Log:
✅ HIT! = The username is available!
❌ Taken = The username is already in use.
⏳ Rate Limited = Backing off to avoid a ban.
🔌 Proxy Error = Bad proxy removed.
Hits are instantly saved to hits.txt and sent to your webhook (if configured).
Step 6: Export Results
Once the scan finishes (or you click ⏹ STOP), click 💾 Export Hits to save all available usernames neatly to a file.

🔑 How to Get a Discord Token (For Burners Only!)

Open Discord in your web browser and log into your burner account.
Press F12 to open Developer Tools.
Go to the Application tab.
On the left sidebar, expand Local Storage and click https://discord.com.
Find the key named token in the right panel.
Copy the value (it looks like MTUwNjY...).
Paste it into the BLUE MOON Discord Token field.
🧠 API Endpoints Used

Platform	Method	Endpoint	Auth
Roblox	POST	users.roblox.com/v1/usernames/users	None
TikTok	GET	tiktok.com/api/user/detail/?uniqueId={name}	None
Discord	POST	discord.com/api/v10/unique-username/check-username	User Token
📜 License

This project is for educational purposes only. Use at your own risk. The developer is not responsible for any actions taken with this tool.

BLUE MOON 🔵 — Snipe the rarest names under the moonlight.
