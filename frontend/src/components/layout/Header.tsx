'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 100);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      const headerHeight = document.querySelector('header')?.offsetHeight || 0;
      const targetPosition = element.getBoundingClientRect().top + window.pageYOffset - headerHeight;

      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });

      setIsMenuOpen(false);
    }
  };

  return (
    <header className={`fixed top-0 w-full z-50 border-b border-gray-100 transition-all duration-300 ${
      isScrolled ? 'bg-white' : 'bg-white/95 backdrop-blur-sm'
    }`}>
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Image
            src="/images/logo_header.svg"
            alt="Solren Logo"
            width={40}
            height={40}
            className="h-10 w-auto"
          />
        </div>

        <div className="flex items-center space-x-6">
          <nav className="hidden md:flex items-center space-x-6">
            <button
              onClick={() => scrollToSection('services')}
              className="text-gray-700 hover:text-primary transition-colors font-medium"
            >
              서비스
            </button>
            <button
              onClick={() => scrollToSection('advantage')}
              className="text-gray-700 hover:text-primary transition-colors font-medium"
            >
              회사 소개
            </button>
            <button
              onClick={() => scrollToSection('explore')}
              className="text-gray-700 hover:text-primary transition-colors font-medium"
            >
              둘러보기
            </button>
          </nav>

          <div className="w-6 h-6 flex items-center justify-center cursor-pointer">
            <i className="ri-search-line text-xl text-gray-600 hover:text-primary transition-colors"></i>
          </div>

          {/* 로그인 버튼 */}
          <Link href="/login">
            <button className="hidden md:block bg-primary text-white px-6 py-2 rounded-lg hover:bg-primary/90 transition-all duration-300 transform hover:-translate-y-1">
              로그인
            </button>
          </Link>

          <div
            className="md:hidden w-6 h-6 flex items-center justify-center cursor-pointer"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <i className={`text-xl text-gray-700 ${isMenuOpen ? 'ri-close-line' : 'ri-menu-line'}`}></i>
          </div>
        </div>
      </div>

      {/* 모바일 메뉴 */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100 px-6 py-4">
          <nav className="flex flex-col gap-4 mb-4">
            <button
              onClick={() => scrollToSection('services')}
              className="text-gray-700 hover:text-primary transition-colors font-medium text-left"
            >
              서비스
            </button>
            <button
              onClick={() => scrollToSection('advantage')}
              className="text-gray-700 hover:text-primary transition-colors font-medium text-left"
            >
              회사 소개
            </button>
            <button
              onClick={() => scrollToSection('explore')}
              className="text-gray-700 hover:text-primary transition-colors font-medium text-left"
            >
              둘러보기
            </button>
          </nav>

          {/* 모바일 로그인 버튼 */}
          <Link href="/login">
            <button className="w-full bg-primary text-white px-6 py-3 rounded-lg hover:bg-primary/90 transition-all duration-300">
              로그인
            </button>
          </Link>
        </div>
      )}
    </header>
  );
}
