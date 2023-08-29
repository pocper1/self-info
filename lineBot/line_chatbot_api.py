# import flask related
import os
import requests
import json


# import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage,
    VideoSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    PostbackEvent, ConfirmTemplate, CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn, FlexSendMessage
)
import json

line_bot_api = LineBotApi('AEuJL3NWEoNGINCR5z1EqigN7gZZoV4lWFASZaHldj0oVR10kjA/lhg1VFY5G3pNUKvopznBoMLYFkKO8Td2PyGAwQgRuhkRH7fjphGE9SvcSOlq8emdOg1wiJ1nQlf/64oObOTlE5hPePT+HRNO1AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('def68c93c241242e10504a9de7e9c6ed')