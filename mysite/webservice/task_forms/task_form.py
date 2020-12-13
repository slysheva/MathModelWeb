from django import forms
from django.utils.safestring import mark_safe

from ..constants import ARGS_FORM, INITIAL_VALUES


class TaskForm(forms.Form):
    ks = forms.FloatField(label=mark_safe(ARGS_FORM["ks"].displayed_name), initial=INITIAL_VALUES["ks"])
    kl = forms.FloatField(label=mark_safe(ARGS_FORM["kl"].displayed_name))
    k = forms.FloatField(label=mark_safe(ARGS_FORM["k"].displayed_name))
    gl = forms.FloatField(label=mark_safe(ARGS_FORM["gl"].displayed_name))
    L = forms.FloatField(label=mark_safe(ARGS_FORM["L"].displayed_name))
    rho = forms.FloatField(label=mark_safe(ARGS_FORM["rho"].displayed_name))
    Dl = forms.FloatField(label=mark_safe(ARGS_FORM["Dl"].displayed_name))
    sigmaInf = forms.FloatField(label=mark_safe(ARGS_FORM["sigmaInf"].displayed_name))
    m = forms.FloatField(label=mark_safe(ARGS_FORM["m"].displayed_name))
    gsMin = forms.FloatField(label=mark_safe(ARGS_FORM["gsMin"].displayed_name))
    gsMax = forms.FloatField(label=mark_safe(ARGS_FORM["gsMax"].displayed_name))
    nMin = forms.FloatField(label=mark_safe(ARGS_FORM["nMin"].displayed_name))
    nMax = forms.FloatField(label=mark_safe(ARGS_FORM["nMax"].displayed_name))

