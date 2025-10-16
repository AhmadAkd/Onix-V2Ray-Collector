#!/usr/bin/env python3
"""
Auto Update UI - Automatically add new protocols and countries to index.html and dashboard.html
"""

import json
import os
import re
from typing import Dict, List, Set, Tuple
from datetime import datetime

class UIAutoUpdater:
    def __init__(self):
        self.subscriptions_dir = "subscriptions"
        self.index_file = os.path.join(self.subscriptions_dir, "index.html")
        self.dashboard_file = os.path.join(self.subscriptions_dir, "dashboard.html")
        self.report_file = os.path.join(self.subscriptions_dir, "latest_report.json")
        
        # Protocol info mapping
        self.protocol_info = {
            'vmess': {'name': 'VMess', 'color': '#4CAF50', 'icon': 'fas fa-shield-alt'},
            'vless': {'name': 'VLESS', 'color': '#2196F3', 'icon': 'fas fa-bolt'},
            'trojan': {'name': 'Trojan', 'color': '#FF9800', 'icon': 'fas fa-lock'},
            'ss': {'name': 'Shadowsocks', 'color': '#9C27B0', 'icon': 'fas fa-eye-slash'},
            'ssr': {'name': 'ShadowsocksR', 'color': '#6c5ce7', 'icon': 'fas fa-ghost'},
            'hysteria': {'name': 'Hysteria', 'color': '#e17055', 'icon': 'fas fa-rocket'},
            'tuic': {'name': 'TUIC', 'color': '#00BCD4', 'icon': 'fas fa-plane'},
            'wireguard': {'name': 'WireGuard', 'color': '#795548', 'icon': 'fas fa-network-wired'},
            'naive': {'name': 'Naive', 'color': '#607D8B', 'icon': 'fas fa-user-secret'},
            'reality': {'name': 'Reality', 'color': '#E91E63', 'icon': 'fas fa-magic'},
            'hysteria2': {'name': 'Hysteria2', 'color': '#FF5722', 'icon': 'fas fa-rocket'},
            'hysteria3': {'name': 'Hysteria3', 'color': '#3F51B5', 'icon': 'fas fa-rocket'}
        }
        
        # Country info mapping
        self.country_info = {
            'US': {'name': 'آمریکا', 'flag': '🇺🇸'},
            'DE': {'name': 'آلمان', 'flag': '🇩🇪'},
            'IR': {'name': 'ایران', 'flag': '🇮🇷'},
            'CA': {'name': 'کانادا', 'flag': '🇨🇦'},
            'NL': {'name': 'هلند', 'flag': '🇳🇱'},
            'TR': {'name': 'ترکیه', 'flag': '🇹🇷'},
            'GB': {'name': 'انگلستان', 'flag': '🇬🇧'},
            'FR': {'name': 'فرانسه', 'flag': '🇫🇷'},
            'JP': {'name': 'ژاپن', 'flag': '🇯🇵'},
            'SG': {'name': 'سنگاپور', 'flag': '🇸🇬'},
            'HK': {'name': 'هنگ‌کنگ', 'flag': '🇭🇰'},
            'AU': {'name': 'استرالیا', 'flag': '🇦🇺'},
            'RU': {'name': 'روسیه', 'flag': '🇷🇺'},
            'CN': {'name': 'چین', 'flag': '🇨🇳'},
            'IN': {'name': 'هند', 'flag': '🇮🇳'},
            'BR': {'name': 'برزیل', 'flag': '🇧🇷'},
            'IT': {'name': 'ایتالیا', 'flag': '🇮🇹'},
            'ES': {'name': 'اسپانیا', 'flag': '🇪🇸'},
            'PL': {'name': 'لهستان', 'flag': '🇵🇱'},
            'SE': {'name': 'سوئد', 'flag': '🇸🇪'},
            'FI': {'name': 'فنلاند', 'flag': '🇫🇮'},
            'LT': {'name': 'لیتوانی', 'flag': '🇱🇹'},
            'CH': {'name': 'سوئیس', 'flag': '🇨🇭'},
            'TW': {'name': 'تایوان', 'flag': '🇹🇼'},
            'KR': {'name': 'کره جنوبی', 'flag': '🇰🇷'},
            'UA': {'name': 'اوکراین', 'flag': '🇺🇦'},
            'EU': {'name': 'اروپا', 'flag': '🇪🇺'},
            'CF': {'name': 'Cloudflare', 'flag': '☁️'}
        }

    def load_report_data(self) -> Dict:
        """Load data from latest_report.json"""
        try:
            with open(self.report_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ فایل {self.report_file} یافت نشد")
            return {}
        except Exception as e:
            print(f"❌ خطا در بارگذاری گزارش: {e}")
            return {}

    def get_available_protocols(self) -> List[str]:
        """Get list of available protocols from report"""
        data = self.load_report_data()
        protocols = data.get('protocols', {})
        return list(protocols.keys())

    def get_available_countries(self) -> List[str]:
        """Get list of available countries from report"""
        data = self.load_report_data()
        countries = data.get('countries', {})
        return list(countries.keys())

    def update_protocol_info(self, new_protocols: List[str]) -> None:
        """Add new protocols to protocol_info if not exists"""
        for protocol in new_protocols:
            if protocol not in self.protocol_info:
                # Generate default info for new protocol
                self.protocol_info[protocol] = {
                    'name': protocol.upper(),
                    'color': '#999999',
                    'icon': 'fas fa-circle'
                }
                print(f"➕ پروتکل جدید اضافه شد: {protocol}")

    def update_country_info(self, new_countries: List[str]) -> None:
        """Add new countries to country_info if not exists"""
        for country in new_countries:
            if country not in self.country_info:
                # Generate default info for new country
                self.country_info[country] = {
                    'name': country,
                    'flag': '🌍'
                }
                print(f"➕ کشور جدید اضافه شد: {country}")

    def generate_protocol_buttons(self, protocols: List[str]) -> str:
        """Generate protocol cards HTML with copyable links"""
        cards = []
        for protocol in protocols:
            info = self.protocol_info.get(protocol, {})
            name = info.get('name', protocol.upper())
            color = info.get('color', '#999999')
            icon = info.get('icon', 'fas fa-circle')
            
            card = f'''
                <div class="protocol-card">
                    <div class="protocol-header">
                        <div class="protocol-icon" style="background: {color};">
                            <i class="{icon}" style="color: white;"></i>
                        </div>
                        <div class="protocol-info">
                            <h3>{name}</h3>
                            <p>کانفیگ‌های {name}</p>
                        </div>
                    </div>
                    <div class="url-box" id="url{protocol}">https://raw.githubusercontent.com/AhmadAkd/Onix-V2Ray-Collector/main/subscriptions/by_protocol/{protocol}.txt</div>
                    <button class="btn-copy" onclick="copyUrl('url{protocol}', this)">
                        <i class="fas fa-copy"></i>
                        <span>کپی لینک اشتراک</span>
                    </button>
                </div>'''
            cards.append(card)
        
        return '\n'.join(cards)

    def generate_country_buttons(self, countries: List[str]) -> str:
        """Generate country cards HTML with copyable links and flags"""
        cards = []
        for country in countries:
            info = self.country_info.get(country, {})
            name = info.get('name', country)
            flag = info.get('flag', '🌍')
            
            card = f'''
                <div class="country-card" data-country="{country}">
                    <div class="country-flag" style="font-size: 2rem; margin-bottom: 10px;">{flag}</div>
                    <h4>{name}</h4>
                    <div class="url-box" id="url{country}">https://raw.githubusercontent.com/AhmadAkd/Onix-V2Ray-Collector/main/subscriptions/by_country/{country}.txt</div>
                    <button class="btn-copy" onclick="copyUrl('url{country}', this)">
                        <i class="fas fa-copy"></i>
                        <span>کپی لینک اشتراک</span>
                    </button>
                </div>'''
            cards.append(card)
        
        return '\n'.join(cards)

    def update_index_html(self, protocols: List[str], countries: List[str]) -> None:
        """Update index.html with new protocols and countries"""
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update protocol buttons
            protocol_pattern = r'<!-- PROTOCOL_BUTTONS_START -->.*?<!-- PROTOCOL_BUTTONS_END -->'
            protocol_buttons = f'''<!-- PROTOCOL_BUTTONS_START -->
{self.generate_protocol_buttons(protocols)}
<!-- PROTOCOL_BUTTONS_END -->'''
            content = re.sub(protocol_pattern, protocol_buttons, content, flags=re.DOTALL)
            
            # Update country buttons
            country_pattern = r'<!-- COUNTRY_BUTTONS_START -->.*?<!-- COUNTRY_BUTTONS_END -->'
            country_buttons = f'''<!-- COUNTRY_BUTTONS_START -->
{self.generate_country_buttons(countries)}
<!-- COUNTRY_BUTTONS_END -->'''
            content = re.sub(country_pattern, country_buttons, content, flags=re.DOTALL)
            
            # Update JavaScript protocol info
            js_protocol_info = json.dumps(self.protocol_info, ensure_ascii=False, indent=2)
            protocol_js_pattern = r'const protocolInfo = \{.*?\};'
            protocol_js_replacement = f'const protocolInfo = {js_protocol_info};'
            content = re.sub(protocol_js_pattern, protocol_js_replacement, content, flags=re.DOTALL)
            
            # Update JavaScript country info
            js_country_info = json.dumps(self.country_info, ensure_ascii=False, indent=2)
            country_js_pattern = r'const countryInfo = \{.*?\};'
            country_js_replacement = f'const countryInfo = {js_country_info};'
            content = re.sub(country_js_pattern, country_js_replacement, content, flags=re.DOTALL)
            
            with open(self.index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {self.index_file} بروزرسانی شد")
            
        except Exception as e:
            print(f"❌ خطا در بروزرسانی {self.index_file}: {e}")

    def update_dashboard_html(self, protocols: List[str], countries: List[str]) -> None:
        """Update dashboard.html with new protocols and countries"""
        try:
            with open(self.dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update JavaScript protocol info
            js_protocol_info = json.dumps(self.protocol_info, ensure_ascii=False, indent=2)
            protocol_js_pattern = r'const protocolInfo = \{.*?\};'
            protocol_js_replacement = f'const protocolInfo = {js_protocol_info};'
            content = re.sub(protocol_js_pattern, protocol_js_replacement, content, flags=re.DOTALL)
            
            # Update JavaScript country info
            js_country_info = json.dumps(self.country_info, ensure_ascii=False, indent=2)
            country_js_pattern = r'const countryInfo = \{.*?\};'
            country_js_replacement = f'const countryInfo = {js_country_info};'
            content = re.sub(country_js_pattern, country_js_replacement, content, flags=re.DOTALL)
            
            with open(self.dashboard_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {self.dashboard_file} بروزرسانی شد")
            
        except Exception as e:
            print(f"❌ خطا در بروزرسانی {self.dashboard_file}: {e}")

    def run_auto_update(self) -> None:
        """Run the complete auto-update process"""
        print("🚀 شروع بروزرسانی خودکار UI...")
        
        # Load current data
        protocols = self.get_available_protocols()
        countries = self.get_available_countries()
        
        print(f"📊 پروتکل‌های موجود: {len(protocols)} - {protocols}")
        print(f"🌍 کشورهای موجود: {len(countries)} - {countries}")
        
        # Update info mappings
        self.update_protocol_info(protocols)
        self.update_country_info(countries)
        
        # Update HTML files
        self.update_index_html(protocols, countries)
        self.update_dashboard_html(protocols, countries)
        
        print("✅ بروزرسانی خودکار UI تکمیل شد!")

def main():
    updater = UIAutoUpdater()
    updater.run_auto_update()

if __name__ == "__main__":
    main()
