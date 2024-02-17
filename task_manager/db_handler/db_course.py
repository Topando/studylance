from ..models import Course


def courses_update():
    for i in range(1, 5):
        try:
            Course(course=str(i)).save()
        except Exception:
            print("ЛОХ")