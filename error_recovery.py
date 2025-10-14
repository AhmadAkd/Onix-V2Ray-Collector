#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Error Recovery System
سیستم بازیابی خطا و Retry Logic
"""

import asyncio
import logging
from typing import Optional, Callable, Any
from functools import wraps
import time
import json

logger = logging.getLogger(__name__)

class ErrorRecovery:
    """سیستم بازیابی خطا"""
    
    def __init__(self):
        self.backup_data = {}
        self.logger = logging.getLogger(__name__)
        
    def retry_with_backoff(self, max_retries: int = 3, initial_delay: float = 1.0):
        """Decorator برای retry با exponential backoff"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                last_exception = None
                delay = initial_delay
                
                for attempt in range(max_retries + 1):
                    try:
                        result = await func(*args, **kwargs)
                        if attempt > 0:
                            self.logger.info(f"✅ {func.__name__} succeeded on attempt {attempt + 1}")
                        return result
                    except Exception as e:
                        last_exception = e
                        
                        if attempt < max_retries:
                            self.logger.warning(f"⚠️ {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
                            self.logger.info(f"⏳ Retrying in {delay:.1f} seconds...")
                            await asyncio.sleep(delay)
                            delay *= 2  # Exponential backoff
                        else:
                            self.logger.error(f"❌ {func.__name__} failed after {max_retries + 1} attempts")
                
                raise last_exception
            return wrapper
        return decorator
    
    def with_fallback(self, fallback_func: Callable):
        """Decorator برای استفاده از fallback در صورت خطا"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"❌ {func.__name__} failed: {e}")
                    self.logger.info(f"🔄 Using fallback: {fallback_func.__name__}")
                    try:
                        return await fallback_func(*args, **kwargs)
                    except Exception as fallback_error:
                        self.logger.error(f"❌ Fallback also failed: {fallback_error}")
                        raise e
            return wrapper
        return decorator
    
    def save_backup(self, key: str, data: Any):
        """ذخیره backup از داده"""
        try:
            self.backup_data[key] = {'data': data, 'timestamp': time.time()}
            with open(f'backup_{key}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"💾 Backup saved for {key}")
        except Exception as e:
            self.logger.error(f"❌ Error saving backup: {e}")
    
    def load_backup(self, key: str) -> Optional[Any]:
        """بارگذاری backup"""
        try:
            if key in self.backup_data:
                backup = self.backup_data[key]
                if time.time() - backup['timestamp'] < 3600:
                    self.logger.info(f"📥 Loaded backup from memory")
                    return backup['data']
            
            with open(f'backup_{key}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.logger.info(f"📥 Loaded backup from file")
                return data
        except Exception as e:
            self.logger.debug(f"No backup available for {key}")
            return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Error Recovery module loaded successfully")

