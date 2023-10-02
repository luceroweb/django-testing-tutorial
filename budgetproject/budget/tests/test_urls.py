"""Testing URLs"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from budget.views import project_list, project_detail, ProjectCreateView


class TestUrls(SimpleTestCase):
    """Testing urls to confirm that they return the expected views"""

    def test_list_url_resolves(self):
        """Testing that the url returns project_list"""
        url = reverse('list')
        self.assertEqual(resolve(url).func, project_list)

    def test_add_url_resolves(self):
        """Testing that add url returns ProjectCreateView"""
        url = reverse('add')
        self.assertEqual(resolve(url).func.view_class, ProjectCreateView)

    def test_detail_url_resolves(self):
        """Testing that the detail url returns project_list"""
        url = reverse('detail', args=['some-slug'])
        self.assertEqual(resolve(url).func, project_detail)
