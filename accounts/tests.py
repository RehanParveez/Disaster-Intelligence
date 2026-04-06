from django.test import TransactionTestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from incidents.models import Incident
from accounts.models import Profile

# Create your tests here.
class ParentTest(TransactionTestCase): 
  def setUp(self):
    User = get_user_model()
    self.client = APIClient()
    self.user, _ = User.objects.get_or_create(username = 'user1', defaults={'email': 'user1@gmail.com'})
    if _: self.user.set_password('user112312'); self.user.save()
    self.admin, _ = User.objects.get_or_create(username = 'admin', defaults={'email': 'admin@gmail.com', 'is_admin': True})
    if _: self.admin.set_password('admin12312'); self.admin.save()

    Profile.objects.get_or_create(user=self.user, defaults={'control': 'responder'})
    Profile.objects.get_or_create(user=self.admin, defaults={'control': 'authority'})
    self.incident = Incident.objects.create(title = 'incident test', location = 'Bahawalpur', severity=2, created_by=self.user, status = 'active')
    
  def auth_user(self, user):
    self.client.force_authenticate(user=user)

class AuthTest(ParentTest):
  def test_check(self):
    self.assertEqual(self.user.username, 'user1')
    self.assertEqual(self.admin.username, 'admin')
        