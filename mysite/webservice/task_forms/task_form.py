from django import forms
from django.utils.safestring import mark_safe

from ..wolfram_tasks import wolfram_tasks

class TaskForm(forms.Form):
    args = wolfram_tasks['model_processes'].args_dict
    ks = forms.FloatField(label=mark_safe(args["ks"].displayed_name))
    kl = forms.FloatField(label=mark_safe(args["kl"].displayed_name))
    k = forms.FloatField(label=mark_safe(args["k"].displayed_name))
    gl = forms.FloatField(label=mark_safe(args["gl"].displayed_name))
    L = forms.FloatField(label=mark_safe(args["L"].displayed_name))
    rho = forms.FloatField(label=mark_safe(args["rho"].displayed_name))
    Dl = forms.FloatField(label=mark_safe(args["Dl"].displayed_name))
    sigmaInf = forms.FloatField(label=mark_safe(args["sigmaInf"].displayed_name))
    m = forms.FloatField(label=mark_safe(args["m"].displayed_name))
    gsMin = forms.FloatField(label=mark_safe(args["gsMin"].displayed_name))
    gsMax = forms.FloatField(label=mark_safe(args["gsMax"].displayed_name))
    nMin = forms.FloatField(label=mark_safe(args["nMin"].displayed_name))
    nMax = forms.FloatField(label=mark_safe(args["nMax"].displayed_name))
