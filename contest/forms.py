import datetime

from django import forms

from contest.models import Contest
from contest.widgets import BootstrapDateTimePickerInput


class ContestForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %I:%M %p'],
        help_text='Format: DD/MM/YYYY HH:MM AM/PM',
        widget=BootstrapDateTimePickerInput,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.id:
            kwargs.update(initial={
                'start_time': datetime.datetime.now().strftime('%d/%m/%Y %H:%M %p'),
                'duration': '00:00:00'
            })
        else:
            kwargs.update(initial={
                'start_time': self.instance.start_time.strftime('%d/%m/%Y %H:%M %p'),
            })
        super().__init__(*args, **kwargs)

    class Meta:
        model = Contest
        fields = [
            'title',
            'description',
            'start_time',
            'duration',
            'is_rated'
        ]
        help_texts = {
            'duration': 'Format: HH:MM:SS'
        }

