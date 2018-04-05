from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={"icon": "font"}), label="Add comment...")
    class Meta:
        model = Comment
        fields = ("content",)
