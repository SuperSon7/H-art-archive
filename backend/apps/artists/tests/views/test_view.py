from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()

class TestUserInfoViewSet:
    
    def test_retrieve_own_profile(self, authenticated_client, artist):
        """artist profile retrieval test"""
        url = reverse('artists-detail', kwargs={'pk': artist.id})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['artist_name'] == artist.artist_name
        
    def test_approve_artist(self, authenticated_client, artist):
        """ artist approval test """
        url = reverse('artists-approve', kwargs={'pk':artist.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_reject_artist(self, authenticated_client, approved_artist):
        """ artist approval test """
        url = reverse('artists-reject', kwargs={'pk':approved_artist.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_update_artist_profile(self, authenticated_client, artist):
        """ artist profile update test """
        url = reverse('artists-detail', kwargs={'pk':artist.id})
        data = {
            'artist_name': 'Updated Artist Name',
            'artist_note': 'Updated artist note'
        }
        response = authenticated_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        artist.refresh_from_db()
        assert artist.artist_name == 'Updated Artist Name' and artist.artist_note == 'Updated artist note'
    
    def test_nonexistent_artist(self, authenticated_client):
        """nonexistent artitst rerival test"""
        url = reverse('artists-detail', kwargs={'pk': 99999})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND