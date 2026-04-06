from accounts.tests import ParentTest
from execution.models import Execution
from events.models import EventKind, Event, EventRecord
from django.urls import reverse
from events.services import make_event
from incidents.models import IncidentPriorRecord

class EventsTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.execution = Execution.objects.create(incident=self.incident, status = 'pending', created_by=self.user)
    self.kind, _ = EventKind.objects.get_or_create(name = 'EXECUTION_FAILED')

  def test_process_exec(self):
    initial_prior = self.incident.prior
    payload = {'execution_id': self.execution.id, 'reason': 'the unit isnt work.'}
    event = make_event(kind_name='EXECUTION_FAILED', payload=payload)
    
    event.refresh_from_db() 
    self.assertTrue(event.is_processed)
    self.assertTrue(EventRecord.objects.filter(event=event, status='success').exists())
    self.incident.refresh_from_db()
    self.assertEqual(self.incident.prior, initial_prior + 10)
    self.assertTrue(IncidentPriorRecord.objects.filter(incident=self.incident).exists())

  def test_replay(self):
    self.auth_user(self.admin)
    event = Event.objects.create(event_kind=self.kind, payload={'execution_id': self.execution.id}, is_processed=False)
    url = reverse('event-replay', kwargs={'pk': event.id})
    resp = self.client.post(url)
        
    self.assertEqual(resp.status_code, 200)
    event.refresh_from_db()
    self.assertTrue(event.is_processed)
    self.assertEqual(resp.data['message'], f'the event {event.id} is repla.')
