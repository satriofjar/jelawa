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

# Admin site custiom title
admin.site.site_header = "Jelawa Administrator"
admin.site.site_title = "Jelawa Admin"
admin.site.index_title = "Welcome to Jelawa Administrator"
