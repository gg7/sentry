from __future__ import absolute_import

from django.template import Context, Template
from mock import Mock

from sentry.plugins import plugins, Plugin2
from sentry.testutils import TestCase


class SamplePlugin(Plugin2):
    def get_actions(self, request, group):
        return [('Example Action', 'http://example.com?id=%s' % (group.id,))]

    def is_enabled(self, project=None):
        return True


class PluginTestCase(TestCase):
    plugin = None

    def setUp(self):
        super(PluginTestCase, self).setUp()
        plugins.register(self.plugin)
        self.addCleanup(plugins.unregister, self.plugin)


class GetActionsTest(PluginTestCase):
    plugin = SamplePlugin

    TEMPLATE = Template("""
        {% load sentry_plugins %}
        {% for k, v in group|get_actions:request %}
            <span>{{ k }} - {{ v }}</span>
        {% endfor %}
    """)

    def test_includes_v2_plugins(self):
        group = self.create_group()

        result = self.TEMPLATE.render(Context({
            'request': Mock(),
            'group': group,
        }))

        assert '<span>Example Action - http://example.com?id=%s</span>' % (group.id,) in result