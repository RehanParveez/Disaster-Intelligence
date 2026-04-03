from accounts.tests import ParentTest
from incidents.selectors.inc_sel import inc_id, nearby_inc, group_by_loc
from incidents.models import IncidentGroup, Incident, IncidentReport, AllocationDecision
from incidents.services.inc_ser import inc_report, verifiy_inc, reject_inc, group_incid, cal_prior
from django.core.exceptions import PermissionDenied
from resources.models import Resource, Unit, Inventory, Availability, Consumption

class SelectorTests(ParentTest):
  def test_inc_id(self):
    inc = inc_id(self.incident.id)
    self.assertEqual(inc.id, self.incident.id)

  def test_nearby_inc(self):
    inc = nearby_inc('Bahawalpur')
    self.assertEqual(inc.location, 'Bahawalpur')

  def test_group_by_loc(self):
    group = IncidentGroup.objects.create(location = 'Bahawalpur', group_size=1)
    res = group_by_loc('Bahawalpur')
    self.assertEqual(res.id, group.id)

class ServiceTests(ParentTest):
  def test_inc_report1(self):
    res = {'location': 'Bahawalpur', 'description': 'the danger of flood is upon us', 'severity': 5, 
      'title': 'Flood Danger'}

    incid = inc_report(res, self.user)
    self.assertEqual(incid.location, 'Bahawalpur')
    self.assertTrue(Incident.objects.count(), 1)
  
  def test_inc_report2(self):
    res = {'location': 'Multan', 'description': 'Fire', 'severity': 4, 'title': 'Fire'}
    inc_report(res, self.user)
    self.assertEqual(Incident.objects.count(), 2)

  def test_verify_incid(self):
    incid = verifiy_inc(self.incident.id, self.admin)
    self.assertEqual(incid.status, 'verified')

  def test_verify_admin(self):
    with self.assertRaises(PermissionDenied):
     verifiy_inc(self.incident.id, self.user)

  def test_reject_incid(self):
    incid = reject_inc(self.incident.id, self.admin)
    self.assertEqual(incid.status, 'rejected')

  def test_group_incid(self):
    group = group_incid(self.incident.id)
    self.assertEqual(group.location, self.incident.location)

  def test_cal_prior(self):
    IncidentReport.objects.create(incident=self.incident, reported_by=self.user, description = 'the prior test', location = 'Bahawalpur')
    incid = cal_prior(self.incident.id)
    self.assertTrue(incid.prior > 0)

class IncidentViewsetTest(ParentTest):
  def setUp(self):
    super().setUp()  
    self.resource = Resource.objects.create(name = 'Ambulance')
    self.unit = Unit.objects.create(kind=self.resource, identifier = 'ABC-101', location = 'Bahawalpur', created_by=self.user)
    self.availability = Availability.objects.create(res_kind=self.resource, location = 'Bahawalpur', total_units=1, avail_units=1)
    self.inventory = Inventory.objects.create(name = 'Head Office', location = 'Bahawalpur')
    
  def test_report(self):
    self.auth_user(self.user)
    res = {'location': 'Islamabad', 'description': 'EarthQuake', 'severity': 4, 'title': 'Road Accident'}
    resp = self.client.post('/incidents/incident/report/', res)
    self.assertEqual(resp.status_code, 201)
    self.assertIn('incident_id', resp.data)
        
  def test_verify1(self):
    self.auth_user(self.admin)
    url = f'/incidents/incident/{self.incident.id}/verify/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
  
  def test_verify2(self):
    self.auth_user(self.user)
    url = f'/incidents/incident/{self.incident.id}/verify/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 403)
  
  def test_reject(self):
    self.auth_user(self.admin)
    url = f'/incidents/incident/{self.incident.id}/reject/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
  
  def test_group(self):
    self.auth_user(self.user)
    url = f'/incidents/incident/{self.incident.id}/group/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    self.assertIn("group_id", resp.data)
        
  def test_recal_prior(self):
    self.auth_user(self.user)
    url = f'/incidents/incident/{self.incident.id}/recal_prior/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    self.assertIn('prior', resp.data)
  
  def test_prior_list(self):
    self.auth_user(self.user)
    resp = self.client.get('/incidents/incident/prior_list/')
    self.assertEqual(resp.status_code, 200)
    
  def test_allocate_unit(self):
    self.auth_user(self.user)
    url = f'/incidents/incident/{self.incident.id}/allocate_unit/'
    data = {'unit_id': self.unit.id, 'inventory_id': self.inventory.id, 'reason': 'the emergency allocation'}
    response = self.client.post(url, data, format = 'json')
    self.assertEqual(response.status_code, 200)
    self.assertIn('the unit is allocated', response.data['message'])

    self.availability.refresh_from_db()
    self.assertEqual(self.availability.avail_units, 0)
    
    consumption = Consumption.objects.filter(unit=self.unit, inventory=self.inventory, change_kind = 'allocated')
    self.assertTrue(consumption.exists())
    alloc = AllocationDecision.objects.filter(unit=self.unit, incident=self.incident)
    self.assertTrue(alloc.exists())

  def test_return_unit(self):
    self.auth_user(self.user)
    AllocationDecision.objects.create(unit=self.unit, incident=self.incident, allocated_by=self.user,
      inventory=self.inventory, reason = 'allocation test')
    self.inventory.resources.add(self.unit)
    self.availability.avail_units = 0
    self.availability.save()

    url = f'/incidents/incident/{self.incident.id}/return_unit/'
    data = {'unit_id': self.unit.id, 'reason': 'now after the incid lets return the unit'}
    response = self.client.post(url, data, format = 'json')
    self.assertEqual(response.status_code, 200)
    self.assertIn('the unit is returned', response.data['message'])

    self.availability.refresh_from_db()
    self.assertEqual(self.availability.avail_units, 1)

    consumption = Consumption.objects.filter(unit=self.unit, inventory=self.inventory, change_kind = 'returned')
    self.assertTrue(consumption.exists())
    alloc_check = AllocationDecision.objects.filter(unit=self.unit, incident=self.incident)
    self.assertFalse(alloc_check.exists())
  