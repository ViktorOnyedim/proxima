from django.contrib import admin
from quiz import models

# Register your models here.
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_correct', 'text')

admin.site.register(models.Organization)
admin.site.register(models.QuizCreator)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Question)
admin.site.register(models.QuizResult)
admin.site.register(models.ParticipantAnswer)
admin.site.register(models.Choice, ChoiceAdmin)
admin.site.register(models.Participant)
