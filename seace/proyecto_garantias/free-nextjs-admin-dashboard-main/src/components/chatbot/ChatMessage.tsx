"use client";
import React from "react";

interface ChatMessageProps {
    message: string;
    isBot: boolean;
    timestamp: string;
    audioUrl?: string | null;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message, isBot, timestamp, audioUrl }) => {
    return (
        <div className={`flex ${isBot ? "justify-start" : "justify-end"} mb-4`}>
            <div className={`flex items-end gap-2 max-w-[80%] ${isBot ? "flex-row" : "flex-row-reverse"}`}>
                {/* Avatar */}
                <div className={`flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full ${isBot
                    ? "bg-gradient-to-br from-indigo-600 to-purple-600"
                    : "bg-gray-300 dark:bg-gray-700"
                    }`}>
                    {isBot ? (
                        <svg className="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                    ) : (
                        <svg className="h-5 w-5 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                    )}
                </div>

                {/* Message Bubble */}
                <div>
                    <div className={`rounded-2xl px-4 py-2.5 ${isBot
                        ? "bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-white"
                        : "bg-gradient-to-br from-indigo-600 to-purple-600 text-white"
                        }`}>
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">{message}</p>
                        {audioUrl && (
                            <div className="mt-2 pt-2 border-t border-gray-200/20">
                                <audio controls autoPlay src={audioUrl} className="h-8 w-full max-w-[200px]" />
                            </div>
                        )}
                    </div>
                    <p className="mt-1 px-2 text-xs text-gray-500 dark:text-gray-400">
                        {timestamp}
                    </p>
                </div>
            </div>
        </div>
    );
};
