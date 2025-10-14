#!/usr/bin/env python3
"""
Debug script to check why some protocols have fewer configs
"""

import asyncio
import json
from config_collector import V2RayCollector
from collections import defaultdict


async def debug_protocols():
    print("🔍 بررسی پروتکل‌ها و منابع...")

    collector = V2RayCollector()

    # Test parsing for each protocol
    test_configs = {
        'vmess': 'vmess://eyJ2IjoiMiIsInBzIjoiVGVzdCIsImFkZCI6IjEuMS4xLjEiLCJwb3J0IjoiODA4MCIsImlkIjoiYWJjZCIsImFpZCI6IjAiLCJuZXQiOiJ0Y3AiLCJ0eXBlIjoibm9uZSIsImhvc3QiOiIiLCJwYXRoIjoiIiwidGxzIjoiIn0=',
        'vless': 'vless://abc@1.1.1.1:8080?security=tls&type=tcp#Test',
        'trojan': 'trojan://abc@1.1.1.1:8080?type=tcp#Test',
        'ss': 'ss://YWVzLTI1Ni1nY206YWJj@1.1.1.1:8080#Test',
        'ssr': 'ssr://MTExLjExMS4xMTEuMTExOjgwODA6YXV0aF9hZXMxMjhfbWQ1OmFlcy0yNTYtY2ZiOnRsczEuMl90aWNrZXRfYXV0aDpabVZqTURCek1UYz0vP29iZnNwYXJhbT0mcmVtYXJrcz1VMEZVVkZSUElFRnVaMlY2TVE9PSZ1ZGJwYXJhbT0mZ3JvdXA9',
        'hysteria': 'hysteria://1.1.1.1:8080?protocol=udp&auth=abc&peer=example.com&insecure=0&upmbps=100&downmbps=100&alpn=h3#Test',
        'wireguard': 'wireguard://abc@1.1.1.1:8080?public_key=abc&private_key=def#Test',
        'tuic': 'tuic://abc@1.1.1.1:8080?congestion_control=bbr&udp_relay_mode=native&alpn=h3#Test',
        'naive': 'naive://abc@1.1.1.1:8080?extraHeaders=User-Agent%3ANaiveProxy#Test'
    }

    print("\n📋 تست Parsing برای هر پروتکل:")
    parsed_counts = defaultdict(int)

    for protocol, config_str in test_configs.items():
        try:
            config = collector.parse_config(config_str)
            if config:
                print(f"✅ {protocol}: OK - {config.protocol}")
                parsed_counts[protocol] = 1
            else:
                print(f"❌ {protocol}: Failed to parse")
                parsed_counts[protocol] = 0
        except Exception as e:
            print(f"❌ {protocol}: Error - {e}")
            parsed_counts[protocol] = 0

    print(f"\n📊 نتایج Parsing: {dict(parsed_counts)}")

    # Test actual sources
    print("\n🌐 تست منابع واقعی:")
    source_protocols = defaultdict(int)

    # Test first 10 sources
    test_sources = collector.config_sources[:10]

    for source_url in test_sources:
        try:
            print(f"\n🔗 Testing: {source_url}")
            configs = await collector.fetch_configs_from_source(source_url)
            print(f"   📥 Received: {len(configs)} configs")

            # Parse and count protocols
            protocol_counts = defaultdict(int)
            for config_str in configs[:50]:  # Test first 50
                try:
                    config = collector.parse_config(config_str)
                    if config:
                        protocol_counts[config.protocol] += 1
                except:
                    pass

            print(f"   📊 Protocols found: {dict(protocol_counts)}")

            # Update totals
            for protocol, count in protocol_counts.items():
                source_protocols[protocol] += count

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print(f"\n📈 Total protocols from sources: {dict(source_protocols)}")

    # Check current subscription files
    print("\n📁 بررسی فایل‌های subscription موجود:")
    import os
    subscription_dir = "subscriptions"

    if os.path.exists(subscription_dir):
        files = os.listdir(subscription_dir)
        protocol_files = [f for f in files if f.endswith('_subscription.txt')]

        for file in protocol_files:
            file_path = os.path.join(subscription_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    config_count = len(
                        [line for line in content.split('\n') if line.strip()])
                    print(f"   📄 {file}: {config_count} configs")
            except Exception as e:
                print(f"   ❌ {file}: Error reading - {e}")
    else:
        print("   ❌ subscriptions directory not found")

    # Check by_protocol directory
    by_protocol_dir = os.path.join(subscription_dir, "by_protocol")
    if os.path.exists(by_protocol_dir):
        print(f"\n📂 Files in by_protocol:")
        files = os.listdir(by_protocol_dir)
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(by_protocol_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        config_count = len(
                            [line for line in content.split('\n') if line.strip()])
                        print(f"   📄 {file}: {config_count} configs")
                except Exception as e:
                    print(f"   ❌ {file}: Error reading - {e}")
    else:
        print(f"   ❌ {by_protocol_dir} not found")

if __name__ == "__main__":
    asyncio.run(debug_protocols())
