from django import forms

from channel.models import Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['text']
