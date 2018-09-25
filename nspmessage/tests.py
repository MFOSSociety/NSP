from django.test import TestCase
from django.shortcuts import reverse
import nsp.tests as tests
from django.contrib.auth.models import User
from accounts.models import Follow
# Create your tests here.

class TestViews(tests.TestLoginRequired):
	def setUp(self):
		self.user_object = User.objects.create(username="testing",
												password="testing")
		self.user_object2 = User.objects.create(username="testing2",
												password="testing2")
		self.user_object3 = User.objects.create(username="testing3",
												password="testing3")
		self.follow_object = Follow.objects.create(follower=self.user_object,
												   following=self.user_object2)
		self.follow_object2 = Follow.objects.create(follower=self.user_object2,
												   following=self.user_object)
		if tests.testDebug:
			print("user_object created")
		self.pathnames_args = {"chat":[],"chat_friend":[self.user_object2.username],
							   "get_messages_api":[self.user_object2.username]}
	def test_views_200(self):
		self.client.force_login(self.user_object)
		for pathname,args in self.pathnames_args.items():
			response = self.client.get(reverse(pathname,args=args))
			self.assertEqual(response.status_code,200)
	def test_chat_friend_view(self):
		self.client.force_login(self.user_object)
		username_statuscode = {self.user_object2:200,
						   self.user_object3:404,
						   self.user_object:404}
		for username,status_code in username_statuscode.items():
			args = [username]
			url = reverse("chat_friend",args=args)
			response = self.client.get(url)
			self.assertEqual(response.status_code,status_code)
