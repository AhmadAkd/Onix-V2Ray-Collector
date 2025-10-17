#!/usr/bin/env python3
"""
بررسی فرمت‌های مختلف کانفیگ در کانال‌های تلگرام
"""

import asyncio
import aiohttp
import re
import logging

# تنظیم logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_different_formats():
    """بررسی فرمت‌های مختلف کانفیگ"""

    # کانال‌هایی که HTML زیادی دارند اما کانفیگ ندارند
    test_channels = [
        "@vlessvpn",      # 183935 characters
        "@vmessvpn",      # 29819 characters
        "@realityvpn",    # 31380 characters
        "@xrayvpn",       # 21482 characters
    ]

    # الگوهای مختلف کانفیگ
    patterns = {
        "vmess": r'vmess://[A-Za-z0-9+/=]+',
        "vless": r'vless://[^\\s]+',
        "trojan": r'trojan://[^\\s]+',
        "ss": r'ss://[A-Za-z0-9+/=]+',
        "ssr": r'ssr://[A-Za-z0-9+/=]+',
        "hysteria": r'hysteria://[^\\s]+',
        "hy2": r'hy2://[^\\s]+',
        "tuic": r'tuic://[^\\s]+',
        "reality": r'reality://[^\\s]+',
        "singbox": r'singbox://[^\\s]+',
        "xray": r'xray://[^\\s]+',
        "base64": r'[A-Za-z0-9+/=]{50,}',  # Base64 strings
        "json": r'\\{[^}]*"server"[^}]*\\}',  # JSON configs
        "yaml": r'[a-zA-Z0-9_-]+:\\s*[^\\n]+',  # YAML configs
    }

    connector = aiohttp.TCPConnector(ssl=False)

    for channel in test_channels:
        print(f"\\n{'='*60}")
        print(f"🔍 Checking {channel}")

        try:
            channel_username = channel[1:] if channel.startswith(
                '@') else channel
            url = f"https://t.me/s/{channel_username}"

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        print(f"HTML Length: {len(html)} characters")

                        # بررسی هر الگو
                        found_any = False
                        for pattern_name, pattern in patterns.items():
                            matches = re.findall(pattern, html, re.IGNORECASE)
                            if matches:
                                print(
                                    f"  ✅ {pattern_name}: {len(matches)} matches")
                                if len(matches) > 0:
                                    print(
                                        f"      Sample: {matches[0][:100]}...")
                                found_any = True

                        if not found_any:
                            print("  ❌ No configs found with any pattern")

                            # بررسی محتوای HTML
                            if "This channel is private" in html:
                                print("  🔒 Channel is PRIVATE")
                            elif "This channel doesn't exist" in html:
                                print("  ❌ Channel DOESN'T EXIST")
                            elif "No posts yet" in html:
                                print("  📭 NO POSTS YET")
                            elif "tgme_page_description" in html:
                                print("  📄 Channel has description but no posts")
                            else:
                                # بررسی کلمات کلیدی
                                keywords = ["vpn", "config",
                                            "proxy", "server", "v2ray", "xray"]
                                found_keywords = []
                                for keyword in keywords:
                                    if keyword.lower() in html.lower():
                                        found_keywords.append(keyword)

                                if found_keywords:
                                    print(
                                        f"  🔍 Found keywords: {', '.join(found_keywords)}")
                                else:
                                    print("  ❓ Unknown issue - no keywords found")

        except Exception as e:
            print(f"  ❌ Error: {e}")

        # انتظار کوتاه
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(check_different_formats())
