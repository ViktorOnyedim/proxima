from django.contrib import admin
from quiz import models

# Register your models here.
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

class ChoiceInlineModel(admin.TabularInline):
    model = models.Choice
    fields = ['text', 'is_correct']

class QuestionAdmin(admin.ModelAdmin):
    fields = ['quiz', 'text', 'type', 'order']
    list_display = ['text', 'type', 'order', 'quiz']
    inlines = [ChoiceInlineModel]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_correct', 'text')

admin.site.register(models.Organization)
admin.site.register(models.QuizCreator)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.QuizResult)
admin.site.register(models.ParticipantAnswer)
admin.site.register(models.Choice, ChoiceAdmin)
admin.site.register(models.Participant)
