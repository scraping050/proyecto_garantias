"use client";
import { useState, useEffect, useCallback } from 'react';
import { useDataCache } from '@/context/DataCacheContext';

interface UseCachedFetchOptions {
    ttl?: number;
    enabled?: boolean;
    staleWhileRevalidate?: boolean;
}

interface UseCachedFetchResult<T> {
    data: T | null;
    loading: boolean;
    error: Error | null;
    refetch: () => Promise<void>;
}

export function useCachedFetch<T>(
    key: string,
    fetcher: () => Promise<T>,
    options: UseCachedFetchOptions = {}
): UseCachedFetchResult<T> {
    const {
        ttl = 5 * 60 * 1000, // 5 minutes default
        enabled = true,
        staleWhileRevalidate = true,
    } = options;

    const { getCache, setCache } = useDataCache();
    const [data, setData] = useState<T | null>(() => getCache(key));
    const [loading, setLoading] = useState<boolean>(!data && enabled);
    const [error, setError] = useState<Error | null>(null);

    const fetchData = useCallback(async (showLoading = true) => {
        if (!enabled) return;

        try {
            if (showLoading) {
                setLoading(true);
            }
            setError(null);

            const result = await fetcher();

            setData(result);
            setCache(key, result, ttl);
        } catch (err) {
            const error = err instanceof Error ? err : new Error('Unknown error');
            setError(error);
            console.error(`Error fetching ${key}:`, error);
        } finally {
            if (showLoading) {
                setLoading(false);
            }
        }
    }, [key, fetcher, enabled, setCache, ttl]);

    useEffect(() => {
        if (!enabled) return;

        // Check cache first
        const cachedData = getCache(key);

        if (cachedData !== null) {
            setData(cachedData);
            setLoading(false);

            // Stale-while-revalidate: show cached data immediately, revalidate in background
            if (staleWhileRevalidate) {
                fetchData(false); // Revalidate without showing loading
            }
        } else {
            // No cache, fetch fresh data
            fetchData(true);
        }
    }, [key, enabled]); // Intentionally omit fetchData to avoid infinite loops

    const refetch = useCallback(async () => {
        await fetchData(true);
    }, [fetchData]);

    return { data, loading, error, refetch };
}
