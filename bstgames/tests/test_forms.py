from django.test import TestCase
from django.contrib.auth import get_user_model

from bstgames.forms import SignUpForm, SendVerifyEmailForm, EditProfileAddressForm


class SignUpFormTestCase(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.password = self.user_model.objects.make_random_password()
        self.email = 'example@example.domain'
        data = {
            'email': self.email, 
            'password1': self.password,
            'password2': self.password
        }
        self.form = SignUpForm(data)

    def test_save(self):
        self.assertTrue(self.form.is_valid())
        user = self.form.save()
        self.assertTrue(self.user_model.objects.filter(pk=user.pk).exists())
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.email, user.username)
        self.assertTrue(user.check_password(self.password))


class SendVerifyEmailFormTestCase(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.email = 'example@example.domain'
        self.password = self.user_model.objects.make_random_password()
        self.invalid_password = self.user_model.objects.make_random_password()
        self.user = self.user_model.objects.create_user(
            username=self.email, email=self.email, password=self.password
        )
        valid_data = {'email': self.user.email, 'password': self.password}
        invalid_password = {'email': self.user.email, 'password': self.invalid_password}
        invalid_email = {'email': 'invalid@invalid.domain', 'password': self.invalid_password}
        self.valid_form = SendVerifyEmailForm(valid_data)
        self.invalid_form_password = SendVerifyEmailForm(invalid_password)
        self.invalid_form_email = SendVerifyEmailForm(invalid_email)

    def test_clean(self):
        self.assertTrue(self.valid_form.is_valid())
        self.assertFalse(self.invalid_form_password.is_valid())
        self.assertFalse(self.invalid_form_email.is_valid())

    def test_get_user(self):
        self.valid_form.is_valid()
        get_user = self.valid_form.get_user()
        self.assertEqual(get_user, self.user)


class EditProfileAddressFormTestCase(TestCase):

    def setUp(self):
        self.valid_form = EditProfileAddressForm({'postal_code': '12345-678'})
        self.invalid_form = EditProfileAddressForm({'postal_code': '123456789'})

    def test_clean_postal_code(self):
        self.assertTrue(self.valid_form.is_valid())
        self.assertFalse(self.invalid_form.is_valid())
