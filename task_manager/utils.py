from studlance.settings import MAX_FILE_SIZE
from task_manager.models import ImagesTask, FilesTask, Task


def check_files(objs):
    if check_files_size(objs) and check_files_count(objs):
        return True
    return False


def check_files_size(objs):
    for obj in objs:
        if obj.size > MAX_FILE_SIZE:
            return False
    return True


def check_files_count(objs):
    if len(objs) <= 5:
        return True
    return False


def images_in_db(images, task):
    for image in images:
        ImagesTask.objects.create(task_id=task, image=image)


def files_in_db(files, task):
    for file in files:
        FilesTask.objects.create(task_id=task, file=file)


def get_task_by_task_id(task_id):
    return Task.objects.get(pk=task_id)


def get_count_files_in_task(task_id, obj):
    return obj.objects.filter(task_id=task_id).count()


def check_task_delete(user, pk, executor_id):
    if check_author_task(user, pk) and check_is_executor(executor_id):
        return True
    return False


def check_author_task(user, pk):
    if user.pk == pk:
        return True
    return False


def check_is_executor(executor_id):
    if executor_id is None:
        return True
    return False


def get_user_by_image_id(image_id):
    user_id = ImagesTask.objects.filter(pk=image_id).first().task_id.customer_id.id
    return user_id


def get_image_by_image_id(image_id):
    return ImagesTask.objects.filter(pk=image_id).first()


def delete_image_by_task(image):
    try:
        image.delete()
    except Exception:
        print("Ошибка удаления фотографии")
