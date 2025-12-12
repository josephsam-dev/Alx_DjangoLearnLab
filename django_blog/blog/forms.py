from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'})
    )

    class Meta:
        model = Comment
        fields = ['content']
