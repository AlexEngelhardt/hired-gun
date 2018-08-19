import datetime

from django.test import TestCase

from django.urls import reverse

from projects.models import Client, Project, Session

# Create your tests here.
# Run via `python3 manage.py test projects`

def create_client(name="derp", payment_terms="Net 30"):
    return Client.objects.create(
        name=name,
        payment_terms=payment_terms
    )


def create_project(client=None, name="testproj", rate=100, rate_unit="hr", active=True):

    if client is None:
        client = create_client()
        
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=30)
    
    if active:
        end_date = today + datetime.timedelta(days=10)
    else:
        end_date = today - datetime.timedelta(days=10)

    return Project.objects.create(
        name=name,
        client=client,
        rate=rate,
        rate_unit=rate_unit,
        start_date=start_date,
        end_date=end_date
    )


def create_session(project=None, days_ago=0):
    if project is None:
        project = create_project()
        
    session_date = datetime.date.today() - datetime.timedelta(days=days_ago)
    return Session.objects.create(
        project = project,
        date = session_date,
        units_worked = 2
    )


class ClientModelTests(TestCase):
    def setUp(self):
        Client.objects.create(name="Superclient")

    def test_test(self):
        """
        Test that tests work :D
        """
        self.assertIs(2+3, 5)

    def ramalam_dingdong(self):
        """
        Look, test methods have to start with 'test'
        This guy won't be executed
        """
        self.assertIs(1+1, 4)


class ClientIndexViewTests(TestCase):
    def TODO_test_no_clients(self):
        """
        If no clients exist, show an appropriate message
        """
        
        response = self.client.get(reverse('projects:clients'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No clients are available")

class SessionModelTests(TestCase):

    def test_sessionmodeltest(self):
        """
        Test that this test file works :)
        """
        sesh = create_session()
        self.assertEqual(sesh.date, datetime.date.today())

class SessionIndexViewTests(TestCase):

    def test_indexview(self):
        create_session()
        response = self.client.get(reverse('projects:sessions'))
        self.assertQuerysetEqual(
            response.context['sessions'],
            ['<Session in testproj for derp on 2018-08-18>']
        )
