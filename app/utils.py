def check_author_task(user, pk):
    if user.pk == pk:
        return True
    return False


def check_is_executor(executor_id):
    if executor_id is None:
        return True
    return False


def check_task_delete(user, pk, executor_id):
    if check_author_task(user, pk) and check_is_executor(executor_id):
        return True
    return False