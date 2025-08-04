"""Test admin functionality."""

from django.contrib.admin import site
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase

from ..admin import CategoryAdmin, ListAdmin
from ..models import Category, List


class AdminTest(TestCase):
    """Test admin functionality."""

    def setUp(self) -> None:
        """Set up test data."""
        self.request = HttpRequest()
        self.request.user = AnonymousUser()

    def test_list_admin_has_delete_permission_returns_false(self) -> None:
        """Test ListAdmin.has_delete_permission returns False."""
        list_admin = ListAdmin(List, site)
        test_list = List.objects.create(name="Test List", id=1)

        # Test with obj
        self.assertFalse(list_admin.has_delete_permission(self.request, test_list))

        # Test without obj
        self.assertFalse(list_admin.has_delete_permission(self.request))

    def test_category_admin_has_delete_permission_returns_false(self) -> None:
        """Test CategoryAdmin.has_delete_permission returns False."""
        category_admin = CategoryAdmin(Category, site)
        test_category = Category.objects.create(name="Test Category", id=1)

        # Test with obj
        self.assertFalse(category_admin.has_delete_permission(self.request, test_category))

        # Test without obj
        self.assertFalse(category_admin.has_delete_permission(self.request))
