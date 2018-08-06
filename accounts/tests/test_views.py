from django.test import TestCase,Client
from django.shortcuts import reverse
from accounts.models import UserProfile
from django.contrib.auth.models import User
# Create your tests here.

class TestViews(TestCase):
	def setUp(self):
		self.client = Client()
		self.user_object = User.objects.create(username="testing",
											   password="testing")
		self.client.force_login(self.user_object)

	def test_views_200(self):
		print("running stuff")
		pathnames = ["home","view_profile","change_profile_picture",
					"registersucess","signup","view_people",
					"password_reset_complete","password_reset_done",
					"reset_password","change_password","edit_profile"]
		for pathname in pathnames:
			url = reverse(pathname)
			response = self.client.get(url)
			self.assertEqual(response.status_code,200)
