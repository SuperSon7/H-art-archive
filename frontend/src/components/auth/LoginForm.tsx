'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // TODO: 로그인 로직 구현
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary via-primary/90 to-primary/80 relative overflow-hidden">
      {/* 배경 패턴 */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30px_30px,rgba(255,255,255,0.1)_2px,transparent_2px)] bg-[length:60px_60px]"></div>
      </div>

      {/* 로고 영역 */}
      <div className="absolute top-8 left-8 z-10">
        <Link href="/" className="flex items-center gap-2">
          <Image
            src="/images/logo_header.svg"
            alt="Solren Logo"
            width={32}
            height={32}
            className="h-8 w-auto"
          />
          <span className="text-white font-semibold text-lg">솔렌</span>
        </Link>
      </div>

      {/* 메인 로그인 폼 */}
      <div className="relative z-20 w-full max-w-md mx-6">
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          {/* 제목 */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">로그인</h1>
            <p className="text-gray-600">솔렌과 함께 예술의 여정을 시작하세요</p>
          </div>

          {/* 새 사용자 링크 */}
          <div className="text-center mb-6">
            <span className="text-gray-600">새로운 사용자신가요? </span>
            <Link href="/signup" className="text-primary hover:text-primary/80 font-medium transition-colors">
              계정 만들기
            </Link>
          </div>

          {/* 이메일 로그인 폼 */}
          <form onSubmit={handleSubmit} className="mb-6">
            <div className="mb-4">
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                이메일 주소
              </label>
              <div className="flex gap-3">
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-300"
                  placeholder="your@email.com"
                  required
                />
                <button
                  type="submit"
                  disabled={isLoading || !email}
                  className="px-6 py-3 bg-primary text-white font-medium rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:-translate-y-1"
                >
                  {isLoading ? (
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  ) : (
                    '계속'
                  )}
                </button>
              </div>
            </div>
          </form>

          {/* 구분선 */}
          <div className="relative mb-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">또는</span>
            </div>
          </div>

          {/* 소셜 로그인 옵션 */}
          <div className="space-y-3 mb-6">
            <button className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-all duration-300 transform hover:-translate-y-1">
              <i className="ri-google-fill text-xl text-red-500"></i>
              <span className="font-medium text-gray-700">Google로 계속</span>
            </button>

            <button className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-all duration-300 transform hover:-translate-y-1">
              <i className="ri-kakao-talk-fill text-xl text-yellow-400"></i>
              <span className="font-medium text-gray-700">Kakao로 계속</span>
            </button>

            <button className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-all duration-300 transform hover:-translate-y-1">
              <i className="ri-apple-fill text-xl text-gray-900"></i>
              <span className="font-medium text-gray-700">Apple로 계속</span>
            </button>
          </div>

          {/* 추가 옵션 */}
          <div className="text-center space-y-3">
            <Link href="/more-options" className="block text-primary hover:text-primary/80 text-sm font-medium transition-colors">
              더 많은 로그인 옵션
            </Link>
            <Link href="/help" className="block text-primary hover:text-primary/80 text-sm font-medium transition-colors">
              로그인 도움말 보기
            </Link>
          </div>
        </div>
      </div>

      {/* 하단 푸터 */}
      <div className="absolute bottom-8 left-8 right-8 z-10">
        <div className="flex flex-col md:flex-row justify-between items-center text-white/80 text-sm">
          <div className="mb-4 md:mb-0">
            <span className="font-medium">© 2025 솔렌. All rights reserved.</span>
          </div>
          <div className="flex space-x-6">
            <Link href="/terms" className="hover:text-white transition-colors">이용약관</Link>
            <Link href="/privacy" className="hover:text-white transition-colors">개인정보처리방침</Link>
            <Link href="/cookies" className="hover:text-white transition-colors">쿠키 설정</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
