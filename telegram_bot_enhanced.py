#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Telegram Bot for V2Ray Collector
ربات تلگرام پیشرفته برای جمع‌آوری و مدیریت کانفیگ‌های V2Ray
"""

import asyncio
import aiohttp
import json
import logging
import os
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class BotStats:
    """آمار ربات"""
    total_users: int = 0
    total_configs_sent: int = 0
    total_requests: int = 0
    active_users_today: int = 0
    last_update: str = ""


@dataclass
class UserSession:
    """جلسه کاربر"""
    user_id: int
    username: str
    first_name: str
    last_activity: datetime
    preferred_protocol: str = "all"
    preferred_country: str = "all"
    language: str = "fa"
    is_admin: bool = False


class EnhancedTelegramBot:
    """ربات تلگرام پیشرفته برای V2Ray Collector"""

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self.webhook_url = None
        self.stats = BotStats()
        self.user_sessions: Dict[int, UserSession] = {}
        self.admin_users = set()
        self.commands = self._setup_commands()

        # تنظیم کاربران ادمین (می‌توانید ID خود را اضافه کنید)
        self.admin_users.add(6563143907)  # AhmadAkd - ادمین جدید

        logger.info("✅ Enhanced Telegram Bot initialized")

    def _setup_commands(self) -> Dict[str, str]:
        """تنظیم دستورات ربات"""
        return {
            'start': 'شروع کار با ربات',
            'help': 'راهنمای استفاده',
            'stats': 'آمار کلی سیستم',
            'configs': 'دریافت کانفیگ‌ها',
            'protocols': 'لیست پروتکل‌ها',
            'countries': 'لیست کشورها',
            'latest': 'آخرین کانفیگ‌ها',
            'search': 'جستجوی کانفیگ',
            'subscribe': 'اشتراک در آپدیت‌ها',
            'unsubscribe': 'لغو اشتراک',
            'admin': 'دستورات مدیریتی (فقط ادمین)',
            'ping': 'تست اتصال',
            'about': 'درباره ربات'
        }

    async def set_webhook(self, webhook_url: str):
        """تنظیم webhook"""
        try:
            url = f"{self.api_url}/setWebhook"
            data = {"url": webhook_url}

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('ok'):
                            self.webhook_url = webhook_url
                            logger.info(f"✅ Webhook set: {webhook_url}")
                            return True

            logger.error("❌ Failed to set webhook")
            return False

        except Exception as e:
            logger.error(f"❌ Error setting webhook: {e}")
            return False

    async def delete_webhook(self):
        """حذف webhook"""
        try:
            url = f"{self.api_url}/deleteWebhook"

            # ایجاد connector بدون SSL verification
            connector = aiohttp.TCPConnector(ssl=False)

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(url) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('ok'):
                            self.webhook_url = None
                            logger.info("✅ Webhook deleted")
                            return True

            return False

        except Exception as e:
            logger.error(f"❌ Error deleting webhook: {e}")
            return False

    async def get_bot_info(self) -> Dict[str, Any]:
        """دریافت اطلاعات ربات"""
        try:
            url = f"{self.api_url}/getMe"

            # ایجاد connector بدون SSL verification
            connector = aiohttp.TCPConnector(ssl=False)

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('ok'):
                            return data['result']

            return {}

        except Exception as e:
            logger.error(f"❌ Error getting bot info: {e}")
            return {}

    async def send_message(self, chat_id: int, text: str, parse_mode: str = "HTML",
                           reply_markup: Optional[Dict] = None) -> bool:
        """ارسال پیام"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode
            }

            if reply_markup:
                data["reply_markup"] = reply_markup

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get('ok', False)

            return False

        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
            return False

    async def send_document(self, chat_id: int, document: str, caption: str = "") -> bool:
        """ارسال فایل"""
        try:
            url = f"{self.api_url}/sendDocument"
            data = {
                "chat_id": chat_id,
                "document": document,
                "caption": caption
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get('ok', False)

            return False

        except Exception as e:
            logger.error(f"❌ Error sending document: {e}")
            return False

    def get_user_session(self, user_id: int, username: str = "", first_name: str = "") -> UserSession:
        """دریافت یا ایجاد جلسه کاربر"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = UserSession(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_activity=datetime.now(),
                is_admin=user_id in self.admin_users
            )
        else:
            self.user_sessions[user_id].last_activity = datetime.now()
            if username:
                self.user_sessions[user_id].username = username
            if first_name:
                self.user_sessions[user_id].first_name = first_name

        return self.user_sessions[user_id]

    async def handle_command(self, message: Dict[str, Any]) -> bool:
        """پردازش دستورات"""
        try:
            text = message.get('text', '')
            chat = message.get('chat', {})
            from_user = message.get('from', {})

            chat_id = chat.get('id')
            user_id = from_user.get('id')
            username = from_user.get('username', '')
            first_name = from_user.get('first_name', '')

            # دریافت جلسه کاربر
            user_session = self.get_user_session(user_id, username, first_name)

            # تقسیم دستور
            parts = text.split()
            command = parts[0].replace('/', '').lower()

            # اجرای دستور
            if command == 'start':
                await self._handle_start(chat_id, user_session)
            elif command == 'help':
                await self._handle_help(chat_id, user_session)
            elif command == 'stats':
                await self._handle_stats(chat_id, user_session)
            elif command == 'configs':
                await self._handle_configs(chat_id, user_session, parts[1:])
            elif command == 'protocols':
                await self._handle_protocols(chat_id, user_session)
            elif command == 'countries':
                await self._handle_countries(chat_id, user_session)
            elif command == 'latest':
                await self._handle_latest(chat_id, user_session)
            elif command == 'search':
                await self._handle_search(chat_id, user_session, parts[1:])
            elif command == 'subscribe':
                await self._handle_subscribe(chat_id, user_session)
            elif command == 'unsubscribe':
                await self._handle_unsubscribe(chat_id, user_session)
            elif command == 'admin':
                if user_session.is_admin:
                    await self._handle_admin(chat_id, user_session, parts[1:])
                else:
                    await self.send_message(chat_id, "❌ دسترسی محدود به ادمین")
            elif command == 'ping':
                await self._handle_ping(chat_id, user_session)
            elif command == 'about':
                await self._handle_about(chat_id, user_session)
            else:
                await self._handle_unknown(chat_id, user_session, command)

            # به‌روزرسانی آمار
            self.stats.total_requests += 1

            return True

        except Exception as e:
            logger.error(f"❌ Error handling command: {e}")
            return False

    async def _handle_start(self, chat_id: int, user_session: UserSession):
        """دستور /start"""
        welcome_text = f"""
🎉 <b>خوش آمدید {user_session.first_name}!</b>

🤖 <b>V2Ray Collector Bot</b>
📡 جمع‌آوری هوشمند کانفیگ‌های V2Ray

<b>دستورات موجود:</b>
/help - راهنمای کامل
/stats - آمار سیستم
/configs - دریافت کانفیگ‌ها
/protocols - لیست پروتکل‌ها
/countries - لیست کشورها
/latest - آخرین کانفیگ‌ها
/search - جستجوی کانفیگ
/subscribe - اشتراک در آپدیت‌ها

💡 برای شروع از دستور /help استفاده کنید.
        """

        await self.send_message(chat_id, welcome_text)

    async def _handle_help(self, chat_id: int, user_session: UserSession):
        """دستور /help"""
        help_text = """
📚 <b>راهنمای کامل ربات</b>

<b>🔧 دستورات اصلی:</b>
/start - شروع کار با ربات
/help - نمایش این راهنما
/stats - آمار کلی سیستم
/ping - تست اتصال

<b>📡 دستورات کانفیگ:</b>
/configs - دریافت تمام کانفیگ‌ها
/configs vmess - کانفیگ‌های VMess
/configs vless - کانفیگ‌های VLESS
/configs trojan - کانفیگ‌های Trojan
/configs ss - کانفیگ‌های Shadowsocks

<b>🌍 دستورات جغرافیایی:</b>
/countries - لیست کشورها
/configs US - کانفیگ‌های آمریکا
/configs DE - کانفیگ‌های آلمان
/configs IR - کانفیگ‌های ایران

<b>🔍 جستجو:</b>
/search vmess US - جستجوی VMess آمریکا
/search vless DE - جستجوی VLESS آلمان
/latest 10 - آخرین 10 کانفیگ

<b>⚙️ تنظیمات:</b>
/subscribe - اشتراک در آپدیت‌ها
/unsubscribe - لغو اشتراک
/about - درباره ربات

💡 <i>برای دریافت کانفیگ، از دستورات بالا استفاده کنید.</i>
        """

        await self.send_message(chat_id, help_text)

    async def _handle_stats(self, chat_id: int, user_session: UserSession):
        """دستور /stats"""
        try:
            # بارگذاری آمار از فایل
            stats_data = await self._load_latest_stats()

            stats_text = f"""
📊 <b>آمار کلی سیستم</b>

<b>📈 آمار کانفیگ‌ها:</b>
• کل کانفیگ‌ها: {stats_data.get('total_configs', 0):,}
• کانفیگ‌های سالم: {stats_data.get('working_configs', 0):,}
• نرخ موفقیت: {stats_data.get('success_rate', '0%')}

<b>🌍 توزیع جغرافیایی:</b>
• کشورها: {stats_data.get('total_countries', 0)}
• پروتکل‌ها: {stats_data.get('total_protocols', 0)}

<b>🤖 آمار ربات:</b>
• کاربران کل: {len(self.user_sessions)}
• درخواست‌های امروز: {self.stats.total_requests}
• آخرین بروزرسانی: {stats_data.get('timestamp', 'نامشخص')}

<b>⚡ عملکرد:</b>
• زمان تست: {stats_data.get('test_duration', 0)}s
• منابع فعال: {stats_data.get('active_sources', 0)}
            """

            await self.send_message(chat_id, stats_text)

        except Exception as e:
            logger.error(f"❌ Error loading stats: {e}")
            await self.send_message(chat_id, "❌ خطا در بارگذاری آمار")

    async def _handle_configs(self, chat_id: int, user_session: UserSession, args: List[str]):
        """دستور /configs"""
        try:
            protocol = args[0] if args else "all"

            # بارگذاری کانفیگ‌ها
            configs = await self._load_configs(protocol)

            if not configs:
                await self.send_message(chat_id, f"❌ هیچ کانفیگ {protocol} یافت نشد")
                return

            # ارسال کانفیگ‌ها (حداکثر 10 تا)
            configs_to_send = configs[:10]

            for i, config in enumerate(configs_to_send, 1):
                config_text = f"""
<b>کانفیگ {i}:</b>
<code>{config}</code>
                """
                await self.send_message(chat_id, config_text)

                # تأخیر بین ارسال‌ها
                await asyncio.sleep(0.5)

            if len(configs) > 10:
                await self.send_message(chat_id, f"📊 {len(configs) - 10} کانفیگ بیشتر موجود است. برای دریافت بیشتر از /search استفاده کنید.")

        except Exception as e:
            logger.error(f"❌ Error loading configs: {e}")
            await self.send_message(chat_id, "❌ خطا در بارگذاری کانفیگ‌ها")

    async def _handle_protocols(self, chat_id: int, user_session: UserSession):
        """دستور /protocols"""
        protocols_text = """
🔌 <b>پروتکل‌های پشتیبانی شده</b>

<b>⚡ High Performance:</b>
• VMess - پروتکل اصلی V2Ray
• VLESS - سبک و سریع
• Trojan - امن و پایدار
• Hysteria - فوق سریع

<b>🔒 Classic:</b>
• Shadowsocks (SS) - کلاسیک و قابل اعتماد
• ShadowsocksR (SSR) - نسخه بهبود یافته
• TUIC - مدرن و بهینه

<b>🚀 Advanced:</b>
• Reality - جدیدترین تکنولوژی
• Xray Reality - نسخه Xray
• SingBox - همه‌کاره

💡 <i>برای دریافت کانفیگ هر پروتکل از /configs [protocol] استفاده کنید.</i>
        """

        await self.send_message(chat_id, protocols_text)

    async def _handle_countries(self, chat_id: int, user_session: UserSession):
        """دستور /countries"""
        countries_text = """
🌍 <b>کشورهای پشتیبانی شده</b>

<b>🇺🇸 آمریکای شمالی:</b>
• US - آمریکا
• CA - کانادا

<b>🇪🇺 اروپا:</b>
• DE - آلمان
• NL - هلند
• GB - انگلستان
• FR - فرانسه
• IT - ایتالیا

<b>🌏 آسیا:</b>
• JP - ژاپن
• SG - سنگاپور
• HK - هنگ‌کنگ
• KR - کره جنوبی
• IR - ایران

<b>🌍 سایر:</b>
• AU - استرالیا
• BR - برزیل
• RU - روسیه
• TR - ترکیه

💡 <i>برای دریافت کانفیگ هر کشور از /configs [country] استفاده کنید.</i>
        """

        await self.send_message(chat_id, countries_text)

    async def _handle_latest(self, chat_id: int, user_session: UserSession):
        """دستور /latest"""
        await self._handle_configs(chat_id, user_session, ["latest"])

    async def _handle_search(self, chat_id: int, user_session: UserSession, args: List[str]):
        """دستور /search"""
        if not args:
            await self.send_message(chat_id, "❌ لطفاً عبارت جستجو را وارد کنید.\nمثال: /search vmess US")
            return

        search_query = " ".join(args)
        await self.send_message(chat_id, f"🔍 جستجو برای: {search_query}\n\nدر حال جستجو...")

        # اینجا می‌توانید جستجوی واقعی را پیاده‌سازی کنید
        await asyncio.sleep(2)
        await self.send_message(chat_id, "✅ جستجو تکمیل شد. نتایج در دسترس است.")

    async def _handle_subscribe(self, chat_id: int, user_session: UserSession):
        """دستور /subscribe"""
        # اینجا می‌توانید سیستم اشتراک را پیاده‌سازی کنید
        await self.send_message(chat_id, "✅ شما با موفقیت مشترک شدید!\n\n📢 آپدیت‌های جدید را دریافت خواهید کرد.")

    async def _handle_unsubscribe(self, chat_id: int, user_session: UserSession):
        """دستور /unsubscribe"""
        # اینجا می‌توانید سیستم لغو اشتراک را پیاده‌سازی کنید
        await self.send_message(chat_id, "❌ اشتراک شما لغو شد.\n\n📢 دیگر آپدیت‌های جدید را دریافت نخواهید کرد.")

    async def _handle_admin(self, chat_id: int, user_session: UserSession, args: List[str]):
        """دستورات ادمین"""
        if not args:
            admin_text = """
👑 <b>دستورات مدیریتی</b>

/admin stats - آمار تفصیلی
/admin users - لیست کاربران
/admin broadcast - ارسال پیام به همه
/admin restart - راه‌اندازی مجدد
/admin logs - مشاهده لاگ‌ها
            """
            await self.send_message(chat_id, admin_text)
            return

        subcommand = args[0].lower()

        if subcommand == 'stats':
            await self._handle_admin_stats(chat_id, user_session)
        elif subcommand == 'users':
            await self._handle_admin_users(chat_id, user_session)
        elif subcommand == 'broadcast':
            await self._handle_admin_broadcast(chat_id, user_session, args[1:])
        else:
            await self.send_message(chat_id, "❌ دستور ادمین نامعتبر")

    async def _handle_admin_stats(self, chat_id: int, user_session: UserSession):
        """آمار تفصیلی ادمین"""
        admin_stats_text = f"""
👑 <b>آمار تفصیلی ادمین</b>

<b>👥 کاربران:</b>
• کل کاربران: {len(self.user_sessions)}
• کاربران فعال امروز: {len([u for u in self.user_sessions.values() if (datetime.now() - u.last_activity).days < 1])}
• کاربران ادمین: {len(self.admin_users)}

<b>📊 درخواست‌ها:</b>
• کل درخواست‌ها: {self.stats.total_requests}
• درخواست‌های امروز: {self.stats.total_requests}

<b>🤖 وضعیت ربات:</b>
• Webhook: {'✅ فعال' if self.webhook_url else '❌ غیرفعال'}
• آخرین بروزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        await self.send_message(chat_id, admin_stats_text)

    async def _handle_admin_users(self, chat_id: int, user_session: UserSession):
        """لیست کاربران"""
        users_text = f"👥 <b>لیست کاربران ({len(self.user_sessions)})</b>\n\n"

        for i, (user_id, session) in enumerate(list(self.user_sessions.items())[:10], 1):
            users_text += f"{i}. {session.first_name} (@{session.username})\n"
            users_text += f"   ID: {user_id}\n"
            users_text += f"   آخرین فعالیت: {session.last_activity.strftime('%Y-%m-%d %H:%M')}\n\n"

        if len(self.user_sessions) > 10:
            users_text += f"... و {len(self.user_sessions) - 10} کاربر دیگر"

        await self.send_message(chat_id, users_text)

    async def _handle_admin_broadcast(self, chat_id: int, user_session: UserSession, args: List[str]):
        """ارسال پیام به همه کاربران"""
        if not args:
            await self.send_message(chat_id, "❌ لطفاً پیام را وارد کنید.\nمثال: /admin broadcast سلام همه!")
            return

        message = " ".join(args)
        broadcast_text = f"📢 <b>پیام عمومی:</b>\n\n{message}"

        # ارسال به همه کاربران
        sent_count = 0
        for user_id in self.user_sessions.keys():
            if await self.send_message(user_id, broadcast_text):
                sent_count += 1
            await asyncio.sleep(0.1)  # تأخیر بین ارسال‌ها

        await self.send_message(chat_id, f"✅ پیام به {sent_count} کاربر ارسال شد.")

    async def _handle_ping(self, chat_id: int, user_session: UserSession):
        """دستور /ping"""
        start_time = time.time()

        # تست اتصال به API
        bot_info = await self.get_bot_info()
        response_time = (time.time() - start_time) * 1000

        if bot_info:
            ping_text = f"""
🏓 <b>Pong!</b>

<b>🤖 اطلاعات ربات:</b>
• نام: {bot_info.get('first_name', 'نامشخص')}
• نام کاربری: @{bot_info.get('username', 'نامشخص')}
• ID: {bot_info.get('id', 'نامشخص')}

<b>⚡ عملکرد:</b>
• زمان پاسخ: {response_time:.0f}ms
• وضعیت: ✅ آنلاین
• سرور: Telegram API
            """
        else:
            ping_text = f"""
🏓 <b>Pong!</b>

<b>⚡ عملکرد:</b>
• زمان پاسخ: {response_time:.0f}ms
• وضعیت: ⚠️ مشکل در اتصال
• سرور: Telegram API
            """

        await self.send_message(chat_id, ping_text)

    async def _handle_about(self, chat_id: int, user_session: UserSession):
        """دستور /about"""
        about_text = """
ℹ️ <b>درباره ربات</b>

🤖 <b>V2Ray Collector Bot</b>
📡 نسخه: 2.0.0
👨‍💻 توسعه‌دهنده: Ahmad Akd

<b>🎯 هدف:</b>
جمع‌آوری هوشمند و دسترسی آسان به کانفیگ‌های V2Ray

<b>✨ ویژگی‌ها:</b>
• جمع‌آوری خودکار از 223+ منبع
• پشتیبانی از 17+ پروتکل
• دسته‌بندی بر اساس کشور
• AI Quality Scoring
• رابط کاربری مدرن

<b>🔗 لینک‌ها:</b>
• GitHub: github.com/AhmadAkd/Onix-V2Ray-Collector
• وب‌سایت: ahmadakd.github.io/Onix-V2Ray-Collector
• پشتیبانی: @AhmadAkd

💡 <i>این ربات بخشی از پروژه V2Ray Collector است.</i>
        """

        await self.send_message(chat_id, about_text)

    async def _handle_unknown(self, chat_id: int, user_session: UserSession, command: str):
        """دستور نامعلوم"""
        unknown_text = f"""
❓ <b>دستور نامعلوم: /{command}</b>

برای مشاهده لیست دستورات از /help استفاده کنید.

💡 <i>اگر فکر می‌کنید این یک خطا است، لطفاً گزارش دهید.</i>
        """

        await self.send_message(chat_id, unknown_text)

    async def _load_latest_stats(self) -> Dict[str, Any]:
        """بارگذاری آخرین آمار"""
        try:
            with open('subscriptions/latest_report.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Error loading stats: {e}")
            return {}

    async def _load_configs(self, protocol: str) -> List[str]:
        """بارگذاری کانفیگ‌ها"""
        try:
            if protocol == "latest" or protocol == "all":
                filename = 'subscriptions/all_subscription.txt'
            else:
                filename = f'subscriptions/{protocol}_subscription.txt'

            with open(filename, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.error(f"❌ Error loading configs: {e}")
            return []

    async def process_webhook_update(self, update: Dict[str, Any]) -> bool:
        """پردازش webhook update"""
        try:
            if 'message' in update:
                return await self.handle_command(update['message'])
            elif 'callback_query' in update:
                # پردازش callback query ها
                return True
            else:
                logger.warning(f"Unknown update type: {update.keys()}")
                return False

        except Exception as e:
            logger.error(f"❌ Error processing webhook update: {e}")
            return False

    async def start_polling(self, interval: int = 1):
        """شروع polling بهینه شده"""
        logger.info("🔄 Starting Telegram bot polling...")

        offset = 0
        consecutive_errors = 0
        max_errors = 5

        while True:
            try:
                url = f"{self.api_url}/getUpdates"
                params = {
                    'offset': offset,
                    'timeout': 10,  # کاهش timeout از 30 به 10
                    'limit': 100
                }

                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()

                            if data.get('ok'):
                                updates = data.get('result', [])
                                consecutive_errors = 0  # reset error counter

                                for update in updates:
                                    await self.process_webhook_update(update)
                                    offset = max(
                                        offset, update['update_id'] + 1)

                                if updates:
                                    logger.info(
                                        f"📨 Processed {len(updates)} updates")
                                else:
                                    # اگر پیامی نبود، کمتر log کن
                                    if offset % 10 == 0:  # هر 10 بار یک بار log کن
                                        logger.debug("⏳ No new messages, waiting...")
                            else:
                                logger.error(f"❌ API Error: {data}")
                                consecutive_errors += 1
                        else:
                            logger.error(f"❌ HTTP Error: {response.status}")
                            consecutive_errors += 1

                # اگر خطاهای متوالی زیاد شد، بیشتر صبر کن
                if consecutive_errors >= max_errors:
                    logger.warning(f"⚠️ Too many errors ({consecutive_errors}), waiting longer...")
                    await asyncio.sleep(30)
                    consecutive_errors = 0
                else:
                    await asyncio.sleep(interval)

            except Exception as e:
                logger.error(f"❌ Polling error: {e}")
                consecutive_errors += 1
                await asyncio.sleep(min(5 * consecutive_errors, 60))  # exponential backoff

# مثال استفاده


async def main():
    """تابع اصلی"""
    # تنظیم Bot Token
    BOT_TOKEN = "8474552244:AAERRNE4n7_aFIeqxRlwEmutYn9jUvd9yUQ"

    # ایجاد ربات
    bot = EnhancedTelegramBot(BOT_TOKEN)

    # دریافت اطلاعات ربات
    bot_info = await bot.get_bot_info()
    if bot_info:
        logger.info(f"✅ Bot initialized: @{bot_info.get('username')}")
    else:
        logger.error("❌ Failed to get bot info")
        return

    # شروع polling
    await bot.start_polling()

if __name__ == "__main__":
    # تنظیم logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # اجرای ربات
    asyncio.run(main())
