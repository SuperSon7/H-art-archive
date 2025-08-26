import { create } from 'zustand';
import { Artwork, ArtworkFilters } from '@/types';

interface ArtworkState {
  artworks: Artwork[];
  featuredArtworks: Artwork[];
  currentArtwork: Artwork | null;
  filters: ArtworkFilters;
  isLoading: boolean;
  totalCount: number;
  currentPage: number;
}

interface ArtworkActions {
  setArtworks: (artworks: Artwork[]) => void;
  setFeaturedArtworks: (artworks: Artwork[]) => void;
  setCurrentArtwork: (artwork: Artwork | null) => void;
  setFilters: (filters: Partial<ArtworkFilters>) => void;
  clearFilters: () => void;
  setLoading: (loading: boolean) => void;
  setTotalCount: (count: number) => void;
  setCurrentPage: (page: number) => void;
  addToArtworks: (artwork: Artwork) => void;
  updateArtwork: (id: number, updates: Partial<Artwork>) => void;
  removeArtwork: (id: number) => void;
}

type ArtworkStore = ArtworkState & ArtworkActions;

const initialFilters: ArtworkFilters = {
  category: undefined,
  price_min: undefined,
  price_max: undefined,
  year_min: undefined,
  year_max: undefined,
  materials: undefined,
  artist_id: undefined,
  search: undefined,
};

export const useArtworkStore = create<ArtworkStore>((set, get) => ({
  // State
  artworks: [],
  featuredArtworks: [],
  currentArtwork: null,
  filters: initialFilters,
  isLoading: false,
  totalCount: 0,
  currentPage: 1,

  // Actions
  setArtworks: (artworks: Artwork[]) =>
    set({
      artworks,
    }),

  setFeaturedArtworks: (artworks: Artwork[]) =>
    set({
      featuredArtworks: artworks,
    }),

  setCurrentArtwork: (artwork: Artwork | null) =>
    set({
      currentArtwork: artwork,
    }),

  setFilters: (filters: Partial<ArtworkFilters>) =>
    set((state) => ({
      filters: { ...state.filters, ...filters },
      currentPage: 1, // 필터 변경 시 첫 페이지로
    })),

  clearFilters: () =>
    set({
      filters: initialFilters,
      currentPage: 1,
    }),

  setLoading: (loading: boolean) =>
    set({
      isLoading: loading,
    }),

  setTotalCount: (count: number) =>
    set({
      totalCount: count,
    }),

  setCurrentPage: (page: number) =>
    set({
      currentPage: page,
    }),

  addToArtworks: (artwork: Artwork) =>
    set((state) => ({
      artworks: [artwork, ...state.artworks],
    })),

  updateArtwork: (id: number, updates: Partial<Artwork>) =>
    set((state) => ({
      artworks: state.artworks.map((artwork) =>
        artwork.id === id ? { ...artwork, ...updates } : artwork
      ),
      featuredArtworks: state.featuredArtworks.map((artwork) =>
        artwork.id === id ? { ...artwork, ...updates } : artwork
      ),
      currentArtwork: state.currentArtwork?.id === id
        ? { ...state.currentArtwork, ...updates }
        : state.currentArtwork,
    })),

  removeArtwork: (id: number) =>
    set((state) => ({
      artworks: state.artworks.filter((artwork) => artwork.id !== id),
      featuredArtworks: state.featuredArtworks.filter((artwork) => artwork.id !== id),
      currentArtwork: state.currentArtwork?.id === id ? null : state.currentArtwork,
    })),
}));
