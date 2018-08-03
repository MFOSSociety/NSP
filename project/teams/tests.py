from django.test import TestCase
from project.models import ProjectDetail
from .models import Team
from django.contrib.auth.models import User
import nsp.tests as tests

# Create your tests here.

class TestTeamsViewsLoginRequired(tests.TestLoginRequired):
	def setUp(self):
		self.user_object = User.objects.create(username="testing",
												password="testing")
		if tests.testDebug:
			print("user_object created")
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		if tests.testDebug:
			print("project_object created")
		self.team_object = Team.objects.create(project=self.project_object,
											   description="testing")
		if tests.testDebug:
			print("team_object created")
		self.pathnames_args = {"createTeam":[self.project_object.id],
							   "deleteTeam":[self.team_object.id],
							   "showTeams":[self.project_object.id]
																}