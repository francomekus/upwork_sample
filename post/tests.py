from django.test import TestCase, Client
from .models import Post

# Create your tests here.


class PostModelTest(TestCase):
    def setUp(self):
        Post.objects.create(title='This is the title', body='This is the body')

    def test_text_content(self):
        post = Post.objects.get(id=1)
        self.assertEqual(f'{post.title}', 'This is the title')
        self.assertEqual(f'{post.body}', 'This is the body')

    def test_post_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is the body')

    def test_post_detail_view(self):
        response = self.client.get('/1/')
        no_response = self.client.get('/post/450000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'This is the body')
