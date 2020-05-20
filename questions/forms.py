from django.forms import ModelForm, Textarea, TextInput

from .models import Question, Answer


# https://stackoverflow.com/questions/16417683/django-displaying-charfield-as-textfield-in-forms-error
class SubmitQnForm(ModelForm):
    class Meta:
        model = Question
        fields = [
            'title',
            'content',
            'image',
            'subject',
            'level'
        ]
        widgets = {
            # https://stackoverflow.com/questions/9323886/increase-charfield-width-in-django-forms
            'title': TextInput(attrs={'size': 50}), 
            'content': Textarea(attrs={'cols':80, 'rows':10, 'class': 'form-control'}),
            
        }

class SubmitAnsForm(ModelForm):
    class Meta:
        model = Answer
        fields = [
            'content',
        ]
        widgets = {
            'content': Textarea(attrs={'cols':70, 'rows':3, 'class': 'form-control'}),
        }