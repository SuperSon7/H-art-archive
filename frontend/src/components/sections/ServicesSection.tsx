export default function ServicesSection() {
  return (
    <section id="services" className="section-padding bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            솔렌의 혁신 서비스
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            최첨단 기술과 체계적인 지원으로 아티스트의 성공을 돕고, 예술 시장에 새로운 활력을 불어넣습니다.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <div className="service-card bg-gray-50 p-8 rounded-2xl">
            <div className="w-16 h-16 bg-primary/10 rounded-xl flex items-center justify-center mb-6">
              <i className="ri-user-star-line text-2xl text-primary"></i>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">디지털 아티스트 매니지먼트</h3>
            <p className="text-gray-600 leading-relaxed">
              포트폴리오 개발, 경력 상담, 전략적 파트너십을 통해 예술적 잠재력을 극대화하는 아티스트를 위한 종합적인 성장과 비즈니스 지원을 제공합니다.
            </p>
          </div>

          <div className="service-card bg-gray-50 p-8 rounded-2xl">
            <div className="w-16 h-16 bg-secondary/10 rounded-xl flex items-center justify-center mb-6">
              <i className="ri-gallery-line text-2xl text-secondary"></i>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">가상 갤러리 & 하이브리드 전시</h3>
            <p className="text-gray-600 leading-relaxed">
              최첨단 가상현실 기술로 전통적인 갤러리 공간과 연결되는 몰입형 온·오프라인 전시 경험을 제공합니다.
            </p>
          </div>

          <div className="service-card bg-gray-50 p-8 rounded-2xl">
            <div className="w-16 h-16 bg-primary/10 rounded-xl flex items-center justify-center mb-6">
              <i className="ri-refresh-line text-2xl text-primary"></i>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">구독형 아트 서비스</h3>
            <p className="text-gray-600 leading-relaxed">
              개인과 기업 고객을 위한 혁신적인 구독 모델. 프리미엄 작품 대여 솔루션으로 공간을 예술적으로 변화시킵니다.
            </p>
          </div>

          <div className="service-card bg-gray-50 p-8 rounded-2xl">
            <div className="w-16 h-16 bg-secondary/10 rounded-xl flex items-center justify-center mb-6">
              <i className="ri-global-line text-2xl text-secondary"></i>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">글로벌 아트 마켓 플랫폼</h3>
            <p className="text-gray-600 leading-relaxed">
              블록체인 기술을 기반으로 안전한 거래와 진품 인증이 가능한, 전 세계 아티스트와 컬렉터를 연결하는 국제 마켓플레이스입니다.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
