import django_filters
from .models import Question

class QuestionFilter(django_filters.FilterSet):
    
    class Meta:
        model = Question

        # Fields is a dictionary of model_field:lookup_expression
        fields = {
            'title': ['contains'],
            'content': ['icontains'],
            'subject': ['exact'],
            'level': ['exact'],
        }