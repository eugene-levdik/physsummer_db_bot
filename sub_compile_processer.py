import sys
import telepot
import urllib3
import time
from latex_factory import build_pdf
import os
from user_data_handler import change_state


chat_id = int(sys.argv[1])
request = sys.argv[2]

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot('secret')

succeeded = False

try:
    request = request.split('\n')
    header = request[0].split('/')
    problem_strs = request[1:]
    problems = []
    for problem_str in problem_strs:
        book_name, problem_name = problem_str.split('/')
        problems.append((book_name, problem_name))

    filename = str(abs(hash((time.time(), chat_id))))

    bot.sendMessage(chat_id, "Начинаю компиляцию. Это может занять до нескольких минут.")
    try:
        pdf_file, tex_file = build_pdf(problems, filename, teachermode=False, tagsmode=False, setphysstyle=header)
        pdf_teachersmode, tex_teachersmode = build_pdf(problems, 'teacher_' + filename, teachermode=True, tagsmode=True, setphysstyle=header)
        bot.sendDocument(chat_id, pdf_file)
        bot.sendDocument(chat_id, pdf_teachersmode)
        succeeded = True
    except FileNotFoundError:
        bot.sendMessage(chat_id, "Ошибка компиляции.", parse_mode= 'Markdown')
except Exception as e:
    bot.sendMessage(chat_id, "Что-то пошло не так...")
    bot.sendMessage(chat_id, str(e))

extensions = ['tex', 'pdf', 'log', 'aux', 'out']
for ext in extensions:
    try:
        os.remove(f'{filename}.{ext}')
        os.remove(f'teacher_{filename}.{ext}')
    except Exception:
        pass

if succeeded:
    change_state(chat_id, 'default')
else:
    bot.sendMessage(chat_id, "Введите верхний колонтитул и список задач на отдельных строках. Для отмены введите /cancel.\n\n*Пример запроса:*\n`ЛФШ-2021/11 класс/Конденсаторы\n1001/12.47\n1001/13.59\ngoldfarb/17.5`", parse_mode= 'Markdown')
