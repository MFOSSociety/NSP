from django.test import TestCase
from django.shortcuts import reverse
from project.models import ProjectDetail,ProjectPeopleInterested
from django.contrib.auth.models import User

testDebug = True
# Create your tests here.

class TestProjectLoginRequired(TestCase):
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
			"add_interested":[self.project_object.id],"remove_interested":["1"],
			"project_edit":[self.project_object.id],"delete_project":[self.project_object.id]}
	def test_call_view_denies_anonymous(self):
		if testDebug:
			print("test_call_view_denies_anonymous")
		for pathname,args in self.pathnames_args.items():
			response = self.client.get(reverse(pathname,args=args), follow=True)
			result = self.assertRedirects(response,reverse("user_login") + "?next=" + reverse(pathname,args=args))
			if testDebug:
				print("Tested {} - {}".format(pathname,result))
