# from .models import ArgModel, PlotModel, CameraPosition

ARGS_FNAME = "./webservice/static/args.json"

METR2CM = 100
GRAMPERMOL = 36.38

URL_PREFIX = '/webservice'

# PLOTS_S = [
#     PlotModel('h0', '/static/h0.png', 'Название графика h0', 'Описание', '/static/h0.csv'),
#     PlotModel('Tb', '/static/Tb.png', 'Название графика Td', 'Описание', '/static/Tb.csv')
# ]

INITIAL_VALUES_S = {
    "rhos": 920.0, "Cps": 2010.0, "ks": 2.219, "Th": 0.0, "L": 335000.0, "h0": 0.001
}

HOST = "127.0.0.1:8000"