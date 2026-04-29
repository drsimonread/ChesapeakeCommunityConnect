

# Create your tests here.
from django.test import TestCase
from boiler.models import Message, MessageForm  
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse


class MessageModelTests(TestCase):

    def test_create_message(self):
        # Test creating a Message instance
        message = Message.objects.create(
            sender="Test Name",
            email="test@test.com",
            subject="Test Subject",
            message="This is a test message.",
            acknowledged=False
        )

        self.assertEqual(message.sender, "Test Name")
        self.assertEqual(message.email, "test@test.com")
        self.assertEqual(message.subject, "Test Subject")
        self.assertEqual(message.message, "This is a test message.")
        self.assertFalse(message.acknowledged)
        self.assertTrue(message.created <= timezone.now())

    def test_string_representation(self):
        # Test the __str__ method
        message = Message.objects.create(
            sender="Jane Smith",
            email="jane@example.com",
            subject="Feedback",
            message="Some feedback content."
        )
        self.assertEqual(str(message), "Jane Smith | jane@example.com | Feedback")

    def test_email_field_validation(self):
        # Test invalid email format
        message = Message(
            sender="User",
            email="Invalid Email",  # Invalid email format
            subject="Test",
            message="Invalid email test."
        )
        with self.assertRaises(ValidationError):
            message.full_clean()  # This will raise a ValidationError due to invalid email
            

class MessageFormTests(TestCase):

    def test_form_valid_data(self):
        # Test form with valid data
        form_data = {
            'sender': 'Alice Brown',
            'email': 'alice@example.com',
            'subject': 'General Inquiry',
            'message': 'This is a message.'
        }
        form = MessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        # Test form with invalid email
        form_data = {
            'sender': 'Bob Green',
            'email': 'invalid email',  # Invalid email format
            'subject': 'Question',
            'message': 'Hello, I have a question.'
        }
        form = MessageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_placeholder_text(self):
        # Test that widgets have the correct placeholder text
        form = MessageForm()
        self.assertEqual(form.fields['sender'].widget.attrs['placeholder'], 'Name')
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email address')
        self.assertEqual(form.fields['subject'].widget.attrs['placeholder'], 'Subject')
        self.assertEqual(form.fields['message'].widget.attrs['placeholder'], 'Message')


