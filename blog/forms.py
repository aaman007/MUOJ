from django import forms

from blog.models import Blog,Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(
                attrs={'placeholder': 'Add a comment'}
            )
        }
        labels = {'comment': ''}
