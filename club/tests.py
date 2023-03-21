from django.test import TestCase

from club.models import Club


# Create your tests here.
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