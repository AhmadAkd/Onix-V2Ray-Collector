#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cache Manager for V2Ray Collector
مدیریت کش برای V2Ray Collector
"""

import json
import time
import hashlib
import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """ورودی کش"""
    data: Any
    timestamp: float
    ttl: int = 3600  # Time to live in seconds (default: 1 hour)
    hit_count: int = 0
    last_accessed: float = 0

class CacheManager:
    """مدیریت کش هوشمند"""
    
    def __init__(self, cache_dir: str = "cache", max_size: int = 1000):
        self.cache_dir = cache_dir
        self.max_size = max_size
        self.memory_cache: Dict[str, CacheEntry] = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size': 0
        }
        
        # ایجاد دایرکتوری کش
        os.makedirs(cache_dir, exist_ok=True)
        
        # بارگذاری کش از فایل
        self._load_cache_from_disk()
        
        logger.info(f"Cache Manager initialized with {len(self.memory_cache)} entries")
    
    def _generate_key(self, data: str) -> str:
        """تولید کلید یکتا برای داده"""
        return hashlib.md5(data.encode('utf-8')).hexdigest()
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """بررسی انقضای ورودی کش"""
        return time.time() - entry.timestamp > entry.ttl
    
    def _cleanup_expired(self):
        """پاک‌سازی ورودی‌های منقضی شده"""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.memory_cache.items():
            if current_time - entry.timestamp > entry.ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.memory_cache[key]
            self.cache_stats['evictions'] += 1
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def _evict_lru(self):
        """حذف کم‌ترین استفاده شده (LRU)"""
        if len(self.memory_cache) >= self.max_size:
            # پیدا کردن کم‌ترین استفاده شده
            lru_key = min(
                self.memory_cache.keys(),
                key=lambda k: self.memory_cache[k].last_accessed
            )
            del self.memory_cache[lru_key]
            self.cache_stats['evictions'] += 1
            logger.debug(f"Evicted LRU cache entry: {lru_key}")
    
    def get(self, key: str) -> Optional[Any]:
        """دریافت داده از کش"""
        cache_key = self._generate_key(key)
        
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            
            if not self._is_expired(entry):
                # به‌روزرسانی آمار
                entry.hit_count += 1
                entry.last_accessed = time.time()
                self.cache_stats['hits'] += 1
                
                logger.debug(f"Cache hit for key: {key[:20]}...")
                return entry.data
            else:
                # حذف ورودی منقضی شده
                del self.memory_cache[cache_key]
                self.cache_stats['evictions'] += 1
        
        self.cache_stats['misses'] += 1
        logger.debug(f"Cache miss for key: {key[:20]}...")
        return None
    
    def set(self, key: str, data: Any, ttl: int = 3600) -> None:
        """ذخیره داده در کش"""
        cache_key = self._generate_key(key)
        current_time = time.time()
        
        # پاک‌سازی منقضی شده‌ها
        self._cleanup_expired()
        
        # بررسی اندازه کش
        if len(self.memory_cache) >= self.max_size:
            self._evict_lru()
        
        # ایجاد ورودی جدید
        entry = CacheEntry(
            data=data,
            timestamp=current_time,
            ttl=ttl,
            last_accessed=current_time
        )
        
        self.memory_cache[cache_key] = entry
        self.cache_stats['size'] = len(self.memory_cache)
        
        logger.debug(f"Cached data for key: {key[:20]}... (TTL: {ttl}s)")
    
    def invalidate(self, key: str) -> bool:
        """حذف داده از کش"""
        cache_key = self._generate_key(key)
        
        if cache_key in self.memory_cache:
            del self.memory_cache[cache_key]
            self.cache_stats['size'] = len(self.memory_cache)
            logger.debug(f"Invalidated cache for key: {key[:20]}...")
            return True
        
        return False
    
    def clear(self) -> None:
        """پاک‌سازی تمام کش"""
        self.memory_cache.clear()
        self.cache_stats['size'] = 0
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """دریافت آمار کش"""
        hit_rate = 0
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        if total_requests > 0:
            hit_rate = (self.cache_stats['hits'] / total_requests) * 100
        
        return {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'hit_rate': f"{hit_rate:.2f}%",
            'evictions': self.cache_stats['evictions'],
            'size': self.cache_stats['size'],
            'max_size': self.max_size,
            'memory_usage_mb': self._calculate_memory_usage()
        }
    
    def _calculate_memory_usage(self) -> float:
        """محاسبه استفاده از حافظه"""
        try:
            import sys
            total_size = 0
            for entry in self.memory_cache.values():
                total_size += sys.getsizeof(entry.data)
                total_size += sys.getsizeof(entry)
            return round(total_size / 1024 / 1024, 2)
        except:
            return 0.0
    
    def _load_cache_from_disk(self):
        """بارگذاری کش از دیسک"""
        cache_file = os.path.join(self.cache_dir, "cache.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                current_time = time.time()
                loaded_count = 0
                
                for key, entry_data in data.items():
                    entry = CacheEntry(**entry_data)
                    
                    # بررسی انقضا
                    if not self._is_expired(entry):
                        self.memory_cache[key] = entry
                        loaded_count += 1
                
                logger.info(f"Loaded {loaded_count} valid cache entries from disk")
                
            except Exception as e:
                logger.error(f"Error loading cache from disk: {e}")
    
    def save_cache_to_disk(self):
        """ذخیره کش روی دیسک"""
        cache_file = os.path.join(self.cache_dir, "cache.json")
        
        try:
            # تبدیل به فرمت قابل ذخیره
            cache_data = {}
            for key, entry in self.memory_cache.items():
                cache_data[key] = asdict(entry)
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(cache_data)} cache entries to disk")
            
        except Exception as e:
            logger.error(f"Error saving cache to disk: {e}")
    
    def get_or_set(self, key: str, factory_func, ttl: int = 3600) -> Any:
        """دریافت از کش یا تولید و ذخیره"""
        cached_data = self.get(key)
        
        if cached_data is not None:
            return cached_data
        
        # تولید داده جدید
        try:
            new_data = factory_func()
            self.set(key, new_data, ttl)
            return new_data
        except Exception as e:
            logger.error(f"Error in factory function for key {key}: {e}")
            return None

# نمونه استفاده
if __name__ == "__main__":
    # تنظیم لاگ
    logging.basicConfig(level=logging.INFO)
    
    # ایجاد cache manager
    cache = CacheManager()
    
    # تست عملکرد
    def expensive_operation():
        time.sleep(1)  # شبیه‌سازی عملیات زمان‌بر
        return {"result": "expensive_data", "timestamp": time.time()}
    
    # تست کش
    start_time = time.time()
    result1 = cache.get_or_set("test_key", expensive_operation)
    print(f"First call took: {time.time() - start_time:.2f}s")
    
    start_time = time.time()
    result2 = cache.get_or_set("test_key", expensive_operation)
    print(f"Second call took: {time.time() - start_time:.2f}s")
    
    # نمایش آمار
    stats = cache.get_stats()
    print(f"Cache stats: {stats}")
