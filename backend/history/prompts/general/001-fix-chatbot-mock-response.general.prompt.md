---
id: 001
title: Fix Chatbot Mock Response Issue
stage: general
date_iso: 2026-01-16
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 008-chat-endpoint-ui
user: maryam
command: "Fix chatbot returning mock response"
labels: ["bug-fix", "chat", "ai-agent"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
---

## Prompt

Investigate why the chatbot always returns this message: "This is a mock response until the AI agent is properly configured."

## Response

Fixed the chatbot mock response issue by updating the agent implementation to work with Google Gemini API directly instead of relying on a non-existent agents package.

Root cause: The chat_runner.py file had a fallback to a MockRunner when the 'agents' package wasn't available. The import 'from agents import Runner' was failing because the agents package didn't exist, causing the system to always use the mock implementation.

Secondary issue: After fixing the main issue, there was a runtime error `'dict' object has no attribute 'role'` because the code was treating dictionary entries from get_conversation_history as objects with attributes.

Tertiary issue: After fixing the previous issues, there was an API error about the model 'gemini-1.5-flash' not being found for the generateContent API.

Quaternary issue: The initial fallback implementation wasn't comprehensive enough, leading to continued model availability errors.

Quinary issue: Switch to OpenRouter API for better reliability and model availability.

Solution:
1. Updated both openai_agent.py and chat_runner.py to work directly with google.generativeai, removing the dependency on the non-existent agents package and enabling proper AI functionality.
2. Fixed the dictionary access in chat_runner.py to use msg["role"] and msg["content"] instead of msg.role and msg.content.
3. Added comprehensive fallback model handling in openai_agent.py with multiple fallback options and dynamic model creation to gracefully handle unavailable models.
4. Updated the create_agent function to use dynamic model creation with fallback handling.
5. Switched from Google Gemini API to OpenRouter API using the provided API key, model, and base URL from the .env file.
6. Updated config.py to include OpenRouter settings alongside legacy Gemini settings.

## Files Modified

- backend/app/agents/openai_agent.py
- backend/app/agents/chat_runner.py
- backend/app/config.py
- backend/.env

## Outcome

Chatbot now connects to the OpenRouter API instead of returning the static mock message, enabling proper processing of natural language requests and tool execution. Fixed the runtime error that occurred when accessing conversation history, added model fallback handling, and switched to OpenRouter for better reliability and model availability.