import datetime
import uuid

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class TaskResult(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    input_data = models.TextField()
    output_data = models.TextField()
    creation_date = models.DateTimeField()
    model_title = models.CharField(max_length=100)
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    #url = models.TextField()


class CameraPosition:
    def __init__(self, elevation, position):
        self.elevation = elevation
        self.azimuth = position


class PlotModel:
    def __init__(self, name, url, alt, description, data_url, camera_pos: CameraPosition):
        self.name = name
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
