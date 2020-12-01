from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist
from .models import *


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_admin = Admin.objects.create(username='admin', password='admin', email='admin@uwm.edu')
        self.user_ta = TA.objects.create(username='ta', password='ta', email='ta@uwm.edu')
        self.user_instructor = Instructor.objects.create(username='instructor', password='instructor',
                                                         email='instructor@uwm.edu')

    def test_valid_admin_login(self):
        response = self.client.post('/', {'name': 'admin', 'password': 'admin'})
        self.assertEqual(response.url, '/adminhome/')

    def test_invalid_admin_login(self):
        response = self.client.post('/', {'name': 'admin', 'password': 'password'})
        self.assertEqual(response.url, '/')

    def test_valid_ta_login(self):
        response = self.client.post('/', {'name': 'ta', 'password': 'ta'})
        self.assertEqual(response.url, '/tahome/')

    def test_invalid_ta_login(self):
        response = self.client.post('/', {'name': 'ta', 'password': 'password'})
        self.assertEqual(response.url, '/')

    def test_valid_instructor_login(self):
        response = self.client.post('/', {'name': 'instructor', 'password': 'instructor'})
        self.assertEqual(response.url, '/instructorhome/')

    def test_invalid_instructor_login(self):
        response = self.client.post('/', {'name': 'instructor', 'password': 'password'})
        self.assertEqual(response.url, '/')


class TestModifyUsers(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_credentials_TA = {'utype': 'ta', 'name': 'TA', 'password': 'password', 'email': 'TA@uwm.edu',
                                     'first_name': 'T', 'last_name': 'A', 'office': '', 'phone': '', 'office_hours': ''}
        self.valid_credentials_Instructor = {'utype': 'instructor', 'name': 'Instructor', 'password': 'password'
            , 'email': 'Instructor@uwm.edu', 'first_name': 'In', 'last_name': 'Structor', 'office': '', 'phone': '',
                                             'office_hours': ''}

        self.user_A = Instructor.objects.create(username='Instructor', password='instructor',
                                                email='instructor@uwm.edu')
        self.user_B = TA.objects.create(username='ta', password='ta', email='ta@uwm.edu')

    def test_create_user_no_name(self):
        credentials = {'utype': 'ta', 'name': '', 'password': 'password', 'email': 'email'}
        response = self.client.post('/createuser/', credentials)
        self.assertRaises(ObjectDoesNotExist, TA.objects.get(username='', password='password'))

    def test_create_user_no_password(self):
        credentials = {'utype': 'ta', 'name': 'name', 'password': '', 'email': 'email'}
        response = self.client.post('/createuser/', credentials)
        self.assertRaises(ObjectDoesNotExist, TA.objects.get(username='name', password=''))

    def test_create_user_no_email(self):
        credentials = {'utype': 'instructor', 'name': 'name', 'password': 'password', 'email': ''}
        response = self.client.post('/createuser/', credentials)
        self.assertRaises(ObjectDoesNotExist, Instructor.objects.get(username='name', password='password'))

    def test_create_user_TA(self):
        response = self.client.post('/createuser/', self.valid_credentials_TA)
        self.assertTrue(
            TA.objects.get(username=self.valid_credentials_TA['name'], password=self.valid_credentials_TA['password']))

    def test_create_user_Instructor(self):
        response = self.client.post('/createuser/', self.valid_credentials_Instructor)
        self.assertTrue(Instructor.objects.get(username=self.valid_credentials_Instructor['name'],
                                               password=self.valid_credentials_Instructor['password']))

    # def test_edit_user_A(self):
    #     response = self.client.post('/edituser/',utype='ta',username='ta', {'first_name':'Tony','last_name':'Stark'})
    #     t = TA.objects.get(username='ta')
    #     self.assertEqual(t.first_name, "Tony")

    def test_delete_user_B(self):
        self.assertTrue(TA.objects.get(username='ta', password='ta'))
        response = self.client.post('/deleteuser/', username='ta')
        self.assertRaises(ObjectDoesNotExist, TA.objects.get(username='ta', password='ta'))


class TestModifyCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.course_B = Course.objects.create(name='MATH', number='413')

    def test_create_course_A(self):
        self.assertRaises(ObjectDoesNotExist, Course.objects.get(name='CS', number='361'))
        response = self.client.post('/createcourse/', {'name': 'CS', 'number': '361'})
        self.assertTrue(Course.objects.get(name='CS', number='361'))

    def test_edit_course_B_no_name(self):
        response = self.client.post('/editcourseMATH/', {'name': 'MATH', 'number': '415'})
        self.assertEqual(Course.objects.get(name='MATH').number, 413)

    def test_edit_course_B_no_number(self):
        response = self.client.post('/editcourse/', {'name': 'MATH', 'number': ''})
        self.assertEqual(Course.objects.get(name='MATH').number, 413)

    def test_edit_course_B(self):
        response = self.client.post('/editcourse/', {'name': 'MATH', 'number': '415'})
        self.assertEqual(Course.objects.get(name='MATH').number, 415)