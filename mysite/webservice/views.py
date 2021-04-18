import csv
import json
import subprocess

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

import matplotlib.pyplot as plt
from django.utils.safestring import mark_safe
from django_tables2 import RequestConfig

from mpl_toolkits.mplot3d import Axes3D

from .journal_table import JournalTable
from .constants import ARGS_FNAME, URL_PREFIX
from .models import PlotModel, ArgModel, CameraPosition, TaskResult, ARGS_FORM, PLOTS, ARGS
from .task_forms.task_form import TaskForm
from .wolfram_tasks import wolfram_tasks
from subprocess import check_output
from datetime import datetime


def main_page(request):
    return render(request, 'webservice/main_page.html', {'section': 'main'})


@login_required
def get_result(request):
    input_data = request.POST

    task_info = TaskResult()
    task_info.input_data = save_args(input_data)

    run_model()

    output_params = {}
    for plot in PLOTS:
        x_axis, y_axis, z_axis = get_points(f".{URL_PREFIX + plot.data_url}")
        output_params[plot.name] = [x_axis, y_axis, z_axis]

    task_info.creation_date = datetime.now()
    task_info.output_data = json.dumps(output_params)
    task_info.created_by_user = request.user
    task_info.model_title = "Затвердевание с двухфазной зоной концентрационного переохлаждения"
    task_info.model_id = 'model_processes'
    task_info.save()
    return redirect('webservice:show_result', task_info_id=task_info.id)


@login_required
def get_journal(request):
    config = RequestConfig(request)
    tasks = TaskResult.objects.filter(created_by_user=request.user)
    table = JournalTable(tasks)
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    config.configure(table)
    return render(request, 'webservice/journal.html', {'table': table, 'section': 'journal'})


@login_required
def delete_journal_record(request, record_id):
    task = get_object_or_404(TaskResult, id=record_id)
    if task.created_by_user == request.user:
        task.delete()
    return redirect('webservice:journal')


@login_required
def open_view_access(request, record_id):
    task = get_object_or_404(TaskResult, id=record_id)
    if task.created_by_user == request.user:
        task.link_access = True
        task.save()
    return redirect('webservice:show_result', task_info_id=record_id)


@login_required
def close_view_access(request, record_id):
    task = get_object_or_404(TaskResult, id=record_id)
    if task.created_by_user == request.user:
        task.link_access = False
        task.save()
    return redirect('webservice:show_result', task_info_id=record_id)


def show_result(request, task_info_id):
    task_info = get_object_or_404(TaskResult, id=task_info_id)
    if task_info.created_by_user != request.user and not task_info.link_access:
        return HttpResponse("Ошибка. Нет прав на просмотр.")
    input_data = json.loads(task_info.input_data)
    result_data = json.loads(task_info.output_data)
    for plot in PLOTS:
        x_axis, y_axis, z_axis = result_data[plot.name]
        draw_plot(plot, x_axis, y_axis, z_axis)
    params = [ArgModel(arg, input_data[arg], mark_safe(ARGS_FORM[arg].displayed_name)) for arg in input_data.keys()]
    query_string = '&'.join([p.json_name + '=' + str(p.value) for p in params])
    return render(request, 'webservice/results.html',
                  {
                      'plots': PLOTS,
                      'params': params,
                      'query_string': query_string,
                      'record_id': task_info_id,
                      'edit_mode': task_info.created_by_user == request.user,
                      'access_opened': task_info.link_access,
                      'model_id': task_info.model_id,
                  })


def model(request, model_id):
    if model_id not in wolfram_tasks:
        return HttpResponse("Модель не найдена")  # TODO: throw 404
    task = wolfram_tasks[model_id]
    if request.method == 'POST':
        return get_result(request)
    else:
        show_hint = False
        if request.GET & TaskForm.base_fields.keys():
            form = TaskForm(request.GET)
        else:
            initial_values = {}
            for arg in task.args_dict.values():
                initial_values[arg.json_name] = arg.value
            form = TaskForm(initial=initial_values)
            show_hint = True

    return render(request, 'webservice/task.html', {
        'form': form,
        'show_hint': show_hint,
        'model_id': model_id,
        'model_description': task.description,
        'default_description': task.default_description,
    })


def run_model():
    out = check_output("wolframscript -script ./static/program.m", stderr=subprocess.STDOUT,
                       stdin=subprocess.DEVNULL)
    # app.logger.info(out)


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
