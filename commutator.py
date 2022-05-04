from db_loader import load_tags
from searcher import find_tags, find
from latex_factory import build_pdf
from user_data_handler import get_role
import re
import time
import os


def find_and_send(bot, chat_id, request):
    req_arr = list(filter(None, re.split('\s*,\s*', request)))
    if len(req_arr) == 0:
        bot.sendMessage(chat_id, "Введите хотя бы один тег.", parse_mode= 'Markdown')
        return
    tags = []
    strings = []
    for req in req_arr:
        if req[0] == '"' and req[-1] == '"' and len(req) > 1:
            strings.append(req[1:-1])
        else:
            tags.append(req)
    # tags = list(filter(None, re.split('\s*,\s*', request)))
    # bot.sendMessage(chat_id, f"Ищу по тегам: `{'`, `'.join(tags)}`.", parse_mode= 'Markdown')
    text_to_send = f"Поиск по запросу: `{'`, `'.join(req_arr)}`."
    ret = bot.sendMessage(chat_id, text_to_send, parse_mode= 'Markdown')
    # msg_id = ret['message_id']
    # tags_db = load_tags()
    try:
        # fitting_problems = find_tags(tags, tags_db)
        fitting_problems = find(tags, strings, role=get_role(chat_id))
    except KeyError as e:
        # text_to_send += f"\nТег не найден: `{str(e)}`."
        # bot.editMessageText((chat_id, msg_id), text_to_send, parse_mode= 'Markdown')
        bot.sendMessage(chat_id, f"Тег не найден: `{str(e)}`.", parse_mode= 'Markdown')
        return
    if len(fitting_problems) == 0:
        # text_to_send += "\nЗадачи не найдены."
        # bot.editMessageText((chat_id, msg_id), text_to_send, parse_mode= 'Markdown')
        bot.sendMessage(chat_id, "Задачи не найдены.")
        return
    max_problems = 500
    if len(fitting_problems) > max_problems:
        # text_to_send += f"\nНайдено слишком много задач: {len(fitting_problems)}. Бутут скомпилированы только первые {max_problems}. Компиляция может занять до нескольких минут."
        # bot.editMessageText((chat_id, msg_id), text_to_send, parse_mode= 'Markdown')
        bot.sendMessage(chat_id, f"Найдено слишком много задач: {len(fitting_problems)}. Бутут скомпилированы только первые {max_problems}. Компиляция может занять до нескольких минут.", parse_mode= 'Markdown')
        fitting_problems = fitting_problems[:max_problems]
    else:
        n = len(fitting_problems)
        if n % 10 == 1 and n % 100 != 11:
            response = f'Найдена {n} задача. Компиляция может занять до нескольких минут.'
        elif n % 10 >= 2 and n % 10 <= 4:
            response = f'Найдены {n} задачи. Компиляция может занять до нескольких минут.'
        else:
            response = f'Найдено {n} задач. Компиляция может занять до нескольких минут.'
        # text_to_send += '\n' + response
        # bot.editMessageText((chat_id, msg_id), text_to_send, parse_mode= 'Markdown')
        bot.sendMessage(chat_id, response)
    filename = str(abs(hash(tuple(tags + [chat_id, time.time()]))))
    try:
        pdf_file, tex_file = build_pdf(fitting_problems, filename)
        bot.sendDocument(chat_id, pdf_file)
    except FileNotFoundError:
        # text_to_send += '\nОшибка компиляции.'
        # bot.editMessageText((chat_id, msg_id), text_to_send, parse_mode= 'Markdown')
        bot.sendMessage(chat_id, "Ошибка компиляции.", parse_mode= 'Markdown')
    extensions = ['tex', 'pdf', 'log', 'aux', 'out']
    for ext in extensions:
        try:
            os.remove(f'{filename}.{ext}')
        except Exception:
            pass


def process_request(request, mode='tags'):
    if mode == 'tags':
        # if ',' in request:
        #     tags = list(filter(None, re.split('\s*,\s*', request)))
        # else:
        #     tags = request.split()
        tags = list(filter(None, re.split('\s*,\s*', request)))
        tags_db = load_tags()
        fitting_problems = find_tags(tags, tags_db)
        if len(fitting_problems) == 0:
            return None
        fitting_problems = fitting_problems[:50]
        pdf_file, tex_file = build_pdf(fitting_problems)
        return pdf_file, tex_file
    elif mode == 'text':
        pass
    else:
        raise Exception('Invalid mode')


if __name__ == '__main__':
    # tags_db = load_tags()
    # print(find_tags(['кинематика', '8', 'физбой'], tags_db))
    # process_request('кинематика')
    tags_db = load_tags()
    tags = ['физбой']
    problems = find_tags(tags, tags_db)
    print(type(problems))
    print(problems)
    for book, problem in problems:
        print(f'\\libproblem{{{book}}}{{{problem}}}')
    # print(len(find_tags(tags, tags_db)))
