from django import forms
from .models import Topic

class NewTopic(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':5,'placeholder':'write her '}),max_length=4000,
                                       help_text='the max length=4000 character')
    class Meta:
        model=Topic
        fields=['subject','message']