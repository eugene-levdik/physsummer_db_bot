from db_loader import load_tags
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import subprocess
from user_data_handler import get_state, change_state, get_role, change_role


def handle_command(bot, chat_id, text):
    text = text.lower()
    command = text.split()[0][1:]
    user_state = get_state(chat_id)

    # команды, доступные в любом режиме, кроме 'default'
    if user_state != 'default':
        if command == 'cancel':
            change_state(chat_id, 'default')
            bot.sendMessage(chat_id, f"Действие {user_state} отменено.")
            return
        # else:
        #     bot.sendMessage(chat_id, "Команда недоступна. Для возврата в обычный режим введите /cancel.")
        #     return

    change_state(chat_id, 'default')
    # команды, доступные в режиме 'default'
    if command == 'start' or command == 'help':
        bot.sendMessage(chat_id, "Этот бот предназначен для поиска по базе задач «Летней Физической Школы». Вводите теги через запятую. Для поиска по тексту введите его в кавычках.\n\n*Примеры запросов:*\n`Архимед, город, 7`\n`кинематика, \"вертикально вверх\"`\n\n*Список команд:*\n/help — информация о боте\n/taglist — список тегов\n/update — обновить базу задач\n/compile — скомпилировать подборку задач", parse_mode= 'Markdown')
    elif command == 'taglist':
        tags = list(load_tags(role=get_role(chat_id)).keys())
        tags.sort()
        bot.sendMessage(chat_id, f"*Список тегов:*\n{', '.join(tags)}.", parse_mode= 'Markdown')
    elif command == 'update':
        subprocess.Popen(['python', 'sub_update_processer.py', str(chat_id)])
    elif command == 'compile':
        bot.sendMessage(chat_id, "Введите верхний колонтитул и список задач на отдельных строках. Для отмены введите /cancel.\n\n*Пример запроса:*\n`ЛФШ-2021/11 класс/Конденсаторы\n1001/12.47\n1001/13.59\ngoldfarb/17.5`", parse_mode= 'Markdown')
        change_state(chat_id, 'compile')
    # elif command == 'edittest':
    #     ret = bot.sendMessage(chat_id, "Тестовое сообщение.")
    #     import time
    #     time.sleep(3)
    #     msg_id = ret['message_id']
    #     msg_text = ret['text']
    #     bot.editMessageText((chat_id, msg_id), msg_text + '\nИзменено через 3 секунды')
    #     # bot.sendMessage(chat_id, f"{str(ret)}")
    # elif command == 'btest':
    #     keyboard = InlineKeyboardMarkup(inline_keyboard=[
    #               [InlineKeyboardButton(text='Press me', callback_data='press123')],
    #           ])

    #     bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)
    elif command == 'getid':
        bot.sendMessage(chat_id, f'Ваш ID: {str(chat_id)}')
    # elif command == 'sub':
    #     import subprocess
    #     subprocess.Popen(['python', 'hello_world.py', str(chat_id), 'some text arg'])
    #     bot.sendMessage(chat_id, 'sub ended')
    elif command == 'op':
        role = get_role(chat_id)
        if role == 'admin':
            change_state(chat_id, 'op')
            bot.sendMessage(chat_id, 'Введите ID пользователя, которому хотите предоставить доступ к приватным задачам.')
        else:
            bot.sendMessage(chat_id, 'У вас нет доступа к данной команде.')
    elif command == 'deop':
        role = get_role(chat_id)
        if role == 'admin':
            change_state(chat_id, 'deop')
            bot.sendMessage(chat_id, 'Введите ID пользователя, которому хотите перестать предоставлять доступ к приватным задачам.')
        else:
            bot.sendMessage(chat_id, 'У вас нет доступа к данной команде.')
    else:
        bot.sendMessage(chat_id, f"Неизвестная команда: {command}")

def handle_text(bot, chat_id, text):
    # bot.sendMessage(chat_id, f"Ищу по тегам: '{text}'. Компиляция может занять некоторое время...")
    # try:
    #     result = find_and_send(bot, chat_id, text)
    # except Exception as e:
    #     bot.sendMessage(chat_id, "Что-то пошло не так...")
    #     bot.sendMessage(chat_id, str(e))
    #     return "OK"
    # if result is None:
    #     bot.sendMessage(chat_id, "Задачи не найдены.")
    #     return "OK"
    # pdf_file, tex_file = result
    # bot.sendDocument(chat_id, pdf_file)
    # bot.sendDocument(chat_id, tex_file)
    # try:
    #     find_and_send(bot, chat_id, text)
    # except Exception as e:
    #     bot.sendMessage(chat_id, "Что-то пошло не так...")
    #     bot.sendMessage(chat_id, str(e))
    user_state = get_state(chat_id)
    if user_state == 'compile':
        subprocess.Popen(['python', 'sub_compile_processer.py', str(chat_id), text])
    elif user_state == 'op':
        try:
            to_op_id = int(text)
            change_role(to_op_id, 'full_access_reader')
            bot.sendMessage(chat_id, 'Успешно.')
            change_state(chat_id, 'default')
            bot.sendMessage(to_op_id, 'Вам предоставлен полный доступ к базе задач.')
        except Exception:
            bot.sendMessage(chat_id, 'Что-то пошло не так. Введите ID ещё раз. Для отмены введите /cancel')
    elif user_state == 'deop':
        try:
            to_deop_id = int(text)
            change_role(to_deop_id, 'default')
            bot.sendMessage(chat_id, 'Успешно.')
            change_state(chat_id, 'default')
        except Exception:
            bot.sendMessage(chat_id, 'Что-то пошло не так. Введите ID ещё раз. Для отмены введите /cancel')
    else:
        subprocess.Popen(['python', 'sub_request_processer.py', str(chat_id), text.lower()])

def handle_callback(bot):
    pass
