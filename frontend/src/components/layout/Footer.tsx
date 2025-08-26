import Image from 'next/image';

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white section-padding footer">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid md:grid-cols-4 gap-8 mb-12">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Image
                src="/images/logo_footer.svg"
                alt="Solren Logo"
                width={40}
                height={40}
                className="h-10 w-auto"
              />
            </div>
            <p className="text-gray-400 mb-6">
              혁신적인 매니지먼트와 글로벌 시장 진출을 통해 차세대 아티스트들의 성장을 지원합니다.
            </p>
            <div className="flex space-x-4">
              <div className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors cursor-pointer">
                <i className="ri-instagram-line text-lg"></i>
              </div>
              <div className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors cursor-pointer">
                <i className="ri-twitter-line text-lg"></i>
              </div>
              <div className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors cursor-pointer">
                <i className="ri-linkedin-line text-lg"></i>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">아티스트</h3>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">아티스트 지원</a></li>
              <li><a href="#" className="hover:text-white transition-colors">포트폴리오 가이드</a></li>
              <li><a href="#" className="hover:text-white transition-colors">성공 사례</a></li>
              <li><a href="#" className="hover:text-white transition-colors">자료실</a></li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">컬렉터</h3>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">작품 둘러보기</a></li>
              <li><a href="#" className="hover:text-white transition-colors">구독 플랜</a></li>
              <li><a href="#" className="hover:text-white transition-colors">투자 가이드</a></li>
              <li><a href="#" className="hover:text-white transition-colors">진품 인증</a></li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">회사 소개</h3>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">회사 소개</a></li>
              <li><a href="#" className="hover:text-white transition-colors">제휴 문의</a></li>
              <li><a href="#" className="hover:text-white transition-colors">보도자료</a></li>
              <li><a href="#" className="hover:text-white transition-colors">연락처</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm">
            © 2025 솔렌. All rights reserved.
          </p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <a href="#" className="text-gray-400 hover:text-white transition-colors text-sm">이용약관</a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors text-sm">개인정보처리방침</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
