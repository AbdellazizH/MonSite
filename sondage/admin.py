from django.contrib import admin

from sondage.models import Question, Choice

# Register your models here.
class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields': ['question_text'], 'classes':['collapse']}),
        ('Date', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inLines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
