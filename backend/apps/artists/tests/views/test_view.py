from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.unit
class TestArtistProfileViewSet:
    def test_retrieve_own_profile(self, artist_client, artist):
        """artist profile retrieval test"""
        url = reverse("artists-detail", kwargs={"pk": artist.id})
        response = artist_client.get(url, HTTP_ACCEPT_LANGUAGE="ko")
        print("Available translations:", response.data["translations"].keys())
        print("Full response:", response.data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["translations"]["ko"]["artist_name"] == artist.safe_translation_getter(
            "artist_name", language_code="ko"
        )

    def test_approve_artist(self, admin_client, artist):
        """artist approval test"""
        url = reverse("artists-admin-approve", kwargs={"pk": artist.id})
        response = admin_client.post(url)
        assert response.status_code == status.HTTP_200_OK

    def test_reject_artist(self, admin_client, approved_artist):
        """artist approval test"""
        url = reverse("artists-admin-reject", kwargs={"pk": approved_artist.id})
        response = admin_client.post(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_artist_profile(self, artist_client, artist):
        """artist profile update test"""
        from django.utils import translation

        translation.activate("ko")
        url = reverse("artists-detail", kwargs={"pk": artist.id})
        data = {
            "translations": {
                "ko": {"artist_name": "Updated Artist Name", "artist_note": "Updated artist note"}
            }
        }
        response = artist_client.patch(url, data, format="json")
        print("response data:", response.data)
        assert response.status_code == status.HTTP_200_OK
        artist.refresh_from_db()
        # artist.set_current_language('ko')

        assert (
            artist.safe_translation_getter("artist_name", language_code="ko")
            == "Updated Artist Name"
        )
        # assert artist.artist_note == 'Updated artist note'

    def test_nonexistent_artist(self, authenticated_client):
        """nonexistent artist retrieval test"""
        url = reverse("artists-detail", kwargs={"pk": 99999})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch("apps.utils.s3_presigner.create_presigned_url")
    def test_generate_main_image_url(self, mock_generate_url, artist_client, artist):
        """main image upload url generation test"""
        mock_generate_url.return_value = (
            "https://s3.amazonaws.com/presigned-url",
            f"profiles/{artist.user.id}/artist_main/test.jpg",
        )

        url = reverse("artists-main-image-presigned")
        data = {"filename": "test.jpg", "content_type": "image/jpeg"}
        response = artist_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "upload_url" in response.data
        assert "s3_key" in response.data

    def test_save_main_image(self, artist_client, artist):
        """test for saving main image"""
        url = reverse("artists-main-image")
        data = {"key": f"profiles/{artist.user.id}/artist_main/test.jpg"}
        response = artist_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        artist.refresh_from_db()
        assert artist.main_image_url is not None
