from django.test import TestCase
from django.shortcuts import reverse
from project.models import ProjectDetail
from project.tests import TestLoginRequired
from project.issueSolution.models import Issue,IssueComment,Solution,SolutionComment
from django.contrib.auth.models import User

testDebug = True
# Create your tests here.

class TestProjectViewsLoginRequired(TestLoginRequired):
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
		self.issue_object = Issue.objects.create(user=self.user_object,
												project=self.project_object,
												title="testing",
												description="testing")
		if testDebug:
			print("issue_object created")
		self.solution_object = Solution.objects.create(issue=self.issue_object,
														user=self.user_object,
														title="testing",
														description="testing")
		if testDebug:
			print("solution_object created")
		self.issueComment_object = IssueComment.objects.create(issue=self.issue_object,
																user=self.user_object,
																comment="testing")

		if testDebug:
			print("issueComment_object created")
		self.solutionComment_object = SolutionComment.objects.create(solution=self.solution_object,
														user=self.user_object,
														comment="testing")
		if testDebug:
			print("solutionComment_object created")
		self.pathnames_args = {"deleteIssueSolution":["issue",self.solution_object.id],"projectIssues":[self.project_object.id,"open"],
			"projectSolutions":[self.project_object.id,"open"],"commentIssueSolution":[self.project_object.id,"issue",self.issue_object.id],
			"editIssueSolution":[self.project_object.id,"issue",self.issue_object.id],"createIssueSolution":[self.project_object.id,"issue"],
			"viewIssueSolution":[self.project_object.id,"issue",self.issue_object.id],"changeStatusIssueSolution":[self.project_object.id,"issue",self.issue_object.id,"open"]}