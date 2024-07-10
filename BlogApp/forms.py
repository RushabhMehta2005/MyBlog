from django import forms
from .models import Blog


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "content"]


class DeleteBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = []
