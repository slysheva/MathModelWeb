import datetime

from django.utils import timezone
from django.db import models


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.question_text
#
#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now
#
#     was_published_recently.admin_order_field = 'pub_date'
#     was_published_recently.boolean = True
#     was_published_recently.short_description = 'Published recently?'
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.choice_text

class CameraPosition:
    def __init__(self, elevation, position):
        self.elevation = elevation
        self.azimuth = position


class PlotModel:
    def __init__(self, url, alt, description, data_url, camera_pos: CameraPosition):
        self.src = url
        self.alt = alt
        self.description = description
        self.data_url = data_url
        self.camera_pos = camera_pos


class ArgModel:
    def __init__(self, json_name, default, displayed_name=None):
        self.json_name = json_name
        self.displayed_name = displayed_name if displayed_name else json_name
        self.default = default
