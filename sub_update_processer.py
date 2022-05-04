import sys
import telepot
import urllib3
from db_loader import generate_db
import subprocess


chat_id = int(sys.argv[1])

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot('secret')


bash_command = ['git', '-C', 'materials', 'pull']
p = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

output, error = p.communicate()
if p.returncode != 0:
   bot.sendMessage(chat_id, "Что-то пошло не так...")
   exit()
if output == b'Already up to date.\n':
    bot.sendMessage(chat_id, "База задач актуальна. Обновление не требуется.")
    exit()

bot.sendMessage(chat_id, "Новые задачи скачаны. Обновляю базу тегов.")

try:
    generate_db()
except Exception:
    bot.sendMessage(chat_id, "Что-то пошло не так...")
    exit()

bot.sendMessage(chat_id, "База задач успешно обновлена.")
