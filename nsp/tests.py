from django.test import TestCase
from django.shortcuts import reverse

testDebug = True

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
