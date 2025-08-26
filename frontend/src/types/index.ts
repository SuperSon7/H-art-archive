// User Types
export interface User {
  id: number;
  email: string;
  username: string;
  user_type: 'ARTIST' | 'COLLECTOR';
  is_active: boolean;
  is_staff: boolean;
  created_at: string;
  updated_at: string;
  agree_terms: boolean;
  agree_privacy: boolean;
  profile_image_url?: string;
  social_type?: string;
  social_id?: string;
}

// Artist Types
export interface Artist {
  id: number;
  approval_status: 'PENDING' | 'APPROVED' | 'REJECTED';
  artist_name: string;
  artist_note?: string;
  user: User;
  main_image_url?: string;
  artwork_count: number;
  follower_count: number;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

// Artwork Types
export interface Artwork {
  id: number;
  title: string;
  description?: string;
  artist: Artist;
  cover_image?: ArtworkImage;
  year_created: number;
  price_krw?: number;
  price_usd?: number;
  materials: string;
  width: number;
  height: number;
  depth?: number;
  dimension_unit: 'cm' | 'inch';
  category: ArtworkCategory;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export type ArtworkCategory =
  | 'painting' | 'oriental_painting' | 'sculpture' | 'printmaking'
  | 'wood_craft' | 'ceramics' | 'metal_craft' | 'photography'
  | 'digital' | 'mixed_media';

export interface ArtworkImage {
  id: number;
  image_url: string;
  is_primary: boolean;
  created_at: string;
}

// Interaction Types
export interface Follow {
  id: number;
  follower: User;
  following: Artist;
  created_at: string;
}

export interface Wishlist {
  id: number;
  user: User;
  artwork: Artwork;
  created_at: string;
}

export interface PurchaseInquiry {
  id: number;
  inquirer: User;
  artwork: Artwork;
  message: string;
  contact_phone: string;
  status: 'pending' | 'responded' | 'completed' | 'cancelled';
  artist_response?: string;
  created_at: string;
  updated_at: string;
  responded_at?: string;
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

// Form Types
export interface LoginForm {
  email: string;
  password: string;
}

export interface SignupForm {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  user_type: 'ARTIST' | 'COLLECTOR';
  agree_terms: boolean;
  agree_privacy: boolean;
}

export interface ArtistProfileForm {
  artist_name: string;
  artist_note?: string;
  main_image_url?: string;
}

export interface ArtworkForm {
  title: string;
  description?: string;
  year_created: number;
  price_krw?: number;
  price_usd?: number;
  materials: string;
  width: number;
  height: number;
  depth?: number;
  dimension_unit: 'cm' | 'inch';
  category: ArtworkCategory;
}

// Filter Types
export interface ArtworkFilters {
  category?: ArtworkCategory;
  price_min?: number;
  price_max?: number;
  year_min?: number;
  year_max?: number;
  materials?: string;
  artist_id?: number;
  search?: string;
}

// Notification Types
export interface Notification {
  id: number;
  user: User;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}
