import Image from 'next/image';

export default function ArtDiscoverySection() {
  return (
    <section id="explore" className="min-h-screen flex items-center bg-white py-32">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-20">
          <h2 className="text-5xl md:text-6xl font-bold text-gray-900 mb-8">
            당신의 공간을 위한 <span className="text-secondary">새로운 예술</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            엄선된 신진 작가와 혁신적인 작품들로 당신의 삶과 공간에 새로운 영감을 불어넣습니다.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/20 to-primary/90 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"></div>
            <Image
              src="/images/aroundsection_1.jpg"
              alt="Art Discovery"
              width={400}
              height={600}
              className="w-full h-[600px] object-cover rounded-2xl"
            />
            <div className="absolute bottom-0 left-0 right-0 p-8 text-white transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
              <h3 className="text-2xl font-semibold mb-3">최첨단 예술</h3>
              <p className="text-gray-100 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                주류를 넘어서는 신진 아티스트와 혁신적인 작품을 가장 먼저 만나보고 소장하세요.
              </p>
            </div>
          </div>

          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/20 to-primary/90 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"></div>
            <Image
              src="/images/aroundsection_2.jpg"
              alt="Artist Growth"
              width={400}
              height={600}
              className="w-full h-[600px] object-cover rounded-2xl"
            />
            <div className="absolute bottom-0 left-0 right-0 p-8 text-white transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
              <h3 className="text-2xl font-semibold mb-3">성장 지원</h3>
              <p className="text-gray-100 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                아티스트의 잠재력을 현실로, 체계적인 육성 프로그램에 당신도 기여할 수 있습니다.
              </p>
            </div>
          </div>

          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/20 to-primary/90 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"></div>
            <Image
              src="/images/aroundsection_3.jpg"
              alt="Space Transformation"
              width={400}
              height={600}
              className="w-full h-[600px] object-cover rounded-2xl"
            />
            <div className="absolute bottom-0 left-0 right-0 p-8 text-white transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
              <h3 className="text-2xl font-semibold mb-3">공간의 변화</h3>
              <p className="text-gray-100 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                큐레이션된 컬렉션과 순환 전시로 개인과 기업 공간을 예술적으로 승화시키세요.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
