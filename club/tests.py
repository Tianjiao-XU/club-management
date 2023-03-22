from django.test import TestCase

from club.models import Club


# Create your tests here.
from django.test import TestCase
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
        add_club("Football",999,5)
        response = self.client.get(reverse('club:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Football")


def add_club(name, likes=0, dislikes=0):
    club = Club.objects.get_or_create(name=name)[0]
    club.likes = likes
    club.dislikes = dislikes
    club.save()
    return club











