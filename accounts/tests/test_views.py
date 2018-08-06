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

	def test_follow_views_302(self):
		urls = [[reverse("follow_user",args=[self.user_object.id]),302],
				[reverse("follow_user",args=[100]),404],
				[reverse("unfollow_user",args=[self.user_object.id]),302],
				[reverse("unfollow_user",args=[100]),404]]
		for url,status_code in urls:
			response = self.client.get(url)
			self.assertEqual(response.status_code,status_code)
			if status_code == 302:
				self.assertEqual(response.url,reverse("view_friend",args=[self.user_object.username]))

	def test_edit_profile_view_post(self):
		url = reverse("edit_profile")
		data_valid = {"first_name":"testing",
				"last_name":"testing",
				"email":"testing@gmail.com"}
		response_valid = self.client.post(url,data=data_valid)
		self.assertEqual(response_valid.url + "/",reverse("view_profile"))
