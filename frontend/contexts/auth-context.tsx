'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '@/lib/api';

interface User {
    id: number;
    id_corporativo: string;
    nombre: string;
    email: string;
    perfil: string;
    job_title?: string;
    avatar_url?: string;
    activo: boolean;
}

interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (id_corporativo: string, password: string) => Promise<void>;
    logout: () => void;
    isAuthenticated: boolean;
    isAdmin: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);

    useEffect(() => {
        // Load user from localStorage on mount
        const storedToken = localStorage.getItem('access_token');
        const storedUser = localStorage.getItem('user');

        if (storedToken && storedUser) {
            setToken(storedToken);
            setUser(JSON.parse(storedUser));
        }
    }, []);

    // Helper to set cookie for cross-port sharing (localhost)
    const setCookie = (name: string, value: string, days: number) => {
        if (typeof document === 'undefined') return;
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (encodeURIComponent(value) || "") + expires + "; path=/";
    };

    const deleteCookie = (name: string) => {
        if (typeof document === 'undefined') return;
        document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    };

    const login = async (id_corporativo: string, password: string) => {
        // The backend expects 'id_corporativo' but the previous code might have used 'username' variable name in the component call
        // We'll keep the param name as id_corporativo to be explicit, but the request body needs to match what the backend expects.
        // Looking at backend main.py -> app.include_router(auth.router) -> auth.py:
        // class UserLogin(BaseModel): id_corporativo: str, password: str
        const response = await api.post('/api/auth/login', { id_corporativo, password });
        const { access_token, user: userData } = response.data;

        setToken(access_token);
        setUser(userData);

        localStorage.setItem('access_token', access_token);
        localStorage.setItem('user', JSON.stringify(userData));

        // Save to cookie for SEACE app (port 3001)
        setCookie('mqs_user_data', JSON.stringify(userData), 1); // 1 day
    };

    const logout = () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        deleteCookie('mqs_user_data');
    };

    const value = {
        user,
        token,
        login,
        logout,
        isAuthenticated: !!token,
        isAdmin: user?.perfil === 'DIRECTOR' || user?.perfil === 'ADMIN', // Adjusted based on likely roles, 'DIRECTOR' seems to be the high privilege one from auth_schemas
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
