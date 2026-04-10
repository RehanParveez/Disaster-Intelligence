from accounts.tests import ParentTest
from responders.models import Responder, Load
from execution.models import Execution, ExecutionRecord, FailureRecord
from django.urls import reverse
from events.models import Event
from analytics.models import ResponseRecord
from incidents.models import AllocationDecision
from resources.models import Resource, Unit 

class ExecutionTest(ParentTest):
  def setUp(self):
    super().setUp()
    Execution.objects.all().delete()
    Responder.objects.all().delete()
    self.resource = Resource.objects.create(name = 'Ambulance', description = 'emergency medical situation')
    self.unit = Unit.objects.create(kind=self.resource, identifier = 'RESCUE-1122', created_by=self.admin)
    self.responder = Responder.objects.create(user=self.user, max_load=5)
    self.load = Load.objects.create(responder=self.responder, incident=self.incident, load_count=1)
    self.execution = Execution.objects.create(incident=self.incident, status = 'pending', created_by=self.user)
    AllocationDecision.objects.create(incident=self.incident, allocated_by=self.admin, unit=self.unit)

  def test_start_exec(self):
    self.auth_user(self.user)
    url = reverse('execution-start', kwargs={'pk': self.execution.id})
        
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    self.execution.refresh_from_db()
    self.assertEqual(self.execution.status, 'started')
    self.assertTrue(ExecutionRecord.objects.filter(execution=self.execution).exists())

  def test_fail_exec(self):
    self.auth_user(self.user)
    url = reverse('execution-fail', kwargs={'pk': self.execution.id})
    data = {'reason': 'the equip. is not work.'}
    resp = self.client.post(url, data)
    self.assertEqual(resp.status_code, 200)
    self.execution.refresh_from_db()
    self.assertEqual(self.execution.status, 'failed')
    self.assertTrue(FailureRecord.objects.filter(execution=self.execution, reason=data['reason']).exists())

    event = Event.objects.filter(event_kind__name = 'EXECUTION_FAILED')
    event = event.last()
    self.assertIsNotNone(event)
    self.assertEqual(event.payload['execution_id'], self.execution.id)

  def test_wrong_trans(self):
    self.execution.status = 'completed'
    self.execution.save()
    self.auth_user(self.user)
    url = reverse('execution-start', kwargs={'pk': self.execution.id})
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 400)
    
  def test_failure_escal(self):
    self.execution.status = 'failed'
    self.execution.save()
    self.execution.refresh_from_db()
    exists = FailureRecord.objects.filter(execution_id=self.execution.id).exists()
    if not exists:
        print(f'failurerecs {FailureRecord.objects.count()}')
    self.assertTrue(exists)
    
  def test_incid_resol(self):
    exec2 = Execution.objects.create(incident=self.incident, status = 'pending', created_by=self.user)
    self.execution.status = 'completed'
    self.execution.save()

    self.incident.refresh_from_db()
    self.assertEqual(self.incident.status, 'active')
    exec2.status = 'completed'
    exec2.save()
    self.incident.refresh_from_db()
    self.assertEqual(self.incident.status, 'resolved')
    self.assertTrue(ResponseRecord.objects.filter(incident=self.incident).exists())