import django_filters
from .models import Question


# https://django-filter.readthedocs.io/en/master/index.html
class QuestionFilter(django_filters.FilterSet):
    
    class Meta:
        model = Question

        # Fields is a dictionary of model_field:lookup_expression
        fields = {
            'title': ['icontains'],
            'content': ['icontains'],
            'subject': ['exact'],
            'level': ['exact'],
        }