import csv
import json
import subprocess

from django.shortcuts import render

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

from .constants import ARGS, ARGS_FORM, ARGS_FNAME, INITIAL_VALUES, URL_PREFIX, plots
from .models import PlotModel, ArgModel, CameraPosition
from .task_forms.task_form import TaskForm
from subprocess import check_output



# class IndexView(generic.ListView):
#     template_name = 'webservice/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         return Question.objects.filter(
#             pub_date__lte=timezone.now()
#         ).order_by('-pub_date')[:5]
#
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'webservice/detail.html'
#
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())
#
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'webservice/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('webservice:results',
#                                             args=(question.id,)))


def list_tasks(request):
    tasks = ["firstTask"]
    return render(request, 'webservice/tasks.html', {"tasks": tasks})



def get_result(request):
    input_data = request.POST

    save_args(input_data)

    run_model()
    for plot in plots:
        draw_plot(plot)

    return render(request, 'webservice/results.html', {'plots': plots})
  #  return render(request, 'webservice/answer.html', {"answer": ans})


def solve_task(request):
    if request.method == 'POST':

        return get_result(request)
    else:
        form = TaskForm(request.GET, initial=INITIAL_VALUES)




    return render(request, 'webservice/task.html', {'form': form})


def run_model():
    out = check_output("wolframscript -script ./static/program.m", stderr=subprocess.STDOUT,
                       stdin=subprocess.DEVNULL)
    #app.logger.info(out)


def save_args(form_data):
    print(form_data)
    args = {}
    for argName in ARGS:
        value = float(form_data[argName])
        if value:
            args[argName] = value
    with open(ARGS_FNAME, "w") as file:
        file.write(json.dumps(args))


def draw_plot(plot: PlotModel):
    x_axis, y_axis, z_axis = get_points(f".{URL_PREFIX + plot.data_url}")
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



