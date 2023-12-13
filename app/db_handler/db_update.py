from .db_direction import direction_update
from .db_university import university_update


def database_filling():
    university_update()
    direction_update()
