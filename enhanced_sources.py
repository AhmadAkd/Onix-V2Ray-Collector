#!/usr/bin/env python3
"""
Enhanced Sources for V2Ray Collector
منابع پیشرفته و جدید برای جمع‌آوری کانفیگ‌ها
"""

# منابع جدید پیشنهادی
ENHANCED_SOURCES = [
    # منابع GitHub جدید
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",

    # منابع Telegram Bot API
    "https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",

    # منابع Discord
    "https://discord.com/api/v9/channels/{CHANNEL_ID}/messages",

    # منابع Reddit
    "https://www.reddit.com/r/VPN/r/V2Ray.json",

    # منابع API های عمومی
    "https://api.github.com/repos/{owner}/{repo}/contents/configs",

    # منابع Cloudflare Workers
    "https://worker-name.workers.dev/api/configs",

    # منابع VPS Providers
    "https://api.digitalocean.com/v2/droplets",

    # منابع CDN
    "https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/configs/",
]

# منابع تلگرام پیشنهادی
TELEGRAM_SOURCES = [
    "@v2rayngvpn",
    "@freev2ray",
    "@vpnconfigs",
    "@proxynetwork",
    "@v2raycollect",
    "@shadowsocks",
    "@trojanvpn",
    "@hysteriavpn",
    "@wireguardvpn",
]

# منابع Discord پیشنهادی
DISCORD_SOURCES = [
    "https://discord.com/api/v9/channels/1234567890/messages",  # مثال
]

# منابع Reddit پیشنهادی
REDDIT_SOURCES = [
    "https://www.reddit.com/r/VPN/hot.json",
    "https://www.reddit.com/r/V2Ray/hot.json",
    "https://www.reddit.com/r/shadowsocks/hot.json",
]
