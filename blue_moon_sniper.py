#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════╗
║   BLUE MOON - Username Sniper v1.0            ║
║   Multi-Platform Username Checker             ║
║   Discord | TikTok | Roblox                   ║
╚═══════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import threading
import string
import random
import time
import os
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
from collections import deque
import itertools
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ======================== THEME COLORS ========================
BG_DARK        = "#0a0a12"
BG_PANEL       = "#0f0f1a"
BG_INPUT       = "#1a1a2e"
BLUE_PRIMARY   = "#7b2ff7"
BLUE_SECONDARY = "#4a00e0"
BLUE_GLOW      = "#9d4edd"
BLUE_DARK      = "#240046"
TEXT_WHITE     = "#ffffff"
TEXT_GRAY      = "#8888aa"
TEXT_GREEN     = "#00ff00"
TEXT_YELLOW    = "#ffcc00"
TEXT_RED       = "#ff4444"
TEXT_CYAN      = "#00ccff"
TEXT_ORANGE    = "#ff8800"
BORDER_COLOR   = "#2a2a40"
DISCORD_CLR    = "#5865F2"
TIKTOK_CLR     = "#ff0050"
ROBLOX_CLR     = "#00b06f"

# ======================== PROXY SOURCES ========================
PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/mertguvencli/Proxy-List-World/main/data.txt",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Brave/1.6.97",
]


# ======================== PROXY MANAGER ========================
class ProxyManager:
    def __init__(self):
        self.proxies = deque()
        self.lock = threading.Lock()
        self.bad_proxies = set()
        self._index = 0

    def add_proxy(self, proxy):
        with self.lock:
            p = proxy.strip()
            if p and p not in self.bad_proxies and p not in self.proxies:
                self.proxies.append(p)

    def get_proxy(self):
        with self.lock:
            if not self.proxies:
                return None
            self._index = (self._index + 1) % len(self.proxies)
            return self.proxies[self._index]

    def mark_bad(self, proxy):
        with self.lock:
            self.bad_proxies.add(proxy)
            try:
                self.proxies.remove(proxy)
            except ValueError:
                pass

    def count(self):
        with self.lock:
            return len(self.proxies)

    def get_proxy_dict(self):
        proxy = self.get_proxy()
        if proxy:
            return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        return None

    def load_from_file(self, filepath):
        count = 0
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if ":" in line and 5 < len(line) < 30:
                    self.add_proxy(line)
                    count += 1
        return count

    def scrape_proxies(self, log_cb=None):
        all_proxies = set()
        for source in PROXY_SOURCES:
            try:
                if log_cb:
                    log_cb(f"Scraping {source[:55]}...")
                r = requests.get(source, timeout=15, verify=False,
                                 headers={"User-Agent": random.choice(USER_AGENTS)})
                if r.status_code == 200:
                    for line in r.text.strip().splitlines():
                        line = line.strip()
                        if ":" in line and 5 < len(line) < 30:
                            all_proxies.add(line)
            except Exception as e:
                if log_cb:
                    log_cb(f"Failed: {str(e)[:50]}")
        with self.lock:
            for p in all_proxies:
                if p not in self.bad_proxies and p not in self.proxies:
                    self.proxies.append(p)
        if log_cb:
            log_cb(f"Scraped {len(all_proxies)} proxies | Active: {self.count()}")
        return len(all_proxies)


# ======================== USERNAME GENERATOR ========================
class UsernameGenerator:
    @staticmethod
    def generate_4letters():
        return ["".join(c) for c in itertools.product(string.ascii_lowercase, repeat=4)]

    @staticmethod
    def generate_4chars(target=500000):
        chars = string.ascii_lowercase + string.digits
        usernames = set()
        for c in itertools.product(string.ascii_lowercase, repeat=4):
            usernames.add("".join(c))
        while len(usernames) < target:
            usernames.add("".join(random.choices(chars, k=4)))
        return list(usernames)

    @staticmethod
    def save_to_file(filepath, usernames):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(usernames))
        return len(usernames)


# ======================== PLATFORM CHECKERS ========================
class PlatformChecker:

    @staticmethod
    def check_roblox(username, proxy_dict=None, timeout=10):
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            r = requests.post(
                "https://users.roblox.com/v1/usernames/users",
                json={"usernames": [username], "excludeBannedUsers": False},
                headers=headers,
                proxies=proxy_dict,
                timeout=timeout,
                verify=False,
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("data") and len(data["data"]) > 0:
                    return "taken"
                return "available"
            if r.status_code == 429:
                return "rate_limited"
            return "error"
        except requests.exceptions.ProxyError:
            return "proxy_error"
        except requests.exceptions.Timeout:
            return "timeout"
        except Exception:
            return "error"

    @staticmethod
    def check_tiktok(username, proxy_dict=None, timeout=12):
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }
        try:
            api_headers = headers.copy()
            api_headers["Accept"] = "application/json"
            api_headers["Referer"] = f"https://www.tiktok.com/@{username}"
            r = requests.get(
                f"https://www.tiktok.com/api/user/detail/?uniqueId={username}&language=en",
                headers=api_headers,
                proxies=proxy_dict,
                timeout=timeout,
                verify=False,
                allow_redirects=True,
            )
            if r.status_code == 200:
                try:
                    data = r.json()
                    if data.get("userInfo") and data["userInfo"].get("user"):
                        return "taken"
                    return "available"
                except (json.JSONDecodeError, ValueError):
                    pass
                text = r.text.lower()
                if f'"uniqueid":"{username.lower()}"' in text:
                    return "taken"
                if "couldn't find" in text or "not exist" in text or "not found" in text:
                    return "available"
            elif r.status_code == 404:
                return "available"
            elif r.status_code == 429:
                return "rate_limited"
        except requests.exceptions.ProxyError:
            return "proxy_error"
        except requests.exceptions.Timeout:
            return "timeout"
        except Exception:
            pass

        try:
            r = requests.get(
                f"https://www.tiktok.com/@{username}",
                headers=headers,
                proxies=proxy_dict,
                timeout=timeout,
                verify=False,
                allow_redirects=True,
            )
            if r.status_code == 200:
                text = r.text.lower()
                if f'"uniqueid":"{username.lower()}"' in text:
                    return "taken"
                if "couldn't find" in text or "not exist" in text:
                    return "available"
                if '"user"' not in text and '"uniqueid"' not in text:
                    return "available"
                return "taken"
            elif r.status_code == 404:
                return "available"
            elif r.status_code == 429:
                return "rate_limited"
        except requests.exceptions.ProxyError:
            return "proxy_error"
        except requests.exceptions.Timeout:
            return "timeout"
        except Exception:
            pass

        return "error"

    @staticmethod
    def check_discord(username, proxy_dict=None, timeout=10, token=None):
        if not token:
            return "no_token"
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Authorization": token,
                "Content-Type": "application/json",
            }
            r = requests.post(
                "https://discord.com/api/v10/unique-username/check-username",
                json={"username": username},
                headers=headers,
                proxies=proxy_dict,
                timeout=timeout,
                verify=False,
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("taken") is True:
                    return "taken"
                if data.get("taken") is False:
                    return "available"
                if data.get("code") == 200:
                    return "available"
                return "error"
            elif r.status_code == 429:
                retry_after = 1
                try:
                    retry_after = r.json().get("retry_after", 1)
                except:
                    pass
                time.sleep(min(retry_after, 5))
                return "rate_limited"
            elif r.status_code == 401:
                return "invalid_token"
            elif r.status_code == 400:
                return "invalid_format"
            return "error"
        except requests.exceptions.ProxyError:
            return "proxy_error"
        except requests.exceptions.Timeout:
            return "timeout"
        except Exception:
            return "error"


# ======================== MAIN APPLICATION ========================
class BlueMoonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BLUE MOON — Username Sniper v1.0")
        self.root.geometry("920x780")
        self.root.configure(bg=BG_DARK)
        self.root.minsize(850, 700)

        # State
        self.proxy_manager = ProxyManager()
        self.running = False
        self.usernames = []
        self.available = []
        self.checked = 0
        self.taken_count = 0
        self.available_count = 0
        self.error_count = 0
        self.total = 0
        self.lock = threading.Lock()
        self.start_time = 0

        self.setup_styles()
        self.build_ui()

    # -------------------- Styles --------------------
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Blue.Horizontal.TProgressbar",
                         troughcolor=BG_INPUT, background=BLUE_PRIMARY,
                         darkcolor=BLUE_PRIMARY, lightcolor=BLUE_GLOW,
                         bordercolor=BG_DARK)
        style.configure("Dark.TCombobox",
                         fieldbackground=BG_INPUT, background=BG_INPUT,
                         foreground=TEXT_WHITE, borderwidth=1,
                         arrowcolor=BLUE_PRIMARY)
        style.map("Dark.TCombobox",
                   fieldbackground=[("readonly", BG_INPUT)],
                   foreground=[("readonly", TEXT_WHITE)],
                   selectbackground=[("readonly", BLUE_DARK)])

    # -------------------- Build UI --------------------
    def build_ui(self):
        # === TOP BLUE LINE ===
        tk.Frame(self.root, bg=BLUE_PRIMARY, height=3).pack(fill="x")

        # === HEADER ===
        hdr = tk.Frame(self.root, bg=BG_DARK)
        hdr.pack(fill="x", padx=0, pady=(8, 0))

        title_frame = tk.Frame(hdr, bg=BG_DARK)
        title_frame.pack()
        tk.Label(title_frame, text="🔵 BLUE MOON", bg=BG_DARK, fg=BLUE_PRIMARY,
                 font=("Segoe UI", 28, "bold")).pack(side="left")
        tk.Label(title_frame, text="  SNIPER", bg=BG_DARK, fg=TEXT_GRAY,
                 font=("Segoe UI", 28, "bold")).pack(side="left")

        tk.Label(hdr, text="Multi-Platform Username Checker  •  Discord  |  TikTok  |  Roblox",
                 bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 9)).pack(pady=(0, 4))

        tk.Frame(self.root, bg=BLUE_DARK, height=1).pack(fill="x", padx=20, pady=(0, 6))

        # === MAIN CONTENT ===
        main = tk.Frame(self.root, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=14, pady=0)

        # ---------- SETTINGS PANEL ----------
        sp = self._panel(main)
        self._panel_title(sp, "⚙  SETTINGS")

        # Webhook
        r1 = tk.Frame(sp, bg=BG_PANEL); r1.pack(fill="x", padx=10, pady=2)
        self._label(r1, "Webhook URL:", 14).pack(side="left")
        self.webhook_entry = self._entry(r1); self.webhook_entry.pack(side="left", fill="x", expand=True)

        # Discord Token
        r2 = tk.Frame(sp, bg=BG_PANEL); r2.pack(fill="x", padx=10, pady=2)
        self._label(r2, "Discord Token:", 14).pack(side="left")
        self.token_entry = self._entry(r2, show="•"); self.token_entry.pack(side="left", fill="x", expand=True)

        # Threads / Timeout / Proxy buttons
        r3 = tk.Frame(sp, bg=BG_PANEL); r3.pack(fill="x", padx=10, pady=(2, 8))
        self._label(r3, "Threads:", 8).pack(side="left")
        self.threads_var = tk.StringVar(value="50")
        self._small_entry(r3, self.threads_var, 6).pack(side="left", padx=(0, 12))
        self._label(r3, "Timeout:", 8).pack(side="left")
        self.timeout_var = tk.StringVar(value="10")
        self._small_entry(r3, self.timeout_var, 6).pack(side="left", padx=(0, 16))

        self._btn(r3, "📁 Load Proxies", BG_INPUT, self.load_proxies).pack(side="left", padx=(0, 5))
        self._btn(r3, "🔍 Scrape Proxies", BLUE_DARK, self.scrape_proxies).pack(side="left", padx=(0, 10))
        self.proxy_lbl = tk.Label(r3, text="Proxies: 0", bg=BG_PANEL, fg=TEXT_CYAN,
                                   font=("Consolas", 9, "bold"))
        self.proxy_lbl.pack(side="left")

        # ---------- PLATFORM PANEL ----------
        pp = self._panel(main)
        pr = tk.Frame(pp, bg=BG_PANEL); pr.pack(fill="x", padx=10, pady=8)

        tk.Label(pr, text="Platforms:", bg=BG_PANEL, fg=BLUE_PRIMARY,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))

        self.discord_var = tk.BooleanVar(value=False)
        self.tiktok_var  = tk.BooleanVar(value=True)
        self.roblox_var  = tk.BooleanVar(value=True)

        for text, var, color in [("Discord", self.discord_var, DISCORD_CLR),
                                  ("TikTok", self.tiktok_var, TIKTOK_CLR),
                                  ("Roblox", self.roblox_var, ROBLOX_CLR)]:
            tk.Checkbutton(pr, text=text, variable=var, bg=BG_PANEL, fg=color,
                           selectcolor=BG_INPUT, activebackground=BG_PANEL,
                           activeforeground=color, font=("Segoe UI", 9, "bold"),
                           cursor="hand2", bd=0, highlightthickness=0).pack(side="left", padx=6)

        tk.Label(pr, text="   Mode:", bg=BG_PANEL, fg=BLUE_PRIMARY,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(12, 8))
        self.mode_var = tk.StringVar(value="4 Letters (a-z)")
        cb = ttk.Combobox(pr, textvariable=self.mode_var,
                           values=["4 Letters (a-z)", "4 Chars (a-z+0-9)"],
                           state="readonly", width=18, style="Dark.TCombobox")
        cb.pack(side="left", ipady=3)

        self._btn(pr, "⚡ Generate", BLUE_PRIMARY, self.generate_usernames).pack(side="left", padx=(14, 0), ipadx=8)
        self.gen_lbl = tk.Label(pr, text="Generated: 0", bg=BG_PANEL, fg=TEXT_GREEN,
                                 font=("Consolas", 9, "bold"))
        self.gen_lbl.pack(side="left", padx=(10, 0))

        # ---------- CONTROLS ----------
        cp = self._panel(main)
        cr = tk.Frame(cp, bg=BG_PANEL); cr.pack(fill="x", padx=10, pady=8)

        self.start_btn = tk.Button(cr, text="▶  START", bg="#00aa00", fg=TEXT_WHITE,
                                    font=("Segoe UI", 13, "bold"), bd=0, width=14,
                                    activebackground="#008800", cursor="hand2",
                                    command=self.start_scan)
        self.start_btn.pack(side="left", padx=(0, 8), ipady=5)

        self.stop_btn = tk.Button(cr, text="⏹  STOP", bg="#aa0000", fg=TEXT_WHITE,
                                   font=("Segoe UI", 13, "bold"), bd=0, width=14,
                                   activebackground="#880000", cursor="hand2",
                                   command=self.stop_scan, state="disabled")
        self.stop_btn.pack(side="left", padx=(0, 16), ipady=5)

        self._btn(cr, "💾 Export Hits", BG_INPUT, self.export_available).pack(side="left", padx=(0, 6))
        self._btn(cr, "📂 Load Usernames", BG_INPUT, self.load_usernames_file).pack(side="left")

        # ---------- STATS ----------
        sp2 = self._panel(main)
        sr = tk.Frame(sp2, bg=BG_PANEL); sr.pack(fill="x", padx=10, pady=(8, 4))

        self.stat_lbls = {}
        for name, color in [("Checked", TEXT_WHITE), ("Available", TEXT_GREEN),
                             ("Taken", TEXT_RED), ("Errors", TEXT_YELLOW),
                             ("CPS", TEXT_CYAN), ("ETA", TEXT_ORANGE)]:
            f = tk.Frame(sr, bg=BG_PANEL); f.pack(side="left", padx=(0, 16))
            tk.Label(f, text=f"{name}:", bg=BG_PANEL, fg=TEXT_GRAY,
                     font=("Segoe UI", 9)).pack(side="left")
            l = tk.Label(f, text="0", bg=BG_PANEL, fg=color,
                          font=("Consolas", 11, "bold"))
            l.pack(side="left", padx=(3, 0))
            self.stat_lbls[name] = l

        self.progress_var = tk.DoubleVar(value=0)
        ttk.Progressbar(sp2, variable=self.progress_var, maximum=100,
                         style="Blue.Horizontal.TProgressbar").pack(fill="x", padx=10, pady=(2, 8))

        # ---------- LIVE LOG ----------
        lp = self._panel(main)
        lh = tk.Frame(lp, bg=BG_PANEL); lh.pack(fill="x", padx=10, pady=(8, 2))
        tk.Label(lh, text="📋 LIVE SCAN LOG", bg=BG_PANEL, fg=BLUE_PRIMARY,
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        self._btn(lh, "Clear", BG_INPUT, self.clear_log, font_size=8).pack(side="right")

        self.log_text = tk.Text(lp, bg=BG_INPUT, fg=TEXT_WHITE, font=("Consolas", 9),
                                 bd=0, relief="flat", wrap="word",
                                 insertbackground=TEXT_WHITE,
                                 selectbackground=BLUE_PRIMARY, height=12)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for tag, color, bold in [
            ("hit", TEXT_GREEN, True), ("taken", "#555577", False),
            ("error", TEXT_YELLOW, False), ("info", TEXT_CYAN, False),
            ("rate", TEXT_ORANGE, False), ("header", BLUE_PRIMARY, True),
            ("proxy_err", "#ff6666", False),
        ]:
            font = ("Consolas", 9, "bold") if bold else ("Consolas", 9)
            self.log_text.tag_configure(tag, foreground=color, font=font)

        self.log("BLUE MOON Username Sniper v1.0 ready.", "info")
        self.log("1) Load/scrape proxies  2) Generate usernames  3) Hit START", "info")
        self.log("Tip: Discord requires a user token. Roblox & TikTok work without auth.", "info")

    # -------------------- UI Helpers --------------------
    def _panel(self, parent):
        f = tk.Frame(parent, bg=BG_PANEL, bd=0,
                     highlightbackground=BORDER_COLOR, highlightthickness=1)
        f.pack(fill="x", pady=(0, 6))
        return f

    def _panel_title(self, parent, text):
        tk.Label(parent, text=text, bg=BG_PANEL, fg=BLUE_PRIMARY,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(8, 4))

    def _label(self, parent, text, width=13):
        return tk.Label(parent, text=text, bg=BG_PANEL, fg=TEXT_GRAY,
                        font=("Segoe UI", 9), width=width, anchor="w")

    def _entry(self, parent, show=None):
        return tk.Entry(parent, bg=BG_INPUT, fg=TEXT_WHITE, insertbackground=TEXT_WHITE,
                        font=("Consolas", 9), bd=0, show=show,
                        highlightthickness=1, highlightbackground=BORDER_COLOR,
                        highlightcolor=BLUE_PRIMARY)

    def _small_entry(self, parent, var, width=6):
        return tk.Entry(parent, textvariable=var, bg=BG_INPUT, fg=TEXT_WHITE,
                        insertbackground=TEXT_WHITE, font=("Consolas", 9), bd=0,
                        width=width, highlightthickness=1,
                        highlightbackground=BORDER_COLOR, highlightcolor=BLUE_PRIMARY)

    def _btn(self, parent, text, bg, cmd, font_size=9):
        return tk.Button(parent, text=text, bg=bg, fg=TEXT_WHITE,
                         font=("Segoe UI", font_size, "bold"), bd=0,
                         activebackground="#2a2a4a", activeforeground=TEXT_WHITE,
                         cursor="hand2", command=cmd)

    # -------------------- Logging --------------------
    def log(self, msg, tag="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{ts}] {msg}\n", tag)
        self.log_text.see("end")
        lines = int(self.log_text.index("end-1c").split(".")[0])
        if lines > 8000:
            self.log_text.delete("1.0", "3000.0")

    def clear_log(self):
        self.log_text.delete("1.0", "end")

    # -------------------- Stats --------------------
    def update_stats(self):
        self.stat_lbls["Checked"].config(text=f"{self.checked:,}")
        self.stat_lbls["Available"].config(text=f"{self.available_count:,}")
        self.stat_lbls["Taken"].config(text=f"{self.taken_count:,}")
        self.stat_lbls["Errors"].config(text=f"{self.error_count:,}")
        if self.total > 0:
            pct = (self.checked / self.total) * 100
            self.progress_var.set(pct)
            elapsed = time.time() - self.start_time
            if self.checked > 0 and pct < 100:
                eta = (elapsed / self.checked) * (self.total - self.checked)
                m, s = divmod(int(eta), 60)
                self.stat_lbls["ETA"].config(text=f"{m}m{s}s")

    # -------------------- Proxy Actions --------------------
    def load_proxies(self):
        fp = filedialog.askopenfilename(title="Select Proxy File",
                                          filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if fp:
            c = self.proxy_manager.load_from_file(fp)
            self.proxy_lbl.config(text=f"Proxies: {self.proxy_manager.count()}")
            self.log(f"Loaded {c:,} proxies from file.", "info")

    def scrape_proxies(self):
        def _scrape():
            self.log("Scraping proxies from 8 sources...", "info")
            self.proxy_manager.scrape_proxies(
                log_cb=lambda m: self.root.after(0, lambda: self.log(m, "info")))
            self.root.after(0, lambda: self.proxy_lbl.config(
                text=f"Proxies: {self.proxy_manager.count()}"))
        threading.Thread(target=_scrape, daemon=True).start()

    # -------------------- Username Generation --------------------
    def generate_usernames(self):
        mode = self.mode_var.get()
        self.log(f"Generating usernames ({mode})... please wait.", "info")
        self.gen_lbl.config(text="Generating...")

        def _gen():
            t0 = time.time()
            if mode == "4 Letters (a-z)":
                self.usernames = UsernameGenerator.generate_4letters()
            else:
                self.usernames = UsernameGenerator.generate_4chars(500000)

            fname = f"usernames_{mode.split()[1].replace('(','').replace(')','')}_{int(time.time())}.txt"
            UsernameGenerator.save_to_file(fname, self.usernames)
            elapsed = time.time() - t0
            self.root.after(0, lambda: self.gen_lbl.config(
                text=f"Generated: {len(self.usernames):,}"))
            self.root.after(0, lambda: self.log(
                f"Generated {len(self.usernames):,} usernames in {elapsed:.1f}s → {fname}", "hit"))

        threading.Thread(target=_gen, daemon=True).start()

    def load_usernames_file(self):
        fp = filedialog.askopenfilename(title="Select Username File",
                                          filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if fp:
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                self.usernames = [l.strip() for l in f if l.strip()]
            self.gen_lbl.config(text=f"Loaded: {len(self.usernames):,}")
            self.log(f"Loaded {len(self.usernames):,} usernames from file.", "info")

    # -------------------- Webhook --------------------
    def send_webhook(self, username, platform):
        url = self.webhook_entry.get().strip()
        if not url:
            return
        try:
            platform_colors = {"discord": 0x5865F2, "tiktok": 0xFF0050, "roblox": 0x00B06F}
            embed = {
                "title": "🌙 USERNAME HIT!",
                "description": f"**`{username}`** is **AVAILABLE** on **{platform.upper()}**!",
                "color": platform_colors.get(platform, 0x7b2ff7),
                "footer": {"text": "BLUE MOON Sniper v1.0"},
                "timestamp": datetime.utcnow().isoformat(),
                "fields": [
                    {"name": "Username", "value": f"`{username}`", "inline": True},
                    {"name": "Platform", "value": platform.upper(), "inline": True},
                    {"name": "Length", "value": str(len(username)), "inline": True},
                ]
            }
            requests.post(url, json={"embeds": [embed], "username": "BLUE MOON",
                                      "avatar_url": "https://i.imgur.com/Z9oOZ3m.png"},
                          timeout=10, verify=False)
        except Exception:
            pass

    # -------------------- Scan Control --------------------
    def start_scan(self):
        if not self.usernames:
            messagebox.showwarning("No Usernames", "Generate or load usernames first!")
            return

        platforms = []
        if self.discord_var.get():
            if not self.token_entry.get().strip():
                messagebox.showwarning("Token Required",
                                        "Enter a Discord user token to check Discord usernames.\n\n"
                                        "You can get yours from browser DevTools → Application → Local Storage → token")
                return
            platforms.append("discord")
        if self.tiktok_var.get():
            platforms.append("tiktok")
        if self.roblox_var.get():
            platforms.append("roblox")

        if not platforms:
            messagebox.showwarning("No Platform", "Select at least one platform!")
            return

        self.running = True
        self.checked = 0
        self.available_count = 0
        self.taken_count = 0
        self.error_count = 0
        self.available = []
        self.total = len(self.usernames) * len(platforms)
        self.start_time = time.time()
        self.progress_var.set(0)

        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.update_stats()

        self.log("═" * 52, "header")
        self.log(f"  SCAN STARTED  |  {len(self.usernames):,} names × {len(platforms)} platforms", "header")
        self.log(f"  Platforms: {' | '.join(p.upper() for p in platforms)}", "header")
        self.log(f"  Proxies: {self.proxy_manager.count()}  |  Threads: {self.threads_var.get()}", "header")
        self.log("═" * 52, "header")

        threading.Thread(target=self._scan_worker, args=(platforms,), daemon=True).start()

    def stop_scan(self):
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log("⚠ Scan stopped by user.", "error")

    # -------------------- Scan Worker --------------------
    def _scan_worker(self, platforms):
        try:
            threads = max(1, int(self.threads_var.get()))
        except ValueError:
            threads = 50
        try:
            timeout = max(3, int(self.timeout_var.get()))
        except ValueError:
            timeout = 10

        token = self.token_entry.get().strip()
        queue = list(self.usernames)
        random.shuffle(queue)

        rate_delays = {p: 0 for p in platforms}
        consecutive_errors = {p: 0 for p in platforms}

        def check_one(username):
            if not self.running:
                return

            for platform in platforms:
                if not self.running:
                    break

                if rate_delays[platform] > 0:
                    time.sleep(rate_delays[platform])
                    rate_delays[platform] = 0

                proxy_dict = self.proxy_manager.get_proxy_dict()

                if platform == "roblox":
                    result = PlatformChecker.check_roblox(username, proxy_dict, timeout)
                elif platform == "tiktok":
                    result = PlatformChecker.check_tiktok(username, proxy_dict, timeout)
                elif platform == "discord":
                    result = PlatformChecker.check_discord(username, proxy_dict, timeout, token)
                else:
                    result = "error"

                if result == "available":
                    consecutive_errors[platform] = 0
                    with self.lock:
                        self.available.append((username, platform))
                        self.available_count += 1
                    self.root.after(0, lambda u=username, p=platform: self.log(
                        f"✅ HIT!  {u}  →  {p.upper()}  →  AVAILABLE!", "hit"))
                    self.root.after(0, lambda u=username, p=platform: self.send_webhook(u, p))
                    self._save_hit(username, platform)

                elif result == "taken":
                    consecutive_errors[platform] = 0
                    with self.lock:
                        self.taken_count += 1
                    self.root.after(0, lambda u=username, p=platform: self.log(
                        f"❌ {u} → {p.upper()} → Taken", "taken"))

                elif result == "rate_limited":
                    consecutive_errors[platform] += 1
                    rate_delays[platform] = min(0.5 * consecutive_errors[platform], 3.0)
                    with self.lock:
                        self.error_count += 1
                    self.root.after(0, lambda u=username, p=platform: self.log(
                        f"⏳ {u} → {p.upper()} → Rate Limited (backoff {rate_delays[platform]:.1f}s)", "rate"))

                elif result == "proxy_error":
                    with self.lock:
                        self.error_count += 1
                    if proxy_dict:
                        raw = self.proxy_manager.get_proxy()
                        if raw:
                            self.proxy_manager.mark_bad(raw)
                    self.root.after(0, lambda u=username, p=platform: self.log(
                        f"🔌 {u} → {p.upper()} → Proxy Error (removed)", "proxy_err"))

                elif result == "timeout":
                    with self.lock:
                        self.error_count += 1
                    self.root.after(0, lambda u=username, p=platform: self.log(
                        f"⏱ {u} → {p.upper()} → Timeout", "error"))

                elif result == "no_token":
                    self.root.after(0, lambda: self.log(
                        "🔑 Discord token missing — skipping Discord checks", "error"))
                    with self.lock:
                        self.error_count += 1

                elif result == "invalid_token":
                    self.root.after(0, lambda: self.log(
                        "🚫 Discord token is INVALID! Stopping Discord checks.", "error"))
                    if "discord" in platforms:
                        platforms.remove("discord")
                    with self.lock:
                        self.error_count += 1

                elif result == "invalid_format":
                    with self.lock:
                        self.error_count += 1

                else:  # error
                    consecutive_errors[platform] += 1
                    with self.lock:
                        self.error_count += 1
                    if consecutive_errors[platform] > 10:
                        rate_delays[platform] = 1.0
                        consecutive_errors[platform] = 0

            with self.lock:
                self.checked += len(platforms)

            self.root.after(0, self.update_stats)

            elapsed = time.time() - self.start_time
            if elapsed > 0 and self.checked > 0:
                cps = self.checked / elapsed
                self.root.after(0, lambda c=cps: self.stat_lbls["CPS"].config(text=f"{c:.1f}/s"))

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for username in queue:
                if not self.running:
                    break
                futures.append(executor.submit(check_one, username))
                time.sleep(0.005)

            for future in as_completed(futures):
                if not self.running:
                    executor.shutdown(wait=False)
                    break

        elapsed = time.time() - self.start_time
        self.root.after(0, lambda: self._finish_scan(elapsed))

    def _save_hit(self, username, platform):
        try:
            with open("hits.txt", "a", encoding="utf-8") as f:
                f.write(f"{username} | {platform} | {datetime.now().isoformat()}\n")
        except Exception:
            pass

    def _finish_scan(self, elapsed):
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        m, s = divmod(int(elapsed), 60)
        self.log("═" * 52, "header")
        self.log(f"  SCAN COMPLETE  |  Time: {m}m {s}s", "header")
        self.log(f"  Checked: {self.checked:,}  |  Available: {self.available_count:,}"
                 f"  |  Taken: {self.taken_count:,}  |  Errors: {self.error_count:,}", "header")
        self.log("═" * 52, "header")
        if self.available:
            self.log(f"💾 All hits saved to hits.txt ({len(self.available)} total)", "hit")

    # -------------------- Export --------------------
    def export_available(self):
        if not self.available:
            messagebox.showinfo("No Hits", "No available usernames found yet.")
            return
        fp = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text", "*.txt")],
                                            title="Export Available Usernames")
        if fp:
            with open(fp, "w", encoding="utf-8") as f:
                for username, platform in self.available:
                    f.write(f"{username} | {platform}\n")
            self.log(f"Exported {len(self.available):,} hits → {fp}", "hit")


# ======================== ENTRY POINT ========================
def main():
    root = tk.Tk()
    root.update_idletasks()
    w, h = 920, 780
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    try:
        root.iconbitmap(default="")
    except Exception:
        pass

    app = BlueMoonApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
