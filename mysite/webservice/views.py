import csv
import json
import subprocess

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

from .constants import ARGS, ARGS_FORM, ARGS_FNAME, INITIAL_VALUES, URL_PREFIX, plots
from .models import PlotModel, ArgModel, CameraPosition, TaskResult
from .task_forms.task_form import TaskForm
from subprocess import check_output
from datetime import datetime


def main_page(request):
    return render(request, 'webservice/main_page.html', {'section': 'main'})


def get_result(request):
    input_data = request.POST

    task_info = TaskResult()
    task_info.input_data = save_args(input_data)

    run_model()

    output_params = {}
    for plot in plots:
        x_axis, y_axis, z_axis = get_points(f".{URL_PREFIX + plot.data_url}")
        output_params[plot.name] = [x_axis, y_axis, z_axis]
        draw_plot(plot, x_axis, y_axis, z_axis)

    task_info.creation_date = datetime.now()
    task_info.output_data = json.dumps(output_params)
    task_info.save()
    return render(request, 'webservice/results.html', {'plots': plots})


def model(request):
    if request.method == 'POST':

        return get_result(request)
    else:
        form = TaskForm(request.GET, initial=INITIAL_VALUES)

    return render(request, 'webservice/task.html', {'form': form})


def run_model():
    out = check_output("wolframscript -script ./static/program.m", stderr=subprocess.STDOUT,
                       stdin=subprocess.DEVNULL)
    #app.logger.info(out)


def save_args(form_data):  # TODO: using db
    args = {}
    for argName in ARGS:
        value = float(form_data[argName])
        if value:
            args[argName] = value
    content = json.dumps(args)
    with open(ARGS_FNAME, "w") as file:
        file.write(content)
    return content


def draw_plot(plot: PlotModel, x_axis, y_axis, z_axis):
    # x_axis, y_axis, z_axis = get_points(f".{URL_PREFIX + plot.data_url}")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x_axis, y_axis, z_axis, linewidth=0.2, antialiased=True, cmap="autumn", alpha=0.9)
    ax.view_init(plot.camera_pos.elevation, plot.camera_pos.azimuth)
    plt.savefig(f".{URL_PREFIX + plot.src}", bbox_inches='tight')


def get_points(fname):
    with open(fname, 'r') as f:
        points = [list(map(float, row)) for row in csv.reader(f)]
    x_axis = [p[0] for p in points]
    y_axis = [p[1] for p in points]
    z_axis = [p[2] for p in points]

    return x_axis, y_axis, z_axis
