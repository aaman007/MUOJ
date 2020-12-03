from django import forms

from problemset.models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['solution_language', 'solution']
