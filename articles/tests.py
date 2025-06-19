from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from articles.models import Article, Category
from users.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile
User = get_user_model()


class DashboardViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('dashboard')
        self.user = User.objects.create_user(
            username='author', password='password123', role=CustomUser.AUTHOR, is_active=True,
            email="e.bahytzhanuly@tau-edu.kz"
        )
        self.redactor = User.objects.create_user(
            username='red', password='password123', role=CustomUser.REDACTOR, is_active=True,
            email="e.bahytzhanuly@tau-edu.kz"
        )

    # Test if user not authenticated
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/users/login/?next=' + self.url)

    def test_redirect_for_redactor(self):
        self.client.login(username='red', password='password123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('my_bids'))

    def test_dashboard_loads_for_author(self):
        self.client.login(username='author', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/dashboard.html')

    def test_post_empty_data(self):
        self.client.login(username='author', password='password123')

        url = reverse('dashboard')
        data = {

        }

        count_before = Article.objects.count()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        count_after = Article.objects.count()
        self.assertEqual(count_before, count_after)

    def test_post_bid_empty_data(self):
        self.client.login(username='author', password='password123')

        url = reverse('dashboard')

        category = Category.objects.create(title_en='Категория тест')

        test_file = SimpleUploadedFile(
            "testfile.pdf", b"file_content_here", content_type="application/pdf"
        )
        count_before = Article.objects.count()

        article_data = {
            'category': category.pk,
            'title': 'Заголовок статьи',
            'title_kk': 'Заголовок статьи KK',
            'title_ru': 'Заголовок статьи RU',
            'annotation': 'Аннотация',
            'annotation_kk': 'Аннотация KK',
            'annotation_ru': 'Аннотация RU',
            'authors': 'Автор1, Автор2',
        }
        file_data = {
            "file": test_file,
        }
        post_data = {**article_data, **file_data}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)

        count_after = Article.objects.count()
        self.assertEqual(count_before, count_after)

    def test_post_article_empty_data(self):
        self.client.login(username='author', password='password123')

        url = reverse('dashboard')

        category = Category.objects.create(title_en='Категория тест')

        test_file_1 = SimpleUploadedFile(
            "testfile.pdf", b"file_content_here", content_type="application/pdf"
        )
        test_file_2 = SimpleUploadedFile(
            "testfile.pdf", b"file_content_here", content_type="application/pdf"
        )
        test_file_3 = SimpleUploadedFile(
            "testfile.pdf", b"file_content_here", content_type="application/pdf"
        )
        count_before = Article.objects.count()

        bid_data = {
            'ai_usage_details': "Не использовал ИИ...",
            "exclusive_submission": True,
            "no_plagiarism": True,
            "authors_confirmed": True,
        }
        file_data = {
            'manuscript': test_file_1,
            'authors_file': test_file_2,
            'cover_letter': test_file_3,
        }

        post_data = {**bid_data, **file_data}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)

        count_after = Article.objects.count()
        self.assertEqual(count_before, count_after)

    def test_post_article_bid_data(self):
        self.client.login(username='author', password='password123')
        url = reverse('dashboard')
        category = Category.objects.create(title_en='Категория тест')
        test_file = SimpleUploadedFile(
            "testfile.pdf", b"file_content_here", content_type="application/pdf"
        )
        test_file_1 = SimpleUploadedFile(
            "testfile.pdf", b"file_content_here", content_type="application/pdf"
        )
        test_file_2 = SimpleUploadedFile(
            "testfile.pdf", b"file_content_here", content_type="application/pdf"
        )
        test_file_3 = SimpleUploadedFile(
            "testfile.pdf", b"file_content_here", content_type="application/pdf"
        )

        count_before = Article.objects.count() + 1

        article_data = {
            'category': str(category.pk),  # pk как строка
            'title': 'Заголовок статьи',
            'title_kk': 'Заголовок статьи KK',
            'title_ru': 'Заголовок статьи RU',
            'annotation': 'Аннотация',
            'annotation_kk': 'Аннотация KK',
            'annotation_ru': 'Аннотация RU',
            'authors': 'Автор1, Автор2',
        }

        bid_data = {
            'ai_usage_details': "Не использовал ИИ...",
            "exclusive_submission": True,
            "no_plagiarism": True,
            "authors_confirmed": True,
        }

        file_data = {
            'file': test_file,
            'manuscript': test_file_1,
            'authors_file': test_file_2,
            'cover_letter': test_file_3,
        }

        post_data = {**article_data, **bid_data, **file_data}

        response = self.client.post(url, data=post_data)

        count_after = Article.objects.count()

        self.assertEqual(count_before, count_after)
        self.assertEqual(response.status_code, 302)

