from django.test import TestCase
from django.shortcuts import reverse
from project.models import ProjectDetail
from nsp.tests import TestLoginRequired
from project.issueSolution.models import Issue,IssueComment,Solution,SolutionComment
from django.contrib.auth.models import User

# Create your tests here.

class TestIssueSolutionViewsLoginRequired(TestLoginRequired):
	def setUp(self):
		self.user_object = User.objects.create(username="testing",
												password="testing")
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		self.issue_object = Issue.objects.create(user=self.user_object,
												project=self.project_object,
												title="testing",
												description="testing")
		self.solution_object = Solution.objects.create(issue=self.issue_object,
														user=self.user_object,
														title="testing",
														description="testing")
		self.issueComment_object = IssueComment.objects.create(issue=self.issue_object,
																user=self.user_object,
																comment="testing")
		self.solutionComment_object = SolutionComment.objects.create(solution=self.solution_object,
														user=self.user_object,
														comment="testing")
		################# args for paths
		deleteIssueSolution_args = ["issue",self.solution_object.id]
		projectIssues_args = [self.project_object.id,"open"]
		projectSolutions_args = [self.project_object.id,"open"]
		commentIssueSolution_args = [self.project_object.id,"issue",self.issue_object.id]
		editIssueSolution_args = [self.project_object.id,"issue",self.issue_object.id]
		createIssueSolution_args = [self.project_object.id,"issue"]
		viewIssueSolution_args = [self.project_object.id,"issue",self.issue_object.id]
		changeStatusIssueSolution_args = [self.project_object.id,"issue",self.issue_object.id,"open"]
		######
		self.pathnames_args = {"deleteIssueSolution":deleteIssueSolution_args,"projectIssues":projectIssues_args,
								"projectSolutions":projectSolutions_args,"commentIssueSolution":commentIssueSolution_args,
								"editIssueSolution":editIssueSolution_args,"createIssueSolution":createIssueSolution_args,
								"changeStatusIssueSolution":[self.project_object.id,"issue",self.issue_object.id,"open"],
								"viewIssueSolution":viewIssueSolution_args}

class TestViews(TestCase):
	def setUp(self):
		self.user_object = User.objects.create(username="testing",
												password="testing")
		self.user_object2 = User.objects.create(username="testing2",
												password="testing2")
		self.project_object = ProjectDetail.objects.create(project_name="testing",
															initiated_by=self.user_object,
															mentor_name="testing",
															branch="testing",
															description="testing")
		self.issue_object = Issue.objects.create(user=self.user_object,
												project=self.project_object,
												title="testing",
												description="testing")
		self.issue_object2 = Issue.objects.create(user=self.user_object2,
												project=self.project_object,
												title="testing2",
												description="testing2")
		self.solution_object = Solution.objects.create(issue=self.issue_object,
														user=self.user_object,
														title="testing",
														description="testing")
		self.issueComment_object = IssueComment.objects.create(issue=self.issue_object,
																user=self.user_object,
																comment="testing")

		self.solutionComment_object = SolutionComment.objects.create(solution=self.solution_object,
														user=self.user_object,
														comment="testing")
		self.client.force_login(self.user_object)
	def test_views_200(self):
		pathnames_args = {

			"projectIssues":[[self.project_object.id,"open"],
							[self.project_object.id,"closed"],
							[self.project_object.id,"all"]],
			"projectSolutions":[[self.project_object.id,"open"],
							[self.project_object.id,"all"],
							[self.project_object.id,"accepted"],
							[self.project_object.id,"notaccepted"]],
			"editIssueSolution":[[self.project_object.id,"issue",self.issue_object.id],
								[self.project_object.id,"solution",self.solution_object.id]],
			"createIssueSolution":[[self.project_object.id,"issue"],
									[self.project_object.id,"solution"]],
			"viewIssueSolution":[[self.project_object.id,"issue",self.issue_object.id],
								[self.project_object.id,"solution",self.solution_object.id]]
		}
		for pathname,argsList in pathnames_args.items():
			for args in argsList:
				url = reverse(pathname,args=args)
				response = self.client.get(url)
				self.assertEqual(response.status_code,200)

	def test_editIssueSolution_get(self):
		url_noAccess = reverse("editIssueSolution",args=[self.project_object.id,
												"issue",self.issue_object2.id])
		response_noAccess = self.client.get(url_noAccess)
		self.assertEqual(response_noAccess.status_code,302)
		url_access = reverse("editIssueSolution",args=[self.project_object.id,
												"issue",self.issue_object.id])
		response2_access = self.client.get(url_access)
		self.assertEqual(response2_access.status_code,200)
		url_invalid = reverse("editIssueSolution",args=[100,
												"issue",self.issue_object2.id])
		response_404 = self.client.get(url_invalid)
		self.assertEqual(response_404.status_code,404)

	def test_changeStatusIssueSolution(self):
		argsList = [[self.project_object.id,"issue",self.issue_object.id,"closed"],
				[self.project_object.id,"issue",self.issue_object.id,"open"],
				[self.project_object.id,"solution",self.solution_object.id,"accepted"],
				[self.project_object.id,"solution",self.solution_object.id,"notaccepted"],
				[self.project_object.id,"solution",self.solution_object.id,"open"]
		]
		for args in argsList:
			url = reverse("changeStatusIssueSolution",args=args)
			response = self.client.post(url)
			self.assertEqual(response.status_code,302)
			self.assertEqual(response.url,reverse("viewIssueSolution",args=args[:3]))

		#Tests if user can edit an issue even if not created by the user
		self.client.force_login(self.user_object2)
		for args in argsList:
			url = reverse("changeStatusIssueSolution",args=args)
			response = self.client.get(url)
			self.assertEqual(response.status_code,302)
			self.assertEqual(response.url,reverse("viewIssueSolution",args=args[:3]))

		self.client.force_login(self.user_object)

	def test_commentIssueSolution(self):
		argsList = [[self.project_object.id,"issue",self.issue_object.id],
					[self.project_object.id,"solution",self.issue_object.id]
		]
		for args in argsList:
			url = reverse("commentIssueSolution",args=args)
			response = self.client.get(url)
			self.assertEqual(response.status_code,302)
			self.assertEqual(response.url,reverse("viewIssueSolution",args=args))
		args_invalid = [[100,"issue",self.issue_object.id],
						[100,"dsadsasd",self.issue_object.id],
						[100,"solution",312],
						[100,"solution",self.issue_object.id]]
		for args in args_invalid:
			url = reverse("commentIssueSolution",args=args)
			valid_data = {"comment":"testing"}
			response = self.client.post(url,valid_data)
			self.assertEqual(response.status_code,404)

	def test_createIssueSolution_issue(self):
		create_issue_url = reverse("createIssueSolution",args=[self.project_object.id,"issue"])
		issue_valid_data = {"title":"testing","description":"testing"}
		response_issue = self.client.post(create_issue_url,issue_valid_data)
		self.assertEqual(response_issue.status_code,302)
		issue_object3 = Issue.objects.get(pk=3)
		self.assertEqual(response_issue.url,reverse("viewIssueSolution",args=[self.project_object.id,
																		      "issue",issue_object3.id]))
	def test_createIssueSolution_post(self):
		create_solution_url = reverse("createIssueSolution",args=[self.project_object.id,"solution"])
		solution_valid_data = {"title":"testing","description":"testing","value":"{}".format(self.issue_object.id)}
		response_issue = self.client.post(create_solution_url,solution_valid_data)
		self.assertEqual(response_issue.status_code,302)
		solution_object2 = Issue.objects.get(pk=2)
		self.assertEqual(response_issue.url,reverse("viewIssueSolution",args=[self.project_object.id,
																		      "solution",solution_object2.id]))