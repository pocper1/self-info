#  import flask related
from flask import Flask, request, abort, url_for
from urllib.parse import parse_qsl, parse_qs
import random
from line_chatbot_api import *

# create flask server
app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print('receive msg')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


# handle msg
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user info & message
    user_id = event.source.user_id
    msg = event.message.text
    user_name = line_bot_api.get_profile(user_id).display_name

    # get msg details
    print('msg from [', user_name, '](', user_id, ') : ', msg)

    if event.message.text == "自我介紹":
        messages = []
        messages.append(StickerSendMessage(
            package_id=11538, sticker_id=51626494))
        messages.append(TextSendMessage(text=f'您好，{user_name}\n歡迎查看我的自我介紹，我是中央大學大三學生'))
        messages.append(LocationSendMessage(
            title="就讀學校", address="中央大學", longitude=121.1941836, latitude=24.9689728))

        messages.append(TextSendMessage(
            text=f'興趣是喜歡攝影，過去寫過一些程式專案\n可以點擊 "過去做過的專案"查看'))
        messages.append(StickerSendMessage(
            package_id=11537, sticker_id=52002768))

        line_bot_api.reply_message(
            event.reply_token,
            messages
        )
    elif event.message.text == "過去做過的專案":

        message = TemplateSendMessage(
            alt_text='過去做過的專案',
            template=ButtonsTemplate(
                # thumbnail_image_url=url_for('static', filename='images/brown_1024.jpg', _external=True),
                thumbnail_image_url='https://i.imgur.com/nyljaMX.png',
                title='過去做過的專案',
                text='想了解作者過去的專案',
                actions=[
                     PostbackAction(
                         label='系統分析與設計期末專案',
                         display_text='系統分析與設計期末專案',
                         data=f'action=show_project&item=系統分析與設計期末專案'
                     ),
                    PostbackAction(
                        label='編譯器專案',
                        display_text='編譯器專案',
                        data=f'action=show_project&item=編譯器專案'
                     ),
                    PostbackAction(
                        label='AI 人工智慧導論_Line Bot',
                        display_text='AI 人工智慧導論_Line Bot',
                        data=f'action=show_project&item=人工智慧導論_Line_Bot'
                     )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text == "其他資訊":
        image_carousel_template_message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/uWteCty.gif',
                        action=PostbackAction(
                            label='了解作者更多',
                            display_text='查看作者Github',
                            data='action=personalDetail&item=查看作者Github'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/hNl0nhz.png',
                        action=PostbackAction(
                            label='查看個人網站',
                            display_text='查看個人網站',
                            data='action=personalDetail&item=查看個人網站'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token, image_carousel_template_message)
    else:
        msg = "您的問題無法在此處理，請當面詢問本人，謝謝"

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=msg))


@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name
    postback_data = dict(parse_qsl(event.postback.data))

    sticker_list = [(1070, 17839), (6362, 11087920),
                    (11537, 52002734), (8525, 16581293)]
    if postback_data.get('action') == 'show_project':
        sticker_random = sticker_list[random.randint(0, len(sticker_list)-1)]
        messages = []
        messages.append(StickerSendMessage(
            package_id=sticker_random[0], sticker_id=sticker_random[1]))
        item = postback_data.get("item", "")
        if item == "系統分析與設計期末專案":
            messages.append(TextSendMessage(
                text=f'{user_name}, 好的沒問題, 這是{postback_data.get("item", "")}的連結:\n https://github.com/pocper1/system_design'))
        elif item == "編譯器專案":
            messages.append(TextSendMessage(
                text=f'{user_name}, 好的沒問題, 這是{postback_data.get("item", "")}的連結:\n https://github.com/pocper1/1101_Compiler'))
        elif item == "人工智慧導論_Line_Bot":
            messages.append(TextSendMessage(
                text=f'{user_name}, 好的沒問題, 這是{postback_data.get("item", "")}的連結:\n https://github.com/pocper1/AI_Project_Group6'))
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action') == 'personalDetail':
        messages = []
        item = postback_data.get("item", "")
        if item == "查看作者Github":
            messages.append(TextSendMessage(
                text=f'這是{postback_data.get("item", "")}的連結:\n https://github.com/pocper1'))
        elif item == "查看個人網站":
            messages.append(TextSendMessage(
                text=f'這是{postback_data.get("item", "")}的連結:\n https://pocper1.github.io/self-info/'))
        line_bot_api.reply_message(event.reply_token, messages)


# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5566)
