import pytest

class TestAdminViews:
    def test_admin_recipes(self, admin_client, complete_recipe):
        response = admin_client.get('/admin/recipe/')
        assert response.status_code == 200

        response = admin_client.get('/admin/recipe/recipe/')
        assert response.status_code == 200

        response = admin_client.get(f'/admin/recipe/recipe/{complete_recipe.id}/change/')
        assert response.status_code == 200
