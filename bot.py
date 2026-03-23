import asyncio
import hashlib
from collections import defaultdict, deque

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import ollama as ollama_client
from config import TELEGRAM_BOT_TOKEN, MAX_HISTORY, OLLAMA_RAG_MODEL
from rag.retriever import retrieve, generate_answer
from vision.captioner import describe_image

user_history: dict[int, deque] = defaultdict(lambda: deque(maxlen=MAX_HISTORY))
query_cache: dict[str, dict] = {}


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Welcome! I'm a GenAI bot powered by local LLMs.\n\n"
        "Commands:\n"
        "/ask <query> - Ask a question (RAG-powered)\n"
        "/image - Send an image for captioning (send photo after this)\n"
        "/summarize - Summarize our recent interactions\n"
        "/help - Show this help message\n\n"
        "You can also just send a photo directly for captioning!"
    )
    await update.message.reply_text(text)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await help_command(update, context)


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text("Please provide a question. Usage: /ask <your question>")
        return

    cache_key = hashlib.md5(query.lower().encode()).hexdigest()
    if cache_key in query_cache:
        result = query_cache[cache_key]
        sources_str = ", ".join(result["sources"])
        await update.message.reply_text(
            f"{result['answer']}\n\n(Cached) Sources: {sources_str}"
        )
        return

    processing_msg = await update.message.reply_text("Thinking...")

    try:
        uid = update.effective_user.id
        history = list(user_history[uid])

        chunks = await asyncio.get_event_loop().run_in_executor(
            None, lambda: retrieve(query)
        )

        if not chunks:
            await processing_msg.edit_text("No knowledge base found. Please run ingest.py first.")
            return

        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: generate_answer(query, chunks, history)
        )

        query_cache[cache_key] = result

        user_history[uid].append({"query": query, "answer": result["answer"]})

        sources_str = ", ".join(result["sources"])
        await processing_msg.edit_text(
            f"{result['answer']}\n\nSources: {sources_str}"
        )
    except Exception as e:
        await processing_msg.edit_text(f"Error: {e}")


async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send me a photo and I'll describe it!")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    processing_msg = await update.message.reply_text("Analyzing image...")

    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        image_bytes = await file.download_as_bytearray()

        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: describe_image(bytes(image_bytes))
        )

        tags_str = ", ".join(result["tags"])
        response = f"Caption: {result['caption']}\n\nTags: {tags_str}"

        uid = update.effective_user.id
        user_history[uid].append({
            "query": "[Image uploaded]",
            "answer": response,
        })

        await processing_msg.edit_text(response)
    except Exception as e:
        await processing_msg.edit_text(f"Error analyzing image: {e}")


async def summarize_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    history = list(user_history[uid])

    if not history:
        await update.message.reply_text("No recent interactions to summarize.")
        return

    processing_msg = await update.message.reply_text("Summarizing...")

    try:
        conversation = "\n".join(
            f"User: {h['query']}\nBot: {h['answer']}" for h in history
        )

        messages = [
            {"role": "system", "content": "Summarize the following conversation concisely."},
            {"role": "user", "content": conversation},
        ]

        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: ollama_client.chat(model=OLLAMA_RAG_MODEL, messages=messages),
        )

        summary = response["message"]["content"]
        await processing_msg.edit_text(f"Summary:\n{summary}")
    except Exception as e:
        await processing_msg.edit_text(f"Error: {e}")


def main():
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set. Create a .env file with your token.")
        return

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(CommandHandler("image", image_command))
    app.add_handler(CommandHandler("summarize", summarize_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot is running! Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
