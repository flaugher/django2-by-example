from django import forms

from .models import Comment

# Use forms.Form when you're building a form that doesn't correspond to a model.
# Use forms.ModelForm when you're building a form that does correpond to a model.

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)