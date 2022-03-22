from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Tag

def  create_user(email='test@test.com', password='password'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_tag_str(self):
        """ Tests the tag string representation """
        tag = Tag.objects.create(
            user=create_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)