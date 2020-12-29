from django import forms
from problemset.models import Problem,TestCase
from problemset.models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['solution_language', 'solution']


class ProblemCreateForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'statement', 'input_section', 'output_section', 'editorial', 'is_protected','solution','solution_language']


class TestCreateForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['label', 'input', 'output', 'is_sample', 'notes']