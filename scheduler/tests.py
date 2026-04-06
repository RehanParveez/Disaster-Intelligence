from accounts.tests import ParentTest
from resources.models import Resource, Unit, Availability
from responders.models import Responder, Load
from django.urls import reverse
from scheduler.models import Cycle, IncidentList, DecisionRecord
from execution.models import Execution
from scheduler.services import run_cycle

class SchedulerTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.resource = Resource.objects.create(name = 'Ambulance')
    self.unit = Unit.objects.create(kind=self.resource, identifier = 'DAC-05', location=self.incident.location)
    self.avail = Availability.objects.create(res_kind=self.resource, location=self.incident.location, total_units=1, avail_units=1)
    self.responder = Responder.objects.create(user=self.user, max_load=5)
    self.load = Load.objects.create(responder=self.responder, incident=self.incident, load_count=0)

  def test_run_cycle(self):
    self.auth_user(self.admin)
    url = reverse('scheduler-run')
    
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    cycle = Cycle.objects.get(id=resp.data['cycle_id'])
    self.assertEqual(cycle.total_incids, 1)
    self.assertEqual(cycle.decis_made, 1)
    list_entry = IncidentList.objects.get(incident=self.incident)
    self.assertEqual(list_entry.prior, 2)
    decis = DecisionRecord.objects.filter(cycle=cycle)
    decis = decis.first()
    
    self.assertIsNotNone(decis)
    self.assertEqual(decis.incident, self.incident)
    exec_exists = Execution.objects.filter(decision=decis)
    exec_exists = exec_exists.exists()
    self.assertTrue(exec_exists, 'the sched has failed')

  def test_scheduler_perm(self):
    self.auth_user(self.user) 
    url = reverse('scheduler-run')
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 403)

  def test_incid_list(self):
    run_cycle()
    self.auth_user(self.admin)
    
    url = reverse('scheduler-List')
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(len(resp.data) > 0)
    self.assertEqual(resp.data[0]['incident'], self.incident.id)
