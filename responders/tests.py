from responders.services import register_respon, set_avail
from responders.models import Capability, Responder
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from accounts.tests import ParentTest

class ResponderServiceTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.skill = Capability.objects.create(name='Rescue')

  def test_reg_respon(self):
    data = {'max_load': 5, 'skills': [self.skill.id]}
    respon = register_respon(self.user, data)
    self.assertEqual(respon.user, self.user)
    self.assertEqual(respon.max_load, 5)
    self.assertIn(self.skill, respon.skills.all())

  def test_respon_exists(self):
    register_respon(self.user, {})
    with self.assertRaises(ValidationError):
      register_respon(self.user, {})

  def test_set_avail_succ(self):
    respon = register_respon(self.user, {})
    start = timezone.now()
    end = start + timedelta(hours=2)
    shift = set_avail(respon.id, {'start_time': start, 'end_time': end})
    self.assertEqual(shift.responder, respon)

  def test_set_avail(self):
    respon = register_respon(self.user, {})
    start = timezone.now()
    end = start  
    with self.assertRaises(ValidationError):
      set_avail(respon.id, {'start_time': start, 'end_time': end})
          
  def test_set_avail_cover(self):
    respon = register_respon(self.user, {})
    start = timezone.now()
    end = start + timedelta(hours=2)
    set_avail(respon.id, {'start_time': start, 'end_time': end})
    with self.assertRaises(ValidationError):
      set_avail(respon.id, {'start_time': start + timedelta(minutes=50), 'end_time': end + timedelta(hours=2)})
      
class ResponderViewTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.skill = Capability.objects.create(name = 'Rescue')

  def test_reg_respon(self):
    self.auth_user(self.user)
    url = '/responders/responder/register/'
    data = {'max_load': 3, 'skills': [self.skill.id]}
    response = self.client.post(url, data, format = 'json')
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Responder.objects.count(), 1)

  def test_set_avail(self):
    self.auth_user(self.user)
    respon = Responder.objects.create(user=self.user)
    url = f'/responders/responder/{respon.id}/set_availability/'
    
    start = timezone.now()
    end = start + timedelta(hours=2)
    data = {'start_time': start.isoformat(), 'end_time': end.isoformat()}
    response = self.client.post(url, data, format = 'json')
    self.assertEqual(response.status_code, 201)

  def test_add_skill(self):
    self.auth_user(self.user)
    respon = Responder.objects.create(user=self.user)
    url = f'/responders/responder/{respon.id}/skill/'
    data = {'skill_id': self.skill.id}
    resp = self.client.post(url, data, format = 'json')
    self.assertEqual(resp.status_code, 200)
    self.assertIn(self.skill, respon.skills.all())
