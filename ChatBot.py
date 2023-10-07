from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "J.A.R.V.I.S"

channel_secret = "894f78623e2144ca87f5c21f24f1ff35"
channel_access_token = "mW47Pxk8gpPt+MgwzNLVsGpGmjKJCUU+z/RTya9x2/W8V5u8AZGRG6w94k7+LQL34rr2UHKRH0v+lSnZmbJAwWobw7q8Dy+vO+i7Zxby3rKu8dFhPXckssb46+4AoIIEQFgyMMpYy/RbJjYa8+vOrgdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello JARVIS"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()
