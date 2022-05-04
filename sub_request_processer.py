import sys
from commutator import find_and_send
import telepot
import urllib3


chat_id = int(sys.argv[1])
request = sys.argv[2]

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot('secret')

try:
    find_and_send(bot, chat_id, request)
except Exception as e:
    bot.sendMessage(chat_id, "Что-то пошло не так...")
    bot.sendMessage(chat_id, str(e))
