import django_filters

from task_manager.forms import MyDateInput
from task_manager.models import Task


class TaskFilter(django_filters.FilterSet):
    time_created = django_filters.DateFilter(
        'time_created', label='От',
        lookup_expr='gte',
        widget=MyDateInput()
    )
    time_created_end = django_filters.DateFilter(
        'time_created', label='До',
        lookup_expr='lte',
        widget=MyDateInput()
    )

    deadline = django_filters.DateFilter(
        'deadline', label='От',
        lookup_expr='gte',
        widget=MyDateInput()
    )
    deadline_end = django_filters.DateFilter(
        'deadline', label='До',
        lookup_expr='lte',
        widget=MyDateInput()
    )

    class Meta:
        model = Task
        fields = ('time_created', "deadline",)
        ordering_fields = ('-time_created',)