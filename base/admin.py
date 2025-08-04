from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Answer, City, Island, Question

# Register your models here.

class AnswareInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(SummernoteModelAdmin):
    inlines = (AnswareInline,)
    list_filter = ("city__name",)
    summernote_fields = ('text',)


admin.site.register(Island)
admin.site.register(City)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

# Admin site custiom title
admin.site.site_header = "Jelawa Administrator"
admin.site.site_title = "Jelawa Admin"
admin.site.index_title = "Welcome to Jelawa Administrator"
