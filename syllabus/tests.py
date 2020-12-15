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
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/adminhome/')

    def test_invalid_admin_login(self):
        response = self.client.post('/', {'name': 'admin', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/')

    def test_valid_ta_login(self):
        response = self.client.post('/', {'name': 'ta', 'password': 'ta'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tahome/')

    def test_invalid_ta_login(self):
        response = self.client.post('/', {'name': 'ta', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/')

    def test_valid_instructor_login(self):
        response = self.client.post('/', {'name': 'instructor', 'password': 'instructor'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/instructorhome/')

    def test_invalid_instructor_login(self):
        response = self.client.post('/', {'name': 'instructor', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/')


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
        self.client.post('/createuser/', credentials)
        with self.assertRaises(ObjectDoesNotExist):
            TA.objects.get(username='', password='password')

    def test_create_user_no_password(self):
        credentials = {'utype': 'ta', 'name': 'name', 'password': '', 'email': 'email'}
        self.client.post('/createuser/', credentials)
        with self.assertRaises(ObjectDoesNotExist):
            TA.objects.get(username='name', password='')

    def test_create_user_no_email(self):
        credentials = {'utype': 'instructor', 'name': 'name', 'password': 'password', 'email': ''}
        self.client.post('/createuser/', credentials)
        with self.assertRaises(ObjectDoesNotExist):
            Instructor.objects.get(username='name', password='password')

    def test_create_user_TA(self):
        self.client.post('/createuser/', self.valid_credentials_TA)
        self.assertTrue(
            TA.objects.get(username=self.valid_credentials_TA['name'], password=self.valid_credentials_TA['password']))

    def test_create_user_Instructor(self):
        self.client.post('/createuser/', self.valid_credentials_Instructor)
        self.assertTrue(Instructor.objects.get(username=self.valid_credentials_Instructor['name'],
                                               password=self.valid_credentials_Instructor['password']))

    def test_edit_user_A(self):
        self.client.post('/edituserta-ta/', {'password': 'ta', 'email': 'ta@uwm.edu',
                                             'first_name': 'Tony', 'last_name': 'Stark', 'office': '', 'phone': '',
                                             'office_hours': ''})
        t = TA.objects.get(username='ta')
        self.assertEqual(t.first_name, "Tony")

    def test_delete_user_B(self):
        self.assertTrue(TA.objects.get(username='ta', password='ta'))
        self.client.post('/deleteuserta/')
        with self.assertRaises(ObjectDoesNotExist):
            TA.objects.get(username='ta', password='ta')

    # TODO test user editing as a TA and instructor


class TestModifyCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.course_B = Course.objects.create(name='MATH', dep_number='413', term='Fall 2020', instructor=None)
        self.section_1 = Section.objects.create(type_of='LAB', number='567', days='M', time='1-2:30pm',
                                                course=self.course_B)

    def test_create_course_A(self):
        self.client.post('/createcourse/', {'name': 'Intro to Software eng', 'dep_number': 'CS361', 'term': 'Fall 2020',
                                            'instruct': '', 'desc': 'desc'})
        self.assertTrue(Course.objects.get(dep_number='CS361'))

    def test_create_course_A_fail(self):
        response = self.client.post('/createcourse/', {'name': 'Intro to Software Eng', 'dep_number': '', 'term': '',
                                                       'instruct': '', 'desc': ''})
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            Course.objects.get(name='Intro to Software Eng')

    def test_edit_course_B_no_name(self):
        self.client.post('/editcourseMATH/', {'name': '', 'dep_number': '413', 'term': '',
                                              'instruct': '', 'desc': ''})
        self.assertEqual(Course.objects.get(name='MATH').dep_number, '413')

    def test_edit_course_B_no_number(self):
        self.client.post('/editcourseMATH/', {'name': 'MATH', 'dep_number': '', 'term': '',
                                              'instruct': '', 'desc': ''})
        self.assertEqual(Course.objects.get(name='MATH').dep_number, '413')

    def test_edit_course_B(self):
        self.client.post('/editcourseMATH/', {'name': 'MA', 'dep_number': '413', 'term': '',
                                              'instruct': '', 'desc': ''})
        self.assertEqual(Course.objects.get(name='MA').dep_number, '413')

    def test_create_section(self):
        self.client.post('/createsectionMATH/',
                         {'stype': 'LEC', 'number': '345', 'days': 'MW', 'time': '1-1:30pm', 'user': ''})
        self.assertTrue(Section.objects.get(course=self.course_B, number='345'))

    def test_create_section_fail(self):
        response = self.client.post('/createsectionMATH/',
                                    {'stype': '', 'number': '345', 'days': 'MW', 'time': '1-1:30pm', 'user': ''})
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            Section.objects.get(course=self.course_B, number='345')

    def test_edit_section(self):
        self.client.post('/editsection567-MATH/',
                         {'stype': 'LEC', 'number': '345', 'days': 'MW', 'time': '1-1:30pm', 'user': ''})
        self.assertTrue(Section.objects.get(course=self.course_B, number='345'))


class TestAssignUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_ta = TA.objects.create(username='ta', password='ta', email='ta@uwm.edu')
        self.user_ta2 = TA.objects.create(username='ta2', password='ta2', email='ta@uwm.edu')
        self.user_instructor = Instructor.objects.create(username='instructor', password='instructor',
                                                         email='instructor@uwm.edu')

        self.course_B = Course.objects.create(name='MATH', dep_number='413', term='Fall 2020')

    def test_assign_instructor(self):
        response = self.client.post('/editcourseMATH/', {'name': '', 'dep_number': '', 'term': '', 'instruct':
                                    'instructor', 'desc': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_instructor, self.course_B.instructor)

    def test_assign_instructor2(self):
        pass

    def test_assign_ta(self):
        pass

    def test_assign_ta2(self):
        pass

    def test_assign_another_ta(self):
        pass

    def test_sec_assign_instructor(self):
        pass

    def test_sec_assign_ta(self):
        pass


class TestModifySyllabusComponent(TestCase):
    pass


class TestViewCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_ta = TA.objects.create(username='ta', password='ta', email='ta@uwm.edu')
        self.user_ta2 = TA.objects.create(username='ta2', password='ta2', email='ta@uwm.edu')
        self.user_instructor = Instructor.objects.create(username='instructor', password='instructor',
                                                         email='instructor@uwm.edu')

        self.course_B = Course.objects.create(name='MATH', dep_number='413', term='Fall 2020',
                                              instructor=self.user_instructor)
        self.course_B.ta_set.add(self.user_ta)
        self.course_B.ta_set.add(self.user_ta2)

    def testDisplay(self):
        response = self.client.get('/courses/Fall%2020/413/')
        self.assertEqual(response.status_code, 200)
