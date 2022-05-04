from db_loader import load_text, load_tags


def find_tags(tags, tags_db):
    # TODO implement partial fit and delivery_mode selection
    fitting_problems = None
    for tag in tags:
        this_tag_problems = tags_db[tag]
        if fitting_problems is None:
            fitting_problems = this_tag_problems
        else:
            fitting_problems = set(fitting_problems).intersection(this_tag_problems)
            if len(fitting_problems) == 0:
                return []
    return list(fitting_problems)


def find(tags, strings, role='default'):
    fitting_problems = None

    if len(tags) > 0:
        tags_db = load_tags(role=role)
        for tag in tags:
            this_tag_problems = tags_db[tag]
            if fitting_problems is None:
                fitting_problems = this_tag_problems
            else:
                fitting_problems = set(fitting_problems).intersection(this_tag_problems)

    if len(strings) > 0:
        text_db = load_text(role=role)
        for s in strings:
            this_s_problems = []
            for problem, task_text in text_db:
                if s.lower() in task_text:
                    this_s_problems.append(problem)
            if fitting_problems is None:
                fitting_problems = this_s_problems
            else:
                fitting_problems = set(fitting_problems).intersection(this_s_problems)
    if fitting_problems is None:
        return []
    return list(fitting_problems)
