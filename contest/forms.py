from django import forms

from contest.models import Contest
from contest.widgets import BootstrapDateTimePickerInput


class ContestForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%m/%d/%Y %I:%M %p'],
        widget=BootstrapDateTimePickerInput(),
        required=True
    )

    class Meta:
        model = Contest
        fields = [
            'title',
            'description',
            'start_time',
            'duration',
            'is_rated'
        ]
