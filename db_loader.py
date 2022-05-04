from os import walk
import pickle
import re


default_db_path = "materials/problems_db"

filter = [('1001', '1.20')]

private_books = ['original']
private_tags = ['говно', 'физбой']
private_roles = ['admin', 'full_access_reader']


def load_problem(db_path, book_name, problem_name):
    file = open(db_path + '/' + book_name + '/' + problem_name + '.tex', encoding="utf-8")
    text = file.read()
    tags_pattern = '\\tags'
    answer_pattern = '\\answer'

    tag_pos = text.find(tags_pattern)
    ans_pos = text.find(answer_pattern)
    task_text = text.lower()
    if tag_pos != -1:
        task_text = task_text[:tag_pos]
    if ans_pos != -1:
        task_text = task_text[:ans_pos]

    tags = None
    if tag_pos != -1:
        tags_text = text[text.find(tags_pattern) + len(tags_pattern) + 1:]
        tags_text = tags_text[:tags_text.find('}')]
        if not len(tags_text) == 0:
            tags = re.split('\s*,\s*', tags_text)
            tags = list(map(str.lower, tags))
            tags = list(map(str.strip, tags))


    return task_text, tags


def generate_db(db_path=default_db_path):
    tags_db = {}
    text_db = []
    for (dir_path, dir_names, file_names) in walk(db_path):
        for problem_name in file_names:
            if not problem_name.endswith('.tex'):
                continue
            if problem_name.endswith('fig.tex'):
                continue
            problem_name = problem_name[:-4]
            directories = dir_path.split('/')
            book_name = directories[len(directories) - 1]
            if (book_name, problem_name) in filter:
                continue
            task_text, tags = load_problem(db_path, book_name, problem_name)

            text_db.append(((book_name, problem_name), task_text))

            if tags is None:
                continue
            for tag in tags:
                if tag not in tags_db:
                    tags_db.update({tag: [(book_name, problem_name)]})
                else:
                    tags_db[tag].append((book_name, problem_name))

    file = open('tags_db.pkl', 'wb')
    pickle.dump(tags_db, file)
    file.close()

    file = open('text_db.pkl', 'wb')
    pickle.dump(text_db, file)
    file.close()


def load_tags(role='default'):
    file = open('tags_db.pkl', 'rb')
    tags_db = pickle.load(file)
    file.close()

    # TODO: implement private
    if not role in private_roles:
        for banned_tag in private_tags:
            tags_db.pop(banned_tag, None)
        for tag in tags_db:
            filtered_problems = []
            for book_name, problem_name in tags_db[tag]:
                if book_name in private_books:
                    continue
                filtered_problems.append((book_name, problem_name))
            tags_db[tag] = filtered_problems

    return tags_db


def load_text(role='default'):
    file = open('text_db.pkl', 'rb')
    text_db = pickle.load(file)
    file.close()

    # TODO: implement private
    if not role in private_roles:
        filtered_db = []
        for problem, text in text_db:
            book_name, problem_name = problem
            if book_name in private_books:
                continue
            filtered_db.append((problem, text))
        text_db = filtered_db

    return text_db


if __name__ == '__main__':
    # generate_db()
    print(len(load_tags(role='admin')))
    print(len(load_text(role='admin')))
    # db = load_tags()
    # tags = list(db.keys())
    # print(len(tags))
    # print(len(set(tags)))
    # print(sorted(tags))
