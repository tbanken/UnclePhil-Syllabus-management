from django.test import TestCase, Client
from .models import *


# Create your tests here.

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Admin.objects.create(username='admin', password='123', email='test@admin.com')
        self.instruct = Instructor.objects.create(username='instruct', password='456',
                                                  email='test@instruct.com', first_name='Test',
                                                  last_name='Instructor', office='TestOffice',
                                                  phone='1234567810', office_hours='test')
        self.ta = Instructor.objects.create(username='ta', password='789',
                                                  email='test@ta.com', first_name='Test',
                                                  last_name='TA', office='TestOfficeTA',
                                                  phone='1098765432', office_hours='never')

    def testFail(self):
        pass


class TATest(TestCase):
    def setUp(self):
        self.client = Client()
        self.ta = Instructor.objects.create(username='ta', password='789',
                                            email='test@ta.com', first_name='Test',
                                            last_name='TA', office='TestOfficeTA',
                                            phone='1098765432', office_hours='never')
