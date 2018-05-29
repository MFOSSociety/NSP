from django.urls import re_path, include
from . import views


urlpatterns = [


    re_path('', views.QuestionIndexView.as_view(), name='qa_index'),

    re_path('question/(?P<pk>\d+)/',
        views.QuestionDetailView.as_view(), name='qa_detail'),

    re_path('question/(?P<pk>\d+)/(?P<slug>[-_\w]+)/',
        views.QuestionDetailView.as_view(), name='qa_detail'),

    re_path('question/answer/(?P<answer_id>\d+)/',
        views.AnswerQuestionView.as_view(), name='qa_answer_question'),

    re_path('question/close/(?P<question_id>\d+)/',
        views.CloseQuestionView.as_view(), name='qa_close_question'),

    re_path('new-question/', views.CreateQuestionView.as_view(),
        name='qa_create_question'),

    re_path('edit-question/(?P<question_id>\d+)/',
        views.UpdateQuestionView.as_view(),
        name='qa_update_question'),

    re_path('answer/(?P<question_id>\d+)/',
        views.CreateAnswerView.as_view(), name='qa_create_answer'),

    re_path('answer/edit/(?P<answer_id>\d+)/',
        views.UpdateAnswerView.as_view(), name='qa_update_answer'),

    re_path('vote/question/(?P<object_id>\d+)/',
        views.QuestionVoteView.as_view(), name='qa_question_vote'),

    re_path('vote/answer/(?P<object_id>\d+)/',
        views.AnswerVoteView.as_view(), name='qa_answer_vote'),

    re_path('comment-answer/(?P<answer_id>\d+)/',
        views.CreateAnswerCommentView.as_view(),
        name='qa_create_answer_comment'),

    re_path('comment-question/(?P<question_id>\d+)/',
        views.CreateQuestionCommentView.as_view(),
        name='qa_create_question_comment'),

    re_path('comment-question/edit/(?P<comment_id>\d+)/',
        views.UpdateQuestionCommentView.as_view(),
        name='qa_update_question_comment'),

    re_path('comment-answer/edit/(?P<comment_id>\d+)/',
        views.UpdateAnswerCommentView.as_view(),
        name='qa_update_answer_comment'),

    re_path('search/', views.QuestionsSearchView.as_view(), name='qa_search'),

    re_path('tag/(?P<tag>[-\w]+)/',
        views.QuestionsByTagView.as_view(), name='qa_tag'),

    re_path('profile/(?P<user_id>\d+)/', views.profile, name='qa_profile'),

    re_path('markdown/', include('markdownx.urls')),

    re_path('hitcount/', include('hitcount.urls', namespace='hitcount')),

]
