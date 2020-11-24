from django.test import TestCase
from django.contrib.auth.models import User
from .models import TA, Instructor

# Create your tests here.


class TATestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="tbanken", password='4744', first_name='Ted', last_name='Banken')
        TA.objects.create(user=user)
