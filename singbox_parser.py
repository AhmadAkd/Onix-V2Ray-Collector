#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SingBox JSON Config Parser
Parser for SingBox format JSON configurations
"""

import json
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SingBoxConfig:
    """SingBox configuration data class"""
    protocol: str
    address: str
    port: int
    config_string: str
    raw_data: Dict[str, Any]

class SingBoxParser:
    """Parser for SingBox JSON format configurations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def parse_singbox_json(self, json_content: str) -> List[str]:
        """
        Parse SingBox JSON format and convert to standard V2Ray URLs
        
        Args:
            json_content: JSON string content
            
        Returns:
            List of standard V2Ray configuration URLs
        """
        try:
            data = json.loads(json_content)
            configs = []
            
            # SingBox format has "outbounds" array
            if isinstance(data, dict) and 'outbounds' in data:
                outbounds = data['outbounds']
                
                for outbound in outbounds:
                    if not isinstance(outbound, dict):
                        continue
                    
                    config_url = self._convert_outbound_to_url(outbound)
                    if config_url:
                        configs.append(config_url)
            
            self.logger.info(f"✅ Parsed {len(configs)} configs from SingBox JSON")
            return configs
            
        except json.JSONDecodeError as e:
            self.logger.debug(f"Not a valid JSON: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error parsing SingBox JSON: {e}")
            return []
    
    def _convert_outbound_to_url(self, outbound: Dict[str, Any]) -> Optional[str]:
        """
        Convert SingBox outbound to standard V2Ray URL
        
        Args:
            outbound: SingBox outbound configuration
            
        Returns:
            Standard V2Ray URL or None
        """
        try:
            protocol = outbound.get('type', '').lower()
            tag = outbound.get('tag', 'Unknown')
            
            # Skip non-proxy outbounds
            if protocol in ['direct', 'block', 'dns']:
                return None
            
            # Extract server info
            server = outbound.get('server', '')
            server_port = outbound.get('server_port', 0)
            
            if not server or not server_port:
                return None
            
            # Convert based on protocol
            if protocol == 'shadowsocks':
                return self._convert_shadowsocks(outbound, server, server_port, tag)
            elif protocol == 'vmess':
                return self._convert_vmess(outbound, server, server_port, tag)
            elif protocol == 'vless':
                return self._convert_vless(outbound, server, server_port, tag)
            elif protocol == 'trojan':
                return self._convert_trojan(outbound, server, server_port, tag)
            elif protocol == 'hysteria2':
                return self._convert_hysteria2(outbound, server, server_port, tag)
            else:
                self.logger.debug(f"Unsupported protocol: {protocol}")
                return None
                
        except Exception as e:
            self.logger.debug(f"Error converting outbound: {e}")
            return None
    
    def _convert_shadowsocks(self, outbound: Dict, server: str, port: int, tag: str) -> Optional[str]:
        """Convert SingBox Shadowsocks to ss:// URL"""
        try:
            method = outbound.get('method', 'chacha20-ietf-poly1305')
            password = outbound.get('password', '')
            
            if not password:
                return None
            
            # Format: ss://BASE64(method:password)@server:port#tag
            import base64
            auth_str = f"{method}:{password}"
            encoded = base64.b64encode(auth_str.encode()).decode()
            
            return f"ss://{encoded}@{server}:{port}#{tag}"
            
        except Exception as e:
            self.logger.debug(f"Error converting Shadowsocks: {e}")
            return None
    
    def _convert_vmess(self, outbound: Dict, server: str, port: int, tag: str) -> Optional[str]:
        """Convert SingBox VMess to vmess:// URL"""
        try:
            uuid = outbound.get('uuid', '')
            if not uuid:
                return None
            
            alter_id = outbound.get('alter_id', 0)
            security = outbound.get('security', 'auto')
            
            # Get transport settings
            transport = outbound.get('transport', {})
            network = transport.get('type', 'tcp')
            
            # Build VMess JSON
            vmess_json = {
                'v': '2',
                'ps': tag,
                'add': server,
                'port': str(port),
                'id': uuid,
                'aid': str(alter_id),
                'scy': security,
                'net': network,
                'type': 'none',
                'host': '',
                'path': '',
                'tls': 'tls' if outbound.get('tls', {}).get('enabled', False) else ''
            }
            
            # Add transport-specific settings
            if network == 'ws':
                vmess_json['path'] = transport.get('path', '/')
                vmess_json['host'] = transport.get('headers', {}).get('Host', '')
            
            # Encode to base64
            import base64
            import json
            encoded = base64.b64encode(json.dumps(vmess_json).encode()).decode()
            
            return f"vmess://{encoded}"
            
        except Exception as e:
            self.logger.debug(f"Error converting VMess: {e}")
            return None
    
    def _convert_vless(self, outbound: Dict, server: str, port: int, tag: str) -> Optional[str]:
        """Convert SingBox VLESS to vless:// URL"""
        try:
            uuid = outbound.get('uuid', '')
            if not uuid:
                return None
            
            # Get transport settings
            transport = outbound.get('transport', {})
            network = transport.get('type', 'tcp')
            
            # Get TLS settings
            tls = outbound.get('tls', {})
            security = 'tls' if tls.get('enabled', False) else 'none'
            
            # Build VLESS URL
            url = f"vless://{uuid}@{server}:{port}?"
            params = [
                f"encryption=none",
                f"security={security}",
                f"type={network}"
            ]
            
            # Add transport-specific params
            if network == 'ws':
                path = transport.get('path', '/')
                host = transport.get('headers', {}).get('Host', server)
                params.append(f"path={path}")
                params.append(f"host={host}")
            
            url += '&'.join(params)
            url += f"#{tag}"
            
            return url
            
        except Exception as e:
            self.logger.debug(f"Error converting VLESS: {e}")
            return None
    
    def _convert_trojan(self, outbound: Dict, server: str, port: int, tag: str) -> Optional[str]:
        """Convert SingBox Trojan to trojan:// URL"""
        try:
            password = outbound.get('password', '')
            if not password:
                return None
            
            # Get TLS settings
            tls = outbound.get('tls', {})
            security = 'tls' if tls.get('enabled', False) else 'none'
            
            # Get transport settings
            transport = outbound.get('transport', {})
            network = transport.get('type', 'tcp')
            
            # Build Trojan URL
            url = f"trojan://{password}@{server}:{port}?"
            params = [
                f"security={security}",
                f"type={network}"
            ]
            
            url += '&'.join(params)
            url += f"#{tag}"
            
            return url
            
        except Exception as e:
            self.logger.debug(f"Error converting Trojan: {e}")
            return None
    
    def _convert_hysteria2(self, outbound: Dict, server: str, port: int, tag: str) -> Optional[str]:
        """Convert SingBox Hysteria2 to hysteria2:// URL"""
        try:
            password = outbound.get('password', '')
            if not password:
                return None
            
            # Build Hysteria2 URL
            url = f"hysteria2://{password}@{server}:{port}?"
            
            # Add optional parameters
            params = []
            if 'up_mbps' in outbound:
                params.append(f"upmbps={outbound['up_mbps']}")
            if 'down_mbps' in outbound:
                params.append(f"downmbps={outbound['down_mbps']}")
            
            if params:
                url += '&'.join(params)
            
            url += f"#{tag}"
            
            return url
            
        except Exception as e:
            self.logger.debug(f"Error converting Hysteria2: {e}")
            return None

# Test function
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test SingBox JSON parsing
    test_json = '''
    {
        "outbounds": [
            {
                "type": "shadowsocks",
                "tag": "Test SS",
                "server": "example.com",
                "server_port": 443,
                "method": "chacha20-ietf-poly1305",
                "password": "test123"
            },
            {
                "type": "vmess",
                "tag": "Test VMess",
                "server": "example.com",
                "server_port": 443,
                "uuid": "12345678-1234-1234-1234-123456789012",
                "alter_id": 0,
                "security": "auto"
            }
        ]
    }
    '''
    
    parser = SingBoxParser()
    configs = parser.parse_singbox_json(test_json)
    
    print(f"\n✅ Parsed {len(configs)} configs:")
    for config in configs:
        print(f"  - {config}")

