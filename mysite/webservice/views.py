import json
import subprocess
from subprocess import check_output

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.utils.safestring import mark_safe
from django_tables2 import RequestConfig

from .journal_table import JournalTable
from .constants import ARGS_FNAME
from .models import ArgModel, TaskResult
from .task_forms.task_form import TaskForm
from .wolfram_tasks import wolfram_tasks
from datetime import datetime


def main_page(request):
    return render(request, 'webservice/main_page.html', {'section': 'main'})


@login_required
def get_result(request, model_id):
    input_data = request.POST

    task_info = TaskResult()
    task_info.input_data = save_args(input_data, model_id)

    current_model = wolfram_tasks[model_id]

    out = check_output("wolframscript -script {}".format(current_model.source_file), stderr=subprocess.STDOUT,
                       stdin=subprocess.DEVNULL)

    output_params = current_model.run_model()

    task_info.creation_date = datetime.now()
    task_info.output_data = json.dumps(output_params)
    task_info.created_by_user = request.user
    task_info.model_title = current_model.tittle
    task_info.model_id = model_id
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

    current_model = wolfram_tasks[task_info.model_id]
    current_model.gen_result(result_data)
    params = [ArgModel(arg, input_data[arg], mark_safe(current_model.args_dict[arg].displayed_name)) for arg in input_data.keys()]
    query_string = '&'.join([p.json_name + '=' + str(p.value) for p in params])
    return render(request, 'webservice/results.html',
                  {
                      'plots': current_model.plots_list,
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
        return get_result(request, model_id)
    else:
        show_hint = False
        if request.GET & TaskForm(task).fields.keys():
            form = TaskForm(task, request.GET)
        else:
            initial_values = {}
            for arg in task.args_dict.values():
                initial_values[arg.json_name] = arg.value
            form = TaskForm(task, initial=initial_values)
            show_hint = True

    return render(request, 'webservice/task.html', {
        'form': form,
        'show_hint': show_hint,
        'model_id': model_id,
        'model_description': task.description,
        'default_description': task.default_description,
    })


def save_args(form_data, model_id):  # TODO: using db
    current_model = wolfram_tasks[model_id]
    args = {}
    for argName in current_model.args_dict:
        value = float(form_data[argName])
        if value:
            args[argName] = value
    content = json.dumps(args)
    with open(ARGS_FNAME, "w") as file:
        file.write(content)
    return content
