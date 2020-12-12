from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from problemset.models import Problem,TestCase

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ProblemCreateForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'statement', 'input_section', 'output_section', 'editorial', 'is_protected','solution','solution_language']

class TestCreateForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['label', 'input', 'output', 'is_sample', 'notes', 'problem']
