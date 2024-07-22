from django.test import TestCase
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class SignUpViewTest(TestCase):
    username = 'myusername'
    pass1 = 'password12345'
    pass2 = 'password12345'
    email = 'myusername@gmail.com'

    def test_signup_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        get_user_model().objects.create_user(
            self.username,
            self.email,
        )
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)

    def test_signup_page_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_page_uses_correct_form(self):
        response = self.client.get(reverse('signup'))
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_signup_page_contains_correct_html(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'Sign Up')

    def test_signup_page_does_not_contain_incorrect_html(self):
        response = self.client.get(reverse('signup'))
        self.assertNotContains(response, 'Hi there! I should not be on the page.')

    def test_valid_signup_post(self):
        response = self.client.post(reverse('signup'), data={
            'username': self.username,
            'password1': self.pass1,
            'password2': self.pass2,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username=self.username.exists()))

    def test_invalid_signup_post(self):
        response = self.client.post(reverse('signup'), data={
            'username': '',
            'password1': self.pass1,
            'password2': self.pass2,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertFalse(User.objects.filter(username='').exists())
