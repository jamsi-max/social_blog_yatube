# posts/tests/tests_url.py
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')

        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            text='Текст тестового поста',
            author=StaticURLTests.user,
            group=StaticURLTests.group
        )

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template_for_guest_client(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{StaticURLTests.group.slug}/': 'posts/group_list.html',
            f'/profile/{StaticURLTests.user}/': 'posts/profile.html',
            f'/posts/{StaticURLTests.post.id}/': 'posts/post_detail.html',
        }

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_correct_template_authorized_client(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            f'/posts/{StaticURLTests.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
            '/follow/': 'posts/follow.html',
        }

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_post_edit_url_redirect_anonymous(self):
        """
        Страница /posts/<post_id>/edit/
        перенаправляет анонимного пользователя.
        """
        response = self.guest_client.get(
            f'/posts/{StaticURLTests.post.id}/edit/'
        )
        self.assertRedirects(
            response,
            reverse('users:login')
            + '?next='
            + reverse(
                'posts:post_edit',
                kwargs={'post_id': StaticURLTests.post.id}
            )
        )

    def test_post_create_url_redirect_anonymous(self):
        """Страница /create/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get('/create/')
        self.assertRedirects(
            response,
            reverse('users:login')
            + '?next='
            + reverse('posts:post_create')
        )

    def test_post_delete_url_redirect_anonymous(self):
        """
        Страница /posts/<post_id>/delete/ перенаправляет
        анонимного пользователя.
        """
        response = self.guest_client.get(
            f'/posts/{StaticURLTests.post.id}/delete/'
        )
        self.assertRedirects(
            response,
            reverse('users:login')
            + '?next='
            + reverse(
                'posts:post_delete',
                kwargs={'post_id': StaticURLTests.post.id}
            )
        )

    def test_post_comment_url_redirect_anonymous(self):
        """
        Страница /posts/<post_id>/comment/ перенаправляет
        анонимного пользователя.
        """
        response = self.guest_client.get(
            f'/posts/{StaticURLTests.post.id}/comment/'
        )
        self.assertRedirects(
            response,
            reverse('users:login')
            + '?next='
            + reverse(
                'posts:add_comment',
                kwargs={'post_id': StaticURLTests.post.id}
            )
        )

    def test_follow_url_redirect_anonymous(self):
        """
        Страница /posts/<str:username>/follow/ перенаправляет
        анонимного пользователя.
        """
        response = self.guest_client.get(
            f'/profile/{StaticURLTests.user.username}/follow/'
        )
        self.assertRedirects(
            response,
            reverse('users:login')
            + '?next='
            + reverse(
                'posts:profile_follow',
                kwargs={'username': StaticURLTests.user.username}
            )
        )

    def test_unfollow_url_redirect_anonymous(self):
        """
        Страница /profile/<str:username>/unfollow/ перенаправляет
        анонимного пользователя.
        """
        response = self.guest_client.get(
            f'/profile/{StaticURLTests.user.username}/unfollow/'
        )
        self.assertRedirects(
            response,
            reverse('users:login')
            + '?next='
            + reverse(
                'posts:profile_unfollow',
                kwargs={'username': StaticURLTests.user.username}
            )
        )

    def test_urls_404_for_guest_client(self):
        response = self.guest_client.get('unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_404_for_authorized_client(self):
        response = self.authorized_client.get('unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
