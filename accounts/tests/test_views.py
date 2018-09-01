from django.test import TestCase,Client
from django.shortcuts import reverse
from accounts.models import UserProfile,Skill
from django.contrib.auth.models import User
# Create your tests here.

class TestViews(TestCase):
	def setUp(self):
		self.client = Client()
		self.user_object = User.objects.create(username="testing",
											   password="testing")
		self.user_object2 = User.objects.create(username="testing2",
											   password="testing2")
		self.UserProfile_object = UserProfile.objects.get(user=self.user_object)
		self.skill = Skill.objects.create(user=self.user_object,
										  skill_name="testing")
		self.client.force_login(self.user_object)

	def test_views_200(self):
		print("running stuff")
		pathnames = ["home","view_profile","change_profile_picture",
					"registersucess","signup","view_people"
					,"change_password","edit_profile"]
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

	def test_change_profile_picture_post(self):
		url = reverse("change_profile_picture")
		data_valid = {"photo":"http://thensp.pythonanywhere.com/static/accounts/img/nsp_profile_default.jpg"}
		response_valid = self.client.post(url,data=data_valid)
		self.assertEqual(response_valid.status_code,302)
		self.assertEqual(response_valid.url,reverse("change_profile_picture"))

	def test_delete_skill_view(self):
		url = reverse("deleteskill",args=[self.skill.id])
		response = self.client.get(url)
		self.assertEqual(response.status_code,302)
		self.assertEqual(response.url,reverse("view_profile"))
		response_afterDeleted = self.client.get(url)
		self.assertEqual(response_afterDeleted.status_code,404)

	def test_add_skill_view(self):
		url = reverse("addskill")
		response_get = self.client.get(url)
		self.assertEqual(response_get.status_code,200)
		valid_data = {"skill":"testing"}
		response_post = self.client.post(url,data=valid_data)
		self.assertEqual(response_post.status_code,200)
		self.assertContains(response_post,"Success!")

	def test_EditUserProfileView_get(self):
		url_access = reverse("EditDetails",args=[self.user_object.id])
		url_noAccess = reverse("EditDetails",args=[self.user_object2.id])
		url_invalid = reverse("EditDetails",args=[100])
		response_access_get = self.client.get(url_access)
		self.assertEqual(response_access_get.status_code,200)
		response_noAcess_get = self.client.get(url_noAccess)
		response_invalid_get = self.client.get(url_invalid)
		self.assertEqual(response_noAcess_get.status_code,404)
		self.assertEqual(response_invalid_get.status_code,404)

	def test_EditUserProfileView_post(self):
		url_access = reverse("EditDetails",args=[self.user_object.id])
		valid_data = {
			"branch":"CSE",
			"year":"1",
			"stream":"BCA",
			"gender":"Male",
			"position":"Student",
			"bio":"testing"
		}
		response_access_get = self.client.post(url_access,valid_data)
		self.assertEqual(response_access_get.status_code,302)
		self.assertEqual(response_access_get.url,reverse("view_profile"))