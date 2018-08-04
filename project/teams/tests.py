from django.test import TestCase,Client
from django.shortcuts import reverse
from project.models import ProjectDetail
from .models import Team
from django.contrib.auth.models import User
from nsp.tests import TestLoginRequired
from . import views
# Create your tests here.

class TestTeamsViewsLoginRequired(TestLoginRequired):
	def setUp(self):
		self.user_object = User.objects.create(username="testing",
												password="testing")
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		self.team_object = Team.objects.create(project=self.project_object,
											   description="testing")

		self.pathnames_args = {"createTeam":[self.project_object.id],
							   "deleteTeam":[self.team_object.id],
							   "showTeams":[self.project_object.id]
																}

class TestDeleteTeamView(TestCase):
	def setUp(self):
		self.client = Client()
		self.user_object = User.objects.create_superuser(
			'testing',
			'testing@example.com',
			'testing',
		)
		self.user_object.set_password("testing")
		self.user_object.save()	
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		self.team_object = Team.objects.create(project=self.project_object,
											   description="testing")

	def test_delete_view_get(self):
		self.client.force_login(self.user_object)
		url = reverse("deleteTeam",args=[self.team_object.id])
		response = self.client.get(url)
		print(response)
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse("showTeams",args=[self.project_object.id]))
		self.assertEquals(response.resolver_match.func,views.deleteTeam)