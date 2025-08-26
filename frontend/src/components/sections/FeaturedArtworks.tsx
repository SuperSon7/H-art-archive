'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { artworkAPI } from '@/lib/api';
import { Artwork } from '@/types';
import { formatPrice, getCategoryName } from '@/lib/utils';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

export default function FeaturedArtworks() {
  const [artworks, setArtworks] = useState<Artwork[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFeaturedArtworks = async () => {
      try {
        setLoading(true);
        const response = await artworkAPI.getArtworks({ featured: true });
        setArtworks(response.results.slice(0, 6)); // 최대 6개 작품만 표시
      } catch (error) {
        console.error('추천 작품을 불러오는데 실패했습니다:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFeaturedArtworks();
  }, []);

  if (loading) {
    return <LoadingSpinner size="lg" className="py-12" />;
  }

  if (artworks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">추천 작품이 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {artworks.map((artwork) => (
        <Link
          key={artwork.id}
          href={`/artworks/${artwork.id}`}
          className="group block"
        >
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden transition-all duration-300 group-hover:shadow-lg group-hover:scale-[1.02]">
            <div className="relative aspect-square overflow-hidden">
              {artwork.cover_image ? (
                <Image
                  src={artwork.cover_image.image_url}
                  alt={artwork.title}
                  fill
                  className="object-cover transition-transform duration-300 group-hover:scale-110"
                  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
              ) : (
                <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                  <svg className="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              )}

              {/* 카테고리 태그 */}
              <div className="absolute top-3 left-3">
                <span className="bg-primary-500 text-white text-xs px-2 py-1 rounded-full">
                  {getCategoryName(artwork.category)}
                </span>
              </div>
            </div>

            <div className="p-4">
              <h3 className="font-semibold text-lg text-gray-800 mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">
                {artwork.title}
              </h3>

              <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                {artwork.artist.artist_name}
              </p>

              <div className="flex justify-between items-center">
                <div className="text-sm text-gray-500">
                  {artwork.year_created}년
                </div>

                {artwork.price_krw && (
                  <div className="font-semibold text-primary-600">
                    {formatPrice(artwork.price_krw, 'KRW')}
                  </div>
                )}
              </div>
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
