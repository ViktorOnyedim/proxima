from django.contrib import admin
from quiz import models

# Register your models here.
admin.site.register(models.Organization)
admin.site.register(models.QuizCreator)
admin.site.register(models.Quiz)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Choice)
admin.site.register(models.Participant)

