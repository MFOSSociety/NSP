from django.urls import path
from . import views
urlpatterns = [
    path('delete/<type_>/<ID>', views.deleteIssueSolution, name="deleteIssueSolution"),
    path('<ID>/issues/<status>', views.projectIssues, name='projectIssues'),
    path('<ID>/solutions/<status>', views.projectSolutions, name='projectSolutions'),
    path('<projectID>/<type_>/<ID>/edit', views.editIssueSolution, name='editIssueSolution'),
    path('<projectID>/<type_>/create', views.createIssueSolution, name='createIssueSolution'),
    path('<projectID>/<type_>/<ID>', views.viewIssueSolution, name='viewIssueSolution'),
    path('<projectID>/<type_>/<ID>/<status>', views.changeStatusIssueSolution,
         name='changeStatusIssueSolution'),
]