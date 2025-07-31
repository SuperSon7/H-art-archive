# Adapters
from abc import ABC, abstractmethod
from authlib.integrations.requests_client import OAuth2Session
from django.conf import settings

class BaseSocialAdapter(ABC):
    provider_name = None
    
    @abstractmethod
    def exchange_code_for_token(self, code, **kwargs):
        pass
    
    @abstractmethod
    def get_user_info(self, access_token):
        pass
    
    @abstractmethod
    def normalize_user_data(self, raw_data):
        pass

class GoogleAdapter(BaseSocialAdapter):
    provider_name = 'google'
    def exchange_code_for_token(self, code, redirect_uri)-> str:
        client = OAuth2Session(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=redirect_uri,
            scope="openid email profile"
        )
        
        token = client.fetch_token(
            url="https://oauth2.googleapis.com/token",
            code=code
        )
        return token["access_token"]
    
    def get_user_info(self, access_token):
        client = OAuth2Session()
        resp = client.get("https://www.googleapis.com/oauth2/v3/userinfo")
        return resp.json()
    
    def normalize_user_data(self, raw_data):
        return {
            'email': raw_data['email'],
            'name': raw_data['name'],
            'provider_id': raw_data['sub'],
            'avatar': raw_data.get('picture')
        }
        
# resistrise
class SocialAdapterRegistry:
    _adapters = {}
    
    @classmethod
    def register(cls, adapter_class):
        if not hasattr(adapter_class, 'provider_name'):
            raise ValueError("Adapter must have provider_name")
        cls._adapters[adapter_class.provider_name] = adapter_class
        
    @classmethod
    def get_adapter(cls, provider_name):
        if provider_name not in cls._adapters:
            raise ValueError(f"Unknown provider: {provider_name}")
        return cls._adapters[provider_name]()
# Register Google adapter
SocialAdapterRegistry.register(GoogleAdapter)


