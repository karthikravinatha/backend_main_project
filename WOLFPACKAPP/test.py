from django.test import TestCase,SimpleTestCase
from django.urls import reverse, resolve
from WOLFPACKAPP.views import add_user, project_add,update_user,get_user,\
    project_add,project_update,project_delete,get_project_and_issues,\
        sprint_add,sprint_delete,add_watcher,add_comment,update_comment,delete_comment
from WOLFPACKAPP.models import Users

class BaseTest(SimpleTestCase):
    def test_user_add(self):
        url = reverse('user-add')
        self.assertEqual(resolve(url).func,add_user)

    def test_user_update(self):
        url = reverse('user-update')
        self.assertEqual(resolve(url).func,update_user)

    def test_user_get(self):
        url = reverse('user-get')
        self.assertEqual(resolve(url).func,get_user)

    def test_project_add(self):
        url = reverse('project-add')
        self.assertEqual(resolve(url).func,project_add)

    def test_project_update(self):
        url = reverse('project-update')
        self.assertEqual(resolve(url).func,project_update)

    def test_project_delete(self):
        url = reverse('project-delete')
        self.assertEqual(resolve(url).func,project_delete)

    def test_project_getlist(self):
        url = reverse('project-getlist')
        self.assertEqual(resolve(url).func,get_project_and_issues)    

    def test_sprint_add(self):
        url = reverse('sprint-add')
        self.assertEqual(resolve(url).func,sprint_add)

    def test_sprint_delete(self):
        url = reverse('sprint-delete')
        self.assertEqual(resolve(url).func,sprint_delete)

    def test_watchers_add(self):
        url = reverse('add-watchers')
        self.assertEqual(resolve(url).func,add_watcher)

    def test_comment_add(self):
        url = reverse('comment-add')
        self.assertEqual(resolve(url).func,add_comment)

    def test_comment_update(self):
        url = reverse('comment-update')
        self.assertEqual(resolve(url).func,update_comment)

    def test_comment_delete(self):
        url = reverse('comment-delete')
        self.assertEqual(resolve(url).func,delete_comment)
