from flask import Flask, request
import telepot
import urllib3
from request_handler import handle_command, handle_text
from user_data_handler import handle_chat_id


proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "secret"
bot = telepot.Bot('secret')
bot.setWebhook("https://physsummerdb.pythonanywhere.com/{}".format(secret), max_connections=1)

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    # f = open('log.txt', 'w')
    # f.write(str(update))
    # f.close()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        try:
            keys_to_extract = ["first_name", "last_name", "username"]
            new_user_data = {key: update["message"]["from"][key] for key in update["message"]["from"].keys() & keys_to_extract}
        except Exception:
            new_user_data = None
        user_state = handle_chat_id(chat_id, new_user_data)
        if "text" in update["message"]:
            text = update["message"]["text"]

            if text[0] == '/':
                handle_command(bot, chat_id, text)
            else:
                handle_text(bot, chat_id, text)
        else:
            bot.sendMessage(chat_id, "Введите текстовое сообщение.")
    return "OK"
