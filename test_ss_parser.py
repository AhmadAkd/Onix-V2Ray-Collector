#!/usr/bin/env python3
"""
Test SS parser specifically
"""

import base64
from config_collector import V2RayCollector


def test_ss_parser():
    collector = V2RayCollector()

    # Test different SS formats
    test_configs = [
        'ss://YWVzLTI1Ni1nY206YWJjQDEuMS4xLjE6ODA4MA==#Test',
        'ss://YWVzLTI1Ni1nY206YWJjQDEuMS4xLjE6ODA4MA',
        'ss://cmM0LW1kNTpwYXNzd29yZA==@server.com:443#remarks',
        'ss://YWVzLTI1Ni1nY206YWJj@1.1.1.1:8080#Test',  # Wrong format
    ]

    print("🧪 Testing SS Parser:")

    for i, config_str in enumerate(test_configs, 1):
        print(f"\n{i}. Testing: {config_str}")

        try:
            # Manual parsing to debug
            if config_str.startswith('ss://'):
                encoded = config_str[5:]

                # Remove fragment if exists
                if '#' in encoded:
                    encoded = encoded.split('#')[0]

                print(f"   Encoded part: {encoded}")

                # Try to decode
                try:
                    # Add padding
                    padding = 4 - (len(encoded) % 4)
                    if padding != 4:
                        encoded += '=' * padding

                    decoded = base64.b64decode(encoded).decode('utf-8')
                    print(f"   Decoded: {decoded}")

                    if '@' in decoded:
                        method_password, address_port = decoded.split('@', 1)
                        print(f"   Method+Password: {method_password}")
                        print(f"   Address+Port: {address_port}")

                        if ':' in method_password and ':' in address_port:
                            method, password = method_password.split(':', 1)
                            address, port = address_port.rsplit(':', 1)
                            print(
                                f"   ✅ Method: {method}, Password: {password}")
                            print(f"   ✅ Address: {address}, Port: {port}")
                        else:
                            print(f"   ❌ Invalid format")
                    else:
                        print(f"   ❌ No @ separator")

                except Exception as e:
                    print(f"   ❌ Decode error: {e}")

            # Test with actual parser
            config = collector.parse_config(config_str)
            if config:
                print(
                    f"   ✅ Parser result: {config.protocol} - {config.address}:{config.port}")
            else:
                print(f"   ❌ Parser failed")

        except Exception as e:
            print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    test_ss_parser()
