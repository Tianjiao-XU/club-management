# from django.contrib.auth.models import User
from django.test import TestCase

from club.forms import CreateClubForm, RegisterForm, LoginForm
from club.models import Club, User

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse


class ClubMethodTests(TestCase):
    def test_ensure_likes_are_positive(self):
        """
        Ensures the number of likes & dislikes received for a Club are positive or zero.
        """
        club1 = Club(name='test', likes=-1, dislikes=-1)
        club1.save()
        self.assertEqual((club1.likes >= 0), True)
        self.assertEqual((club1.dislikes >= 0), True)

    def test_slug_line_creation(self):
        """
        Checks to make sure that when a club is created, an
        appropriate slug is created.
        Example: "Random Club String" should be "random-club-string".
        """

        club2 = Club(name='Random Club String')
        club2.save()
        self.assertEqual(club2.slug, 'random-club-string')


class ViewTest(TestCase):
    def test_index_view_date_and_time(self):
        """
        Checks that the data and time are present on the index page.
        """
        response = self.client.get(reverse('club:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Today is')

    def test_contact_view_overview(self):
        """
        Checks that the Overview is present on the contact page.
        """
        response = self.client.get(reverse('club:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Overview')

    def test_login_view_login_to_user(self):
        """
        Checks that the user login is present on the login page.
        """
        response = self.client.get(reverse('club:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login to user')

    def test_search_view_searchbar(self):
        """
        Checks that the searchbar is present on the search page.
        """
        response = self.client.get(reverse('club:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ' Search')

    def test_index_view_with_club(self):
        """
        Checks if clubs are displayed correctly.
        """
        add_club("Football", 999, 5)
        response = self.client.get(reverse('club:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Football")


class RegisterViewTestCase(TestCase):
    """
    This class is used to check the register functions
    """
    def setUp(self):
        """
        set up a test user
        """
        self.url = reverse('club:register')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123!',
            'birthday': '12/11/2002',
        }

    def test_register_view_get(self):
        """
        test the register view get
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/register.html')
        self.assertIsInstance(response.context['register_form'], RegisterForm)
        self.assertFalse(response.context['registered'])

class UserLoginTestCase(TestCase):
    """
    This class is used to check the login functions
    """
    def setUp(self):
        """
        create a test user
        """
        self.user = User.objects.create_user(email='testuser@gmail.com', username="testuser", password='testpassword123')
        self.login_url = reverse('club:login')

    def test_login_page_loads(self):
        """
        load login page
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/login.html')
        self.assertIsInstance(response.context['login_form'], LoginForm)

    def test_valid_login(self):
        """
        test a valid input
        """
        data = {'email' : 'testuser@gmail.com', 'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, reverse('club:index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

class ClubViewTestCase(TestCase):
    """
    This class is used to check the club view
    """
    def setUp(self):
        """
        Create test user and club objects
        """
        self.user = User.objects.create_user(email='testuser@gmail.com', username="testuser", password='testpassword123')
        self.club = Club.objects.create(name='Test Club', description='A test club', manager=self.user)

    def test_viewClub_authenticated(self):
        """
        Test authenticated user can access club details
        """
        client = Client()
        client.login(email='testuser@gmail.com', password='testpassword123')
        response = client.get(reverse('club:view_club', args=[self.club.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Club')
        self.assertContains(response, 'A test club')



def add_club(name, likes=0, dislikes=0,type = "football",location="Glasgow"):
    """
    this method is used to create and add a club in database
    """
    club = Club.objects.get_or_create(name=name,type=type,location=location)[0]
    club.likes = likes
    club.dislikes = dislikes
    club.save()
    return club
