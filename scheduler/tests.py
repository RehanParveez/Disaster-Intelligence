from accounts.tests import ParentTest
from resources.models import Resource, Unit, Availability
from responders.models import Responder, Load
from django.urls import reverse
from incidents.models import Incident
from scheduler.services import run_cycle
from scheduler.models import DecisionRecord, Cycle
from django.utils import timezone
from datetime import timedelta
from responders.models import Shift
from execution.models import Execution, FailureRecord


class SchedulerTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.resource = Resource.objects.create(name = 'fire truck')
    self.unit = Unit.objects.create(kind=self.resource, identifier = 'FTT-02', location=self.incident.location)
    self.avail = Availability.objects.create(res_kind=self.resource, location=self.incident.location, total_units=1, avail_units=1)
    self.responder = Responder.objects.create(user=self.admin, max_load=5)
    self.load = Load.objects.create(responder=self.responder, incident=self.incident, load_count=0)

    self.run_url = reverse('scheduler-run')
    self.list_url = reverse('scheduler-List')
    self.latest_url = reverse('scheduler-latest')

  def test_scarcity(self):
    low_incid = Incident.objects.create(title = 'Small Fire', location = 'Sector-A Multan', severity=10, prior=10, status = 'active', created_by=self.admin)
    Availability.objects.create(res_kind=self.resource, location = 'Sector-A Multan', total_units=10, avail_units=1)
    Unit.objects.create(kind=self.resource, identifier = 'FT-01', location = 'Sector-A Multan')
    cycle = run_cycle()

    self.assertEqual(cycle.decis_made, 0)
    self.assertFalse(DecisionRecord.objects.filter(incident=low_incid).exists())

  def test_preemption(self):
    Incident.objects.all().delete()
    now = timezone.now()
    
    Shift.objects.create(responder=self.responder, start_time=now - timedelta(hours=1), end_time=now + timedelta(hours=1))
    victim_incid = Incident.objects.create(title = 'Minor Issue', location = 'Sector-B Bahawalpur', severity=5, prior=5, status = 'active', created_by=self.admin)
    unit = Unit.objects.create(kind=self.resource, identifier = 'FT-02', location = 'Sector-B Bahawalpur')
    prev_exec = Execution.objects.create(incident=victim_incid, unit=unit, status = 'started')
    thief_incid = Incident.objects.create(title = 'Big Explosion', location = 'Sector-B Bahawalpur', 
      severity=50, prior=50, status = 'active', created_by=self.admin)
    Availability.objects.create(res_kind=self.resource, location = 'Sector-B Bahawalpur', total_units=1, avail_units=0)
    Load.objects.filter(responder=self.responder).update(load_count=0)

    run_cycle()
    prev_exec.refresh_from_db()
    self.assertEqual(prev_exec.status, 'failed', 'vict mission should be cance.')
    self.assertTrue(FailureRecord.objects.filter(execution=prev_exec).exists())
    decision_exists = DecisionRecord.objects.filter(incident=thief_incid, unit=unit).exists()
    self.assertTrue(decision_exists, 'dec rec isnt created for the thief')
    self.assertTrue(Execution.objects.filter(incident=thief_incid, status = 'pending').exists())

  def test_run_perm(self):
    self.auth_user(self.admin)
    Incident.objects.create(title = 'check', location = 'location', severity=50, prior=50, status = 'active', created_by=self.admin)
    Availability.objects.create(res_kind=self.resource, location = 'location', total_units=5, avail_units=5)
    Unit.objects.create(kind=self.resource, identifier = 'Id1', location = 'location')
    resp = self.client.post(self.run_url)
    self.assertEqual(resp.status_code, 200)
    self.assertIn('cycle_id', resp.data)

  def test_lat_cycle(self):
    self.auth_user(self.admin)
    Cycle.objects.create(total_incids=5)
    c2 = Cycle.objects.create(total_incids=10)
    resp = self.client.get(self.latest_url)
    print(resp.data)
    
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.data['id'], c2.id)
    self.assertEqual(resp.data['total_incids'], 10)

  def test_incid_list(self):
    self.auth_user(self.admin)
    Incident.objects.create(title = 'low', severity=10, prior=10, status = 'active', created_by=self.admin)
    inc2 = Incident.objects.create(title = 'high', severity=50, prior=50, status = 'active', created_by=self.admin)
    run_cycle()

    resp = self.client.get(self.list_url)
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.data[0]['incident'], inc2.id)
