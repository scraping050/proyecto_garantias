"use client";
import React, { useState } from "react";
import { ChatbotButton } from "./ChatbotButton";
import { ChatbotWidget } from "./ChatbotWidget";

export const Chatbot: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    return (
        <>
            <ChatbotWidget isOpen={isOpen} />
            <ChatbotButton onClick={toggleChat} isOpen={isOpen} />
        </>
    );
};
