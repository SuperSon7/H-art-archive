export default function AdvantagesSection() {
  return (
    <section id="advantage" className="min-h-screen flex items-center bg-primary text-white py-32">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-20">
          <h2 className="text-5xl md:text-6xl font-bold mb-8">
            솔렌의 <span className="text-secondary">장점</span>
          </h2>
          <p className="text-xl text-gray-200 max-w-3xl mx-auto">
            솔렌은 신진 작가들이 겪는 구조적 한계를 넘어, 예술가로서 온전히 자립하고 성장할 수 있도록 돕습니다.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-12">
          <div className="bg-white/5 backdrop-blur-sm p-12 rounded-2xl hover:transform hover:-translate-y-2 transition-all duration-300">
            <div className="w-16 h-16 bg-secondary/20 rounded-xl flex items-center justify-center mb-8">
              <i className="ri-funds-line text-3xl text-secondary"></i>
            </div>
            <h3 className="text-2xl font-semibold mb-4">다양한 수익 창출</h3>
            <p className="text-gray-300 leading-relaxed">
              전시, 판매, 대여, 디지털 라이선싱을 통한 다양한 수입 기회를 제공합니다. 우리 플랫폼은 아티스트들의 수익 잠재력을 극대화합니다.
            </p>
          </div>

          <div className="bg-white/5 backdrop-blur-sm p-12 rounded-2xl hover:transform hover:-translate-y-2 transition-all duration-300">
            <div className="w-16 h-16 bg-secondary/20 rounded-xl flex items-center justify-center mb-8">
              <i className="ri-global-line text-3xl text-secondary"></i>
            </div>
            <h3 className="text-2xl font-semibold mb-4">글로벌 시장 진출</h3>
            <p className="text-gray-300 leading-relaxed">
              공정한 가격과 투명한 거래 과정으로 국제 컬렉터와 직접 연결됩니다. 국경을 넘어 여러분의 영향력을 확장하세요.
            </p>
          </div>

          <div className="bg-white/5 backdrop-blur-sm p-12 rounded-2xl hover:transform hover:-translate-y-2 transition-all duration-300">
            <div className="w-16 h-16 bg-secondary/20 rounded-xl flex items-center justify-center mb-8">
              <i className="ri-shield-star-line text-3xl text-secondary"></i>
            </div>
            <h3 className="text-2xl font-semibold mb-4">매니지먼트 지원</h3>
            <p className="text-gray-300 leading-relaxed">
              마케팅, 법률 지원, 경력 전략 가이드를 포함한 종합적인 아티스트 육성을 지원합니다. 비즈니스는 우리가 담당하니, 여러분은 예술 창작에만 집중하세요.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
