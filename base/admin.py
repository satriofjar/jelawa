from django.contrib import admin
from .models import Island, City, Question, Answer
# Register your models here.

class AnswareInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
     inlines = (AnswareInline,)


admin.site.register(Island)
admin.site.register(City)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
