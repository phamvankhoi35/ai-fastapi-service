from loguru import logger
import os

logger.add(
    "chatbot.log",
    rotation="1 MB",
    level="INFO",
    format="{time} | {level} | {message}",
)

def log_chat(session_id, question, answer):
    logger.info(
        f"session={session_id}, Q={question}, A={answer}"
    )