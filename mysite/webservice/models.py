import datetime
import uuid

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

import matplotlib.pyplot as plt

from .constants import METR2CM, GRAMPERMOL, URL_PREFIX


class TaskResult(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    input_data = models.TextField()
    output_data = models.TextField()
    creation_date = models.DateTimeField()
    model_title = models.CharField(max_length=100)
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    link_access = models.BooleanField(default=False)
    model_id = models.TextField()


class CameraPosition:
    def __init__(self, elevation, position):
        self.elevation = elevation
        self.azimuth = position


class PlotModel:
    def __init__(self, name, url, alt, description, data_url, camera_pos: CameraPosition=None):
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
        self.value = default


class WolframTask:
    def __init__(self):
        self.id = "model_processes"
        self.tittle = "Затвердевание с двухфазной зоной концентрационного переохлаждения"
        self.description = "Модель, описывающая процессы затвердевания с двухфазной зоной концентрационного переохлаждения"
        self.default_description = "Параметры по умолчанию — сплав TiAl"
        self.args_dict = {
            "ks": ArgModel("ks", 29.22 / METR2CM, "k<sub>s</sub>"),
            "kl": ArgModel("kl", 29 / METR2CM, "k<sub>l</sub>"),
            "k": ArgModel("k", 0.8),
            "gl": ArgModel("gl", 1, "g<sub>l</sub>"),
            "L": ArgModel("L", 12268.8 / GRAMPERMOL),
            "rho": ArgModel("rho", 3.46, "ρ"),
            "Dl": ArgModel("Dl", 8.27 * (10 ** (-9)) * METR2CM * METR2CM, "D<sub>l</sub>"),
            "sigmaInf": ArgModel("sigmaInf", 0.55, "σ<sub>∞</sub>"),
            "m": ArgModel("m", -8.8),
            "gsMin": ArgModel("gsMin", 2, "g<sub>s<sub>min</sub></sub>"),
            "gsMax": ArgModel("gsMax", 25, "g<sub>s<sub>max</sub></sub>"),
            "nMin": ArgModel("nMin", -2, "n<sub>min</sub>"),
            "nMax": ArgModel("nMax", 2, "n<sub>max</sub>"),
        }
        self.source_file = "./static/program.m"
        self.input_file = "./webservice/static/args.json"
        self.plots_list = [
            PlotModel('phi', '/static/phi_interpolated.png', 'Доля твёрдой фазы на границе кристалл-двухфазная зона',
                      'Доля твёрдой фазы на&nbsp;границе кристалл-двухфазная зона в&nbsp;зависимости от&nbsp;градиента температуры в&nbsp;твёрдой фазе g<sub>s</sub> и&nbsp;коэффициента отклонения уравнения ликвидуса от&nbsp;линейного вида&nbsp;n',
                      '/static/phi_interpolated.csv', CameraPosition(25, 45)),
            PlotModel('epsilon', '/static/epsilon.png', 'Безразмерная протяжённость двухфазной зоны',
                      'Безразмерная протяжённость двухфазной зоны',
                      '/static/epsilon.csv', CameraPosition(20, 40)),
            PlotModel('delta', '/static/delta.png', 'Протяженность области фазового перехода',
                      'Протяженность области фазового перехода в&nbsp;зависимости от&nbsp;градиента температуры в&nbsp;твердой фазе',
                      '/static/delta.csv', CameraPosition(30, 40))
        ]

    def draw_plot(self, plot: PlotModel, x_axis, y_axis, z_axis):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(x_axis, y_axis, z_axis, linewidth=0.2, antialiased=True, cmap="autumn", alpha=0.9)
        ax.view_init(plot.camera_pos.elevation, plot.camera_pos.azimuth)
        plt.savefig(f".{URL_PREFIX + plot.src}", bbox_inches='tight')

    # по выходным файлам вольфрам скрипта посторить результат
    def gen_result(self, result_data):
        for plot in self.plots_list:
            x_axis, y_axis, z_axis = result_data[plot.name]
            self.draw_plot(plot, x_axis, y_axis, z_axis)

PLOTS = [
    PlotModel('phi', '/static/phi_interpolated.png', 'Доля твёрдой фазы на границе кристалл-двухфазная зона',
              'Доля твёрдой фазы на&nbsp;границе кристалл-двухфазная зона в&nbsp;зависимости от&nbsp;градиента температуры в&nbsp;твёрдой фазе g<sub>s</sub> и&nbsp;коэффициента отклонения уравнения ликвидуса от&nbsp;линейного вида&nbsp;n',
              '/static/phi_interpolated.csv', CameraPosition(25, 45)),
    PlotModel('epsilon', '/static/epsilon.png', 'Безразмерная протяжённость двухфазной зоны',
              'Безразмерная протяжённость двухфазной зоны',
              '/static/epsilon.csv', CameraPosition(20, 40)),
    PlotModel('delta', '/static/delta.png', 'Протяженность области фазового перехода',
              'Протяженность области фазового перехода в&nbsp;зависимости от&nbsp;градиента температуры в&nbsp;твердой фазе',
              '/static/delta.csv', CameraPosition(30, 40))
]

ARGS_FORM = {
    "ks": ArgModel("ks", 29.22 / METR2CM, "k<sub>s</sub>"),
    "kl": ArgModel("kl", 29 / METR2CM, "k<sub>l</sub>"),
    "k": ArgModel("k", 0.8),
    "gl": ArgModel("gl", 1, "g<sub>l</sub>"),
    "L": ArgModel("L", 12268.8 / GRAMPERMOL),
    "rho": ArgModel("rho", 3.46, "ρ"),
    "Dl": ArgModel("Dl", 8.27 * (10 ** (-9)) * METR2CM * METR2CM, "D<sub>l</sub>"),
    "sigmaInf": ArgModel("sigmaInf", 0.55, "σ<sub>∞</sub>"),
    "m": ArgModel("m", -8.8),
    "gsMin": ArgModel("gsMin", 2, "g<sub>s<sub>min</sub></sub>"),
    "gsMax": ArgModel("gsMax", 25, "g<sub>s<sub>max</sub></sub>"),
    "nMin": ArgModel("nMin", -2, "n<sub>min</sub>"),
    "nMax": ArgModel("nMax", 2, "n<sub>max</sub>"),
}

ARGS = [arg.json_name for arg in ARGS_FORM.values()]
