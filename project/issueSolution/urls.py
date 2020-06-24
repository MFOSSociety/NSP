from django.urls import path
from . import views
urlpatterns = [
    path("<type_>/<ID>/vote",views.voteSolution,name="voteSolution"),
    path('delete/<type_>/<ID>', views.deleteIssueSolution, name="deleteIssueSolution"),
    path('<ID>/issues/<status>', views.projectIssues, name='projectIssues'),
    path('<ID>/solutions/<status>', views.projectSolutions, name='projectSolutions'),
    path('project/<projectID>/<type_>/<ID>/comment', views.commentIssueSolution, name='commentIssueSolution'),
    path('project/<projectID>/<type_>/<ID>/comment/edit/', views.editCommentIssueSolution,
         name='editCommentIssueSolution'),
    path('<projectID>/<type_>/<ID>/edit', views.editIssueSolution, name='editIssueSolution'),
    path('<projectID>/<type_>/create', views.createIssueSolution, name='createIssueSolution'),
    path('<projectID>/<type_>/<ID>', views.viewIssueSolution, name='viewIssueSolution'),
    path('<projectID>/<type_>/<ID>/<status>', views.changeStatusIssueSolution,
         name='changeStatusIssueSolution'),
]