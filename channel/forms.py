from django import forms

from channel.models import Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Enter Message'}),
        }

    def __init__(self):
        super().__init__()
        self.fields['text'].label = ''
