import pickle


def handle_chat_id(chat_id, new_data=None):
    try:
        f = open('user_db.pkl', 'rb')
        user_db = pickle.load(f)
        f.close()
    except FileNotFoundError:
        user_db = {}

    if not chat_id in user_db:
        user_data = {'state': 'default', 'role': 'default'}
        user_db[chat_id] = user_data

    if new_data is not None:
        user_db[chat_id].update(new_data)

    f = open('user_db.pkl', 'wb')
    pickle.dump(user_db, f)
    f.close()

    return user_db[chat_id]['state']


def get_state(chat_id):
    f = open('user_db.pkl', 'rb')
    user_db = pickle.load(f)
    f.close()
    return user_db[chat_id]['state']


def change_state(chat_id, new_state):
    f = open('user_db.pkl', 'rb')
    user_db = pickle.load(f)
    f.close()

    user_db[chat_id]['state'] = new_state

    f = open('user_db.pkl', 'wb')
    pickle.dump(user_db, f)
    f.close()

def get_role(chat_id):
    f = open('user_db.pkl', 'rb')
    user_db = pickle.load(f)
    f.close()
    return user_db[chat_id]['role']


def change_role(chat_id, new_role):
    f = open('user_db.pkl', 'rb')
    user_db = pickle.load(f)
    f.close()

    user_db[chat_id]['role'] = new_role

    f = open('user_db.pkl', 'wb')
    pickle.dump(user_db, f)
    f.close()


def add_new_mandatory_key(key, value):
    f = open('user_db.pkl', 'rb')
    user_db = pickle.load(f)
    f.close()

    for chat_id in user_db:
        user_db[chat_id][key] = value

    f = open('user_db.pkl', 'wb')
    pickle.dump(user_db, f)
    f.close()


if __name__== '__main__':
    # add_new_mandatory_key('role', 'default')

    f = open('user_db.pkl', 'rb')
    user_db = pickle.load(f)

    import json
    print(json.dumps(user_db, sort_keys=True, indent=4))

    # print(user_db)
    # print(handle_chat_id(147093804))
    # change_state(147093804, 'compile')

    # change_role(147093804, 'admin')
