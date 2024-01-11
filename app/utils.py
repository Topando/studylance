from itertools import count


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


def check_create_task(user, Task):
    count_tasks = Task.objects.filter(customer_id=user.id).count()
    if count_tasks > 10:
        return False
    if not user.profile.is_customer:
        return False
    return True
