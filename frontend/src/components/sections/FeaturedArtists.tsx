'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { artistAPI } from '@/lib/api';
import { Artist } from '@/types';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

export default function FeaturedArtists() {
  const [artists, setArtists] = useState<Artist[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFeaturedArtists = async () => {
      try {
        setLoading(true);
        const response = await artistAPI.getArtists({ featured: true });
        setArtists(response.results.slice(0, 6)); // 최대 6명의 작가만 표시
      } catch (error) {
        console.error('추천 작가를 불러오는데 실패했습니다:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFeaturedArtists();
  }, []);

  if (loading) {
    return <LoadingSpinner size="lg" className="py-12" />;
  }

  if (artists.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">추천 작가가 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {artists.map((artist) => (
        <Link
          key={artist.id}
          href={`/artists/${artist.id}`}
          className="group block"
        >
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden transition-all duration-300 group-hover:shadow-lg group-hover:scale-[1.02]">
            <div className="relative aspect-square overflow-hidden">
              {artist.main_image_url ? (
                <Image
                  src={artist.main_image_url}
                  alt={artist.artist_name}
                  fill
                  className="object-cover transition-transform duration-300 group-hover:scale-110"
                  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
              ) : (
                <div className="w-full h-full bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
                  <svg className="w-20 h-20 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
              )}

              {/* 추천 작가 배지 */}
              {artist.is_featured && (
                <div className="absolute top-3 right-3">
                  <span className="bg-accent-500 text-white text-xs px-2 py-1 rounded-full">
                    추천
                  </span>
                </div>
              )}
            </div>

            <div className="p-4">
              <h3 className="font-semibold text-lg text-gray-800 mb-2 group-hover:text-primary-600 transition-colors">
                {artist.artist_name}
              </h3>

              {artist.artist_note && (
                <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                  {artist.artist_note}
                </p>
              )}

              <div className="flex justify-between items-center text-sm text-gray-500">
                <span>작품 {artist.artwork_count}개</span>
                <span>팔로워 {artist.follower_count}명</span>
              </div>
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
