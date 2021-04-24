from django import forms
from django.utils.safestring import mark_safe


class TaskForm(forms.Form):

    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_args = model.args_dict
        for arg in form_args.values():
            self.fields[arg.json_name] = forms.FloatField(label=mark_safe(arg.displayed_name))
