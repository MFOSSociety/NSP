from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from qa.models import (Answer, AnswerComment, AnswerVote, Question,
                       QuestionComment)

admin.site.register(Question)
admin.site.register(Answer, MarkdownxModelAdmin)
admin.site.register(AnswerComment)
admin.site.register(QuestionComment)
admin.site.register(AnswerVote)
