# Ollama Insights Plan

## Goal

Enhance the existing Insights page by integrating Ollama to generate AI-powered financial recommendations from user transaction data.

## Requirements

- Add local Ollama integration.
- Use model: phi3:mini by default.
- Create analytics/ai_insights.py.
- Read recent transactions from database.
- Generate transaction summary.
- Send summary to Ollama.
- Display AI-generated financial insights.
- Add loading spinner while generating.
- Handle Ollama unavailable errors gracefully.
- Do not modify existing database schema.
- Do not modify transaction storage logic.

## User Flow

1. User opens Insights page.
2. User clicks "Generate AI Insights".
3. Transactions are summarized.
4. Summary is sent to Ollama.
5. AI recommendations are displayed.
