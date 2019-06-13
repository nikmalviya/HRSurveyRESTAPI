from django.contrib import admin

from .models import Question, QuestionChoice


class QuestionChoiceAdmin(admin.TabularInline):
    model = QuestionChoice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        QuestionChoiceAdmin
    ]


admin.site.register(Question, QuestionAdmin)
