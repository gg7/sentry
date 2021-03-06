from __future__ import absolute_import

from django.core.urlresolvers import reverse
from exam import fixture

from sentry.testutils import TestCase


class ProjectReleaseTrackingTest(TestCase):
    def setUp(self):
        super(ProjectReleaseTrackingTest, self).setUp()
        self.organization = self.create_organization()
        self.team = self.create_team(organization=self.organization)
        self.project = self.create_project(team=self.team)

    @fixture
    def path(self):
        return reverse('sentry-project-release-tracking', args=[
            self.organization.slug, self.project.slug,
        ])

    def test_renders_with_context(self):
        self.login_as(self.organization.owner)
        resp = self.client.get(self.path)
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, 'sentry/project-release-tracking.html')
        assert resp.context['project'] == self.project
