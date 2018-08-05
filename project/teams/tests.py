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
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		self.team_object = Team.objects.create(project=self.project_object,
											   description="testing")
		self.team_object2 = Team.objects.create(project=self.project_object,
											   description="testing")

	def test_delete_view_get(self):
		self.client.force_login(self.user_object)
		url = reverse("deleteTeam",args=[self.team_object.id])
		response = self.client.get(url)
		print(response)
		self.assertEquals(response.status_code, 302)
		response2 = self.client.get(url)
		self.assertEquals(response2.status_code, 404)
		url2 = reverse("deleteTeam",args=[self.team_object2.id])
		response3 = self.client.get(url2,follow=True)
		self.assertEquals(response3.status_code, 200)
		self.assertEquals(response.url, reverse("showTeams",args=[self.project_object.id]))
		self.assertEquals(response.resolver_match.func,views.deleteTeam)

class TestShowTeamsView(TestCase):
	def setUp(self):
		self.client = Client()
		self.user_object = User.objects.create_superuser(
			'testing',
			'testing@example.com',
			'testing',
		)
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		self.client.force_login(self.user_object)
	def test_showTeams_view(self):
		url_valid = reverse("showTeams",args=[self.project_object.id])
		url_invalid = reverse("showTeams",args=[100])
		response_valid = self.client.get(url_valid)
		response_invalid = self.client.get(url_invalid)
		self.assertEquals(response_valid.status_code, 200)
		self.assertEquals(response_invalid.status_code, 404)

class TestShowTeamView(TestCase):
	def setUp(self):
		self.client = Client()
		self.user_object = User.objects.create_superuser(
			'testing',
			'testing@example.com',
			'testing',
		)
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		self.team_object = Team.objects.create(project=self.project_object,
											   description="testing")
		self.client.force_login(self.user_object)
	def test_showTeam_view(self):
		url_valid = reverse("showTeam",args=[self.team_object.id])
		url_invalid = reverse("showTeam",args=[100])
		response_valid = self.client.get(url_valid)
		response_invalid = self.client.get(url_invalid)
		self.assertEquals(response_valid.status_code, 200)
		self.assertEquals(response_invalid.status_code, 404)

class TestCreateTeamView(TestCase):
	def setUp(self):
		self.client = Client()
		self.user_object = User.objects.create_superuser(
			'testing',
			'testing@example.com',
			'testing',
		)
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		self.team_object = Team.objects.create(project=self.project_object,
											   description="testing")
		self.client.force_login(self.user_object)
	def test_createTeam_view(self):
		url_valid = reverse("createTeam",args=[self.project_object.id])
		url_invalid = reverse("createTeam",args=[100])
		response_valid = self.client.get(url_valid)
		response_invalid = self.client.get(url_invalid)
		self.assertEquals(response_valid.status_code, 200)
		self.assertEquals(response_invalid.status_code, 404)
		self.assertContains(response_valid,"</form>")
