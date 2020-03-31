from django import forms
from .models import Post,Comments
from ckeditor.widgets import CKEditorWidget



class ContentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields  = [
            'title',
            'overview',
            'content',
            'author',
            'thumbnail',
            'categories',
            'featured',
            'prev_post',
            'next_post'
            
        ]


class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'name':"name",
        'id':"name",
        'placeholder':"name",
        'class':"form-control form-group col-md-6",
    }), label="")
    content = forms.CharField(widget=forms.Textarea(attrs={
        'name':"usercomment",
        'id':"usercomment",
        'placeholder':"Type your comment",
        'class':"form-control form-group col-md-12",
        'rows':"4",
    }), label="")

    class Meta:
        model = Comments
        fields = [
            'name',
            'content',
        ]