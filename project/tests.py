from django.test import TestCase
from django.shortcuts import reverse
from project.models import ProjectDetail,ProjectPeopleInterested
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import authenticate

testDebug = True
# Create your tests here.

class TestLoginRequired(TestCase):
	def setUp(self):
		self.pathnames_args = {}
	def test_call_view_denies_anonymous(self):
		if testDebug:
			print("test_call_view_denies_anonymous")
		for pathname,args in self.pathnames_args.items():
			response = self.client.get(reverse(pathname,args=args), follow=True)
			result = self.assertRedirects(response,reverse("user_login") + "?next=" + reverse(pathname,args=args))
			if testDebug:
				print("Tested {} - {}".format(pathname,result))

class TestProjectViewsLoginRequired(TestCase):
	def setUp(self):
		self.user_object = User.objects.create(username="testing",
												password="testing")
		if testDebug:
			print("user_object created")
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		if testDebug:
			print("project_object created")
		self.interested_object = ProjectPeopleInterested.objects.create(user=self.user_object,
																		project=self.project_object)
		if testDebug:
			print("interested_object created")
		self.pathnames_args = {"start_project":[],"project_list_view":[],
			"interested_list":[self.project_object.id],"view_project_detail":[self.project_object.id],
			"add_interested":[self.project_object.id],"remove_interested":[self.interested_object.id],
			"project_edit":[self.project_object.id],"delete_project":[self.project_object.id]}
	def test_call_view_denies_anonymous(self):
		if testDebug:
			print("test_call_view_denies_anonymous")
		for pathname,args in self.pathnames_args.items():
			response = self.client.get(reverse(pathname,args=args), follow=True)
			result = self.assertRedirects(response,reverse("user_login") + "?next=" + reverse(pathname,args=args))
			if testDebug:
				print("Tested {} - {}".format(pathname,result))

"""class Test_delete_project_view(TestCase):
	def setUp(self):
		self.c = Client()
		self.user_object = User.objects.create(username="testing",
												password="testing")
		if testDebug:
			print("user_object created")
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		if testDebug:
			print("project_object created")
			print(self.project_object)	
	def test_get_method(self):
		self.login = authenticate(username=self.user_object.username,password=self.user_object.password) 
		self.assertTrue(self.login)
		response = self.c.get(reverse("delete_project",args=[self.project_object.id]))
		print(response)
		self.assertEqual(response.status_code, 200)"""