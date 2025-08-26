import Image from 'next/image';
import Link from 'next/link';

export default function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center overflow-hidden">
      {/* Background Image */}
      <Image
        src="/images/herosection_back.jpg"
        alt="hero background"
        fill
        className="absolute inset-0 w-full h-full object-cover z-0"
        priority
      />

      {/* Overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-black/70 via-black/50 to-transparent z-10"></div>

      {/* Content */}
      <div className="relative z-20 max-w-7xl mx-auto px-6 w-full">
        <div className="max-w-2xl">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight whitespace-nowrap">
            예술의 혁신을 <span className="text-secondary">함께하다</span>, 솔렌
          </h1>
          <p className="text-xl md:text-2xl text-gray-200 leading-relaxed mb-8">
            신진 아티스트의 성장을 위한 혁신적인 매니지먼트. 글로벌 시장 진출을 통해 예술의 새로운 패러다임을 함께 만들어갑니다.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            <Link href="/login">
              <button className="bg-secondary text-gray-900 hover:bg-secondary/90 px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 transform hover:-translate-y-1">
                시작하기
              </button>
            </Link>
            <Link href="#services">
              <button className="border-2 border-white text-white hover:bg-white hover:text-gray-900 px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 transform hover:-translate-y-1">
                서비스 둘러보기
              </button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
