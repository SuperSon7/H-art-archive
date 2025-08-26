import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  User, Artist, Artwork, Follow, Wishlist, PurchaseInquiry,
  ApiResponse, PaginatedResponse, LoginForm, SignupForm,
  ArtistProfileForm, ArtworkForm, ArtworkFilters
} from '@/types';

// API 클라이언트 설정
const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 - 토큰 추가
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터 - 토큰 만료 처리
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (data: LoginForm): Promise<{ access: string; refresh: string }> => {
    const response = await apiClient.post('/accounts/login/', data);
    return response.data;
  },

  signup: async (data: SignupForm): Promise<ApiResponse<User>> => {
    const response = await apiClient.post('/accounts/signup/', data);
    return response.data;
  },

  refreshToken: async (refresh: string): Promise<{ access: string }> => {
    const response = await apiClient.post('/accounts/token/refresh/', { refresh });
    return response.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/accounts/logout/');
  },

  getProfile: async (): Promise<User> => {
    const response = await apiClient.get('/accounts/profile/');
    return response.data;
  },

  updateProfile: async (data: Partial<User>): Promise<User> => {
    const response = await apiClient.patch('/accounts/profile/', data);
    return response.data;
  },
};

// Artist API
export const artistAPI = {
  getArtists: async (params?: { featured?: boolean; search?: string }): Promise<PaginatedResponse<Artist>> => {
    const response = await apiClient.get('/artists/', { params });
    return response.data;
  },

  getArtist: async (id: number): Promise<Artist> => {
    const response = await apiClient.get(`/artists/${id}/`);
    return response.data;
  },

  createArtistProfile: async (data: ArtistProfileForm): Promise<Artist> => {
    const response = await apiClient.post('/artists/', data);
    return response.data;
  },

  updateArtistProfile: async (id: number, data: Partial<ArtistProfileForm>): Promise<Artist> => {
    const response = await apiClient.patch(`/artists/${id}/`, data);
    return response.data;
  },

  followArtist: async (artistId: number): Promise<Follow> => {
    const response = await apiClient.post('/artists/follow/', { artist_id: artistId });
    return response.data;
  },

  unfollowArtist: async (artistId: number): Promise<void> => {
    await apiClient.delete(`/artists/${artistId}/follow/`);
  },
};

// Artwork API
export const artworkAPI = {
  getArtworks: async (filters?: ArtworkFilters): Promise<PaginatedResponse<Artwork>> => {
    const response = await apiClient.get('/artworks/', { params: filters });
    return response.data;
  },

  getArtwork: async (id: number): Promise<Artwork> => {
    const response = await apiClient.get(`/artworks/${id}/`);
    return response.data;
  },

  createArtwork: async (data: ArtworkForm): Promise<Artwork> => {
    const response = await apiClient.post('/artworks/', data);
    return response.data;
  },

  updateArtwork: async (id: number, data: Partial<ArtworkForm>): Promise<Artwork> => {
    const response = await apiClient.patch(`/artworks/${id}/`, data);
    return response.data;
  },

  deleteArtwork: async (id: number): Promise<void> => {
    await apiClient.delete(`/artworks/${id}/`);
  },

  uploadArtworkImage: async (artworkId: number, file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('image', file);
    const response = await apiClient.post(`/artworks/${artworkId}/images/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
};

// Wishlist API
export const wishlistAPI = {
  getWishlist: async (): Promise<PaginatedResponse<Wishlist>> => {
    const response = await apiClient.get('/wishlist/');
    return response.data;
  },

  addToWishlist: async (artworkId: number): Promise<Wishlist> => {
    const response = await apiClient.post('/wishlist/', { artwork_id: artworkId });
    return response.data;
  },

  removeFromWishlist: async (artworkId: number): Promise<void> => {
    await apiClient.delete(`/wishlist/${artworkId}/`);
  },
};

// Purchase Inquiry API
export const purchaseInquiryAPI = {
  createInquiry: async (data: { artwork_id: number; message: string; contact_phone: string }): Promise<PurchaseInquiry> => {
    const response = await apiClient.post('/purchase-inquiries/', data);
    return response.data;
  },

  getInquiries: async (): Promise<PaginatedResponse<PurchaseInquiry>> => {
    const response = await apiClient.get('/purchase-inquiries/');
    return response.data;
  },

  getInquiry: async (id: number): Promise<PurchaseInquiry> => {
    const response = await apiClient.get(`/purchase-inquiries/${id}/`);
    return response.data;
  },
};

export default apiClient;
