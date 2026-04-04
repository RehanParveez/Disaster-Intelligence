from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from incidents.models import Incident
from accounts.models import Profile

# Create your tests here.
class ParentTest(TestCase):
  def setUp(self):
    User = get_user_model()
    self.client = APIClient()
    self.user = User.objects.create_user(username = 'user1', password = 'user1123456', email = 'user1@gmail.com')
    self.admin = User.objects.create_user(username = 'admin', password = 'admin123456', email = 'admin@gmail.com', is_admin=True)
    Profile.objects.create(user=self.user, control = 'responder')
    Profile.objects.create(user=self.admin, control = 'authority')
    self.incident = Incident.objects.create(title = 'incident test', description = 'description test',
      location = 'Bahawalpur', severity=2, created_by=self.user, status = 'active')
    
  def auth_user(self, user):
    self.client.force_authenticate(user=user)

class AuthTest(ParentTest):
  def test_check(self):
    self.assertEqual(self.user.username, 'user1')
    self.assertEqual(self.admin.username, 'admin')
        