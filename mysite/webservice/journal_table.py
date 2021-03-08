import django_tables2 as tables
from django.utils.html import format_html

from .constants import HOST
from .models import TaskResult


class JournalTable(tables.Table):
    class Meta:
        model = TaskResult
        template_name = "django_tables2/bootstrap.html"
        fields = ("model_title", "creation_date", "id")

    model_title = tables.Column(verbose_name="Название модели")
    creation_date = tables.Column(verbose_name="Дата создания")
    id = tables.Column(verbose_name="Действия", orderable=False, attrs={
            "td": {"align": "center"}
        })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render_creation_date(self, value, record):
        return value.strftime("%d.%m.%Y, %H:%M")

    def render_id(self, value, record):
        search_url = "http://{}/webservice/show_result/{}/".format(HOST, record.id)
        return (format_html('<a href="{}" data-toggle="tooltip" title="Просмотр"><i class="fa fa-search"></i></a>', search_url)
                + format_html('<a href="{}" data-toggle="tooltip" title="Удалить"><i class="fa fa-trash"></i></a>', search_url))
