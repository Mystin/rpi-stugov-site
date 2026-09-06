from branches.models import BranchPage
from home.models import HomePage

from wagtail.images import get_image_model
from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase


class HomeSetUpTests(WagtailPageTestCase):
    """
    Tests for basic page structure setup and HomePage creation.
    """

    def test_root_create(self):
        root_page = Page.objects.get(pk=1)
        self.assertIsNotNone(root_page)

    def test_homepage_create(self):
        root_page = Page.objects.get(pk=1)
        homepage = HomePage(title="Home")
        root_page.add_child(instance=homepage)
        self.assertTrue(HomePage.objects.filter(title="Home").exists())


class HomeTests(WagtailPageTestCase):
    """
    Tests for homepage functionality and rendering.
    """

    def setUp(self):
        """
        Create a homepage instance for testing.
        """
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testsite", root_page=root_page, is_default_site=True)
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)

    def test_homepage_is_renderable(self):
        self.assertPageIsRenderable(self.homepage)

    def test_homepage_template_used(self):
        response = self.client.get(self.homepage.url)
        self.assertTemplateUsed(response, "home/home_page.html")

    def test_image_credits_are_rendered_with_source_links(self):
        image_model = get_image_model()
        hero_image = image_model.objects.create(
            title="Hero image",
            file=get_test_image_file(filename="hero.png"),
        )
        branch_image = image_model.objects.create(
            title="Branch image",
            file=get_test_image_file(filename="branch.png"),
        )

        self.homepage.hero_image = hero_image
        self.homepage.hero_image_credit = "RPI Archives"
        self.homepage.hero_image_credit_url = "https://example.com/hero"
        self.homepage.save()

        branch = BranchPage(
            title="Student Senate",
            branch_type="senate",
            image=branch_image,
            image_credit="Jane Photographer",
            image_credit_url="https://example.com/branch",
        )
        self.homepage.add_child(instance=branch)

        response = self.client.get(self.homepage.url)

        self.assertContains(response, "RPI Archives")
        self.assertContains(response, "https://example.com/hero")
        self.assertContains(response, "Jane Photographer")
        self.assertContains(response, "https://example.com/branch")

        response = self.client.get(branch.url)
        self.assertContains(response, "Jane Photographer")
        self.assertContains(response, "https://example.com/branch")
