import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from telegram.ext import Application
from pydantic import BaseModel

from bot.services import JokeService, AnimeQuotes, MessageStorage

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

class MessageRequest(BaseModel):
    user_id: str
    message: str

app = FastAPI()

bot_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# эндпоинты
@app.post("/send_message")
async def send_telegram_message(request: MessageRequest):
    try:
        await bot_app.bot.send_message(
            chat_id=request.user_id, 
            text=request.message
        )
        MessageStorage.send_message(request.user_id, request.message)
        return {"status": "success", "message": "Сообщение отправлено"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_total_count_msg")
async def get_message_count(request: Request):
    try:
        data = await request.json()
    except:
        data = {}
    user_id = data.get('user_id')
    
    if not user_id:
        raise HTTPException(status_code=400, detail="Требуется ID пользователя")
    
    count = MessageStorage.get_message_count(user_id)
    return {"user_id": user_id, "message_count": count}

@app.post("/send_joke")
async def send_random_joke(request: Request):
    try:
        data = await request.json()
    except:
        data = {}
    user_id = data.get('user_id')
    
    if not user_id:
        raise HTTPException(status_code=400, detail="Требуется ID пользователя")
    
    try:
        joke = JokeService.get_random_joke()
        joke_message = f"{joke['setup']}\n\n{joke['punchline']}"
        await bot_app.bot.send_message(chat_id=user_id, text=joke_message)
        
        MessageStorage.send_message(user_id, joke_message)
        return {"status": "success", "joke": joke_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post('/send_anime_quote')
async def send_anime_quote(request: Request):
    try:
        data = await request.json()
    except:
        data = {}
    user_id = data.get('user_id')

    if not user_id:
        raise HTTPException(status_code=400, detail="Требуется ID пользователя")
    
    try:
        quote = AnimeQuotes.get_anime_quotes()
        quote_message = f"Anime: {quote['anime']}\nCharacter: {quote['character']}\nQuote: {quote['quote']}"
        await bot_app.bot.send_message(chat_id=user_id, text=quote_message)

        MessageStorage.send_message(user_id, quote_message)
        return {"status": "success", "joke": quote_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)