from django.contrib import admin

from .models import User, Question, Subject, Level, Answer


class QuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ("saved_by",)
    
# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Level)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)