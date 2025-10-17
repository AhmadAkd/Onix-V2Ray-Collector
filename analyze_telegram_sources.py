#!/usr/bin/env python3
"""
تحلیل منابع تلگرام - چرا بیشتر منابع کار نمی‌کنند؟
"""

import asyncio
import aiohttp
import re
import logging
from telegram_collector import TELEGRAM_SOURCES

# تنظیم logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_telegram_source(source):
    """تست یک منبع تلگرام"""
    try:
        channel_username = source.channel_id[1:] if source.channel_id.startswith(
            '@') else source.channel_id
        url = f"https://t.me/s/{channel_username}"

        print(f"\\n🔍 Testing {source.channel_name} ({source.channel_id}):")
        print(f"   URL: {url}")

        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                print(f"   Status: {response.status}")

                if response.status == 200:
                    html = await response.text()
                    print(f"   HTML Length: {len(html)} characters")

                    # بررسی وجود کانفیگ‌ها
                    configs = []
                    patterns = [
                        r'vmess://[A-Za-z0-9+/=]+',
                        r'vless://[^\\s]+',
                        r'trojan://[^\\s]+',
                        r'ss://[A-Za-z0-9+/=]+',
                        r'ssr://[A-Za-z0-9+/=]+',
                        r'hysteria://[^\\s]+',
                        r'hy2://[^\\s]+',
                        r'tuic://[^\\s]+'
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        configs.extend(matches)

                    print(f"   Configs Found: {len(configs)}")

                    if len(configs) > 0:
                        print(f"   ✅ WORKING - Found {len(configs)} configs")
                        print(f"   Sample: {configs[0][:50]}...")
                    else:
                        print(f"   ❌ NO CONFIGS - Channel might be:")
                        print(f"      - Private/restricted")
                        print(f"      - No recent configs")
                        print(f"      - Different format")

                        # بررسی محتوای HTML
                        if "This channel is private" in html:
                            print(f"      - Channel is PRIVATE")
                        elif "This channel doesn't exist" in html:
                            print(f"      - Channel DOESN'T EXIST")
                        elif "No posts yet" in html:
                            print(f"      - NO POSTS YET")
                        else:
                            print(f"      - Unknown issue")
                else:
                    print(f"   ❌ HTTP Error: {response.status}")

    except Exception as e:
        print(f"   ❌ Error: {e}")


async def analyze_all_sources():
    """تحلیل تمام منابع"""
    print("🔍 Analyzing Telegram Sources...")
    print(f"Total sources: {len(TELEGRAM_SOURCES)}")

    working_sources = []
    broken_sources = []

    for i, source in enumerate(TELEGRAM_SOURCES):
        print(f"\\n{'='*60}")
        print(f"Source {i+1}/{len(TELEGRAM_SOURCES)}")

        await test_telegram_source(source)

        # انتظار کوتاه برای جلوگیری از rate limiting
        await asyncio.sleep(1)

    print(f"\\n{'='*60}")
    print("📊 SUMMARY:")
    print(f"Total sources tested: {len(TELEGRAM_SOURCES)}")
    print(f"Working sources: {len(working_sources)}")
    print(f"Broken sources: {len(broken_sources)}")

if __name__ == "__main__":
    asyncio.run(analyze_all_sources())
