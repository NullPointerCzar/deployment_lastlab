from django.test import TestCase, LiveServerTestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Note


# ──────────────────────────────────────────────
# 1.  Django Unit Tests
# ──────────────────────────────────────────────

class NoteModelTests(TestCase):

    def test_notes_can_be_created(self):
        """A note with a description of 10+ chars can be saved successfully."""
        note = Note.objects.create(description="This is a valid note description")
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(note.description, "This is a valid note description")

    def test_error_occurs_if_description_is_less_than_10_chars_long(self):
        """A note whose description is shorter than 10 chars must fail validation."""
        note = Note(description="short")
        with self.assertRaises(ValidationError):
            note.full_clean()


# ──────────────────────────────────────────────
# 2.  Selenium UI Tests
# ──────────────────────────────────────────────

class NoteSeleniumTests(LiveServerTestCase):
    """
    End-to-end browser tests using Selenium.
    Requires:  pip install selenium
    chromedriver must be available on PATH (or set via webdriver options).
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        options = Options()
        options.add_argument("--headless")      # run without a visible window in CI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_notes_can_be_created(self):
        """Submitting a valid note through the browser creates it and shows it on the list page."""
        self.driver.get(f"{self.live_server_url}/notes/new/")
        textarea = self.driver.find_element("name", "description")
        textarea.clear()
        textarea.send_keys("This is a valid note description")
        textarea.submit()
        # After a successful save we are redirected to the list page
        body = self.driver.find_element("tag name", "body").text
        self.assertIn("This is a valid note description", body)

    def test_error_occurs_if_description_is_less_than_10_chars_long(self):
        """Submitting a too-short description stays on the form page and shows an error."""
        self.driver.get(f"{self.live_server_url}/notes/new/")
        textarea = self.driver.find_element("name", "description")
        textarea.clear()
        textarea.send_keys("short")
        textarea.submit()
        body = self.driver.find_element("tag name", "body").text
        self.assertIn("Description must be at least 10 characters", body)

