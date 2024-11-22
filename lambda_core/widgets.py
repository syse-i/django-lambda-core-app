from django import forms


class ClearableFileInput(forms.ClearableFileInput):
    # noinspection PyUnresolvedReferences
    template_name = 'forms/widgets/clearable_file_input.html'
