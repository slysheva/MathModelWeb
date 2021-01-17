from .models import ArgModel, PlotModel, CameraPosition

ARGS_FNAME = "./webservice/static/args.json"

METR2CM = 100
GRAMPERMOL = 36.38

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

URL_PREFIX = '/webservice'

plots = [
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

INITIAL_VALUES = {
    "ks": float(0.2922),
    "kl": 0.29,
    "k": 0.8,
    "gl": 1,
    "L": 337.2402418911489,
    "rho": 3.46,
    "Dl": 8.27e-05,
    "sigmaInf": 0.55,
    "m": -8.8,
    "gsMin": 2,
    "gsMax": 25,
    "nMin": -2,
    "nMax": 2
}