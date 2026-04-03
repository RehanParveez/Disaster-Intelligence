from accounts.tests import ParentTest
from resources.models import Resource, Unit, Availability, Inventory, Consumption
from django.core.exceptions import ValidationError
from resources.services import create_unit, allocate_unit, return_unit, update_avail
from rest_framework.test import APIClient

class ServicesTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.resource1 = Resource.objects.create(name = 'Food', description = 'food packets')
    self.resource2 = Resource.objects.create(name = 'Water', description = 'water bottles')
    self.unit1 = Unit.objects.create(kind=self.resource1, identifier = 'U001', location = 'Bahawalpur', created_by=self.user)
    self.unit2 = Unit.objects.create(kind=self.resource2, identifier = 'U002', location = 'Bahawalpur', created_by=self.user)
    self.avail1 = Availability.objects.create(res_kind=self.resource1, total_units=1, avail_units=1, location = 'Bahawalpur')
    self.avail2 = Availability.objects.create(res_kind=self.resource2, total_units=1, avail_units=1, location = 'Bahawalpur')
    self.invent = Inventory.objects.create(name = 'Main Storage', location = 'Bahawalpur')

  def test_create_unit1(self):
    data = {'kind': self.resource1.id, 'identifier': 'U003', 'location': 'Bahawalpur'}
    unit = create_unit(data, self.user)
    self.assertEqual(unit.kind, self.resource1)
    self.assertEqual(unit.identifier, 'U003')
    self.assertEqual(Availability.objects.get(res_kind=self.resource1, location = 'Bahawalpur').total_units, 2)
    self.assertEqual(Consumption.objects.filter(unit=unit, change_kind = 'created').count(), 1)

  def test_allocate_unit1(self):
    prev_avail = self.avail1.avail_units
    avail = allocate_unit(self.unit1.id, self.invent.id, self.user, reason = 'for work')
    self.assertEqual(avail.avail_units, prev_avail - 1)
    self.assertIn(self.unit1, self.invent.resources.all())
    self.assertEqual(Consumption.objects.filter(unit=self.unit1, change_kind = 'allocated').count(), 1)

  def test_return_unit1(self):
    allocate_unit(self.unit1.id, self.invent.id, self.user)
    prev_avail = Availability.objects.get(id=self.avail1.id).avail_units
    avail = return_unit(self.unit1.id, self.invent.id, self.user, reason = ' return unit from field')
    self.assertEqual(avail.avail_units, prev_avail + 1)
    self.assertNotIn(self.unit1, self.invent.resources.all())
    self.assertEqual(Consumption.objects.filter(unit=self.unit1, change_kind = 'returned').count(), 1)

  def test_update_avail(self):
    data = {'avail_units': 0}
    avail = update_avail(self.unit1.id, data)
    self.assertEqual(avail.avail_units, 0)

  def test_create_unit2(self):
    data = {'identifier': 'U004', 'location': 'Bahawalpur'} 
    with self.assertRaises(ValidationError):
      create_unit(data, self.user)
   
  def test_allo_mul_units(self):
    units = []
    for v, res in enumerate([self.resource1, self.resource2], start=3):
      u = Unit.objects.create(kind=res, identifier = f'U00{v}', location = 'Bahawalpur', created_by=self.user)
      units.append(u)
      Availability.objects.filter(res_kind=res, location = 'Bahawalpur').update(avail_units=2, total_units=2)
    for u in units:
      allocate_unit(u.id, self.invent.id, self.user)
    for u in units:
      self.assertIn(u, self.invent.resources.all())
      self.assertEqual(Consumption.objects.filter(unit=u, change_kind = 'allocated').count(), 1)

  def test_return_mul_units(self):
    allocate_unit(self.unit1.id, self.invent.id, self.user)
    allocate_unit(self.unit2.id, self.invent.id, self.user)
    return_unit(self.unit1.id, self.invent.id, self.user)
    return_unit(self.unit2.id, self.invent.id, self.user)
    
    self.assertNotIn(self.unit1, self.invent.resources.all())
    self.assertNotIn(self.unit2, self.invent.resources.all())
    self.assertEqual(Consumption.objects.filter(unit=self.unit1, change_kind = 'returned').count(), 1)
    self.assertEqual(Consumption.objects.filter(unit=self.unit2, change_kind = 'returned').count(), 1)

class UnitViewsetTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.auth_user(self.user)
    self.resource1 = Resource.objects.create(name = 'Water', description = 'water bottles')
    self.resource2 = Resource.objects.create(name = 'Food', description = 'food packets')
    self.unit1 = Unit.objects.create(kind=self.resource1, identifier = 'U001', location = 'Bahawalpur', created_by=self.user)
    self.unit2 = Unit.objects.create(kind=self.resource2, identifier = 'U002', location = 'Bahawalpur', created_by=self.user)
    self.avail1 = Availability.objects.create(res_kind=self.resource1, total_units=2, avail_units=2, location = 'Bahawalpur')
    self.avail2 = Availability.objects.create(res_kind=self.resource2, total_units=2, avail_units=2, location = 'Bahawalpur')
    self.invent = Inventory.objects.create(name = 'Main Storage', location = 'Bahawalpur')

  def test_upd_avail(self):
    url = f'/resources/unit/{self.unit1.id}/upd_avail/'
    response = self.client.post(url, {'avail_units': 0})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Availability.objects.get(id=self.avail1.id).avail_units, 0)
