"use client";
import React, { createContext, useContext, useState, useCallback, useRef } from 'react';

interface CacheEntry {
    data: any;
    timestamp: number;
    ttl: number;
}

interface DataCacheContextType {
    getCache: (key: string) => any | null;
    setCache: (key: string, data: any, ttl?: number) => void;
    invalidateCache: (key: string) => void;
    clearCache: () => void;
    prefetch: (key: string, fetcher: () => Promise<any>, ttl?: number) => Promise<void>;
}

const DataCacheContext = createContext<DataCacheContextType | undefined>(undefined);

const DEFAULT_TTL = 5 * 60 * 1000; // 5 minutes
const MAX_CACHE_SIZE = 50; // Maximum number of cache entries

export function DataCacheProvider({ children }: { children: React.ReactNode }) {
    const cacheRef = useRef<Map<string, CacheEntry>>(new Map());
    const [, forceUpdate] = useState({});

    const getCache = useCallback((key: string): any | null => {
        const entry = cacheRef.current.get(key);

        if (!entry) {
            return null;
        }

        // Check if cache is expired
        const now = Date.now();
        if (now - entry.timestamp > entry.ttl) {
            cacheRef.current.delete(key);
            return null;
        }

        return entry.data;
    }, []);

    const setCache = useCallback((key: string, data: any, ttl: number = DEFAULT_TTL) => {
        // Implement LRU eviction if cache is full
        if (cacheRef.current.size >= MAX_CACHE_SIZE) {
            const firstKey = cacheRef.current.keys().next().value;
            if (firstKey) {
                cacheRef.current.delete(firstKey);
            }
        }

        cacheRef.current.set(key, {
            data,
            timestamp: Date.now(),
            ttl,
        });

        forceUpdate({});
    }, []);

    const invalidateCache = useCallback((key: string) => {
        cacheRef.current.delete(key);
        forceUpdate({});
    }, []);

    const clearCache = useCallback(() => {
        cacheRef.current.clear();
        forceUpdate({});
    }, []);

    const prefetch = useCallback(async (
        key: string,
        fetcher: () => Promise<any>,
        ttl: number = DEFAULT_TTL
    ) => {
        // Don't prefetch if already cached and not expired
        const cached = getCache(key);
        if (cached !== null) {
            return;
        }

        try {
            const data = await fetcher();
            setCache(key, data, ttl);
        } catch (error) {
            console.error(`Error prefetching ${key}:`, error);
        }
    }, [getCache, setCache]);

    const value: DataCacheContextType = {
        getCache,
        setCache,
        invalidateCache,
        clearCache,
        prefetch,
    };

    return (
        <DataCacheContext.Provider value={value}>
            {children}
        </DataCacheContext.Provider>
    );
}

export function useDataCache() {
    const context = useContext(DataCacheContext);
    if (context === undefined) {
        throw new Error('useDataCache must be used within a DataCacheProvider');
    }
    return context;
}
