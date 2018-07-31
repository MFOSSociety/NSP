from django.test import TestCase
from django.shortcuts import reverse
import nsp.tests as tests
from django.contrib.auth.models import User
# Create your tests here.

class TestNspmessageViewsLoginRequired(tests.TestLoginRequired):
	def setUp(self):
		self.user_object = User.objects.create(username="testing",
												password="testing")
		self.user_object2 = User.objects.create(username="testing2",
												password="testing2")
		if tests.testDebug:
			print("user_object created")
		self.pathnames_args = {"chat":[],
							  "chat_friend":[self.user_object2.id],
							  "new_message":[self.user_object2.id]}