# from requests import session
#
# conversation_memory = {}
#
# def get_history(session_id: str):
#     return conversation_memory.get(session_id, [])
#
# def add_message(session_id: str, role: str, content: str):
#     if session_id not in conversation_memory:
#         conversation_memory[session_id] = []
#
#     conversation_memory[session_id].append(
#         {
#             "role": role,
#             "content": content
#         }
#     )

import os
import redis
import json

redis_url = os.getenv("REDIS_URL")
redis_client = redis.from_url(redis_url, decode_responses=True)

def get_history(session_id: str):
    data = redis_client.get(session_id)
    if not data:
        return []
    return json.loads(data)

def add_message(session_id: str, role: str, content: str):
    history = get_history(session_id)
    history.append({
        "role": role,
        "content": content
    })
    redis_client.set(session_id, json.dumps(history))
