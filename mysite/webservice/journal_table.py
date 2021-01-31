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
    id = tables.Column(verbose_name="Просмотр", orderable=False, attrs={
            "td": {"align": "center"}
        })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render_creation_date(self, value, record):
        return value.strftime("%d.%m.%Y, %H:%M")

    def render_id(self, value, record):
        url = "http://{}/webservice/show_result/{}/".format(HOST, record.id)
        return format_html('<a href="{}"><i class="fa fa-search"></a>', url)
