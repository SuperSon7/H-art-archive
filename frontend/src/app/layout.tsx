import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: '솔렌 - 예술의 혁신을 함께하다',
  description: '신진 아티스트의 성장을 위한 혁신적인 매니지먼트. 글로벌 시장 진출을 통해 예술의 새로운 패러다임을 함께 만들어갑니다.',
  keywords: ['아트', '매니지먼트', '갤러리', '아티스트', '전시', '아트마켓'],
  authors: [{ name: '솔렌 팀' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body className={inter.className}>
        <div className="min-h-screen bg-white">
          <Header />
          <main>{children}</main>
          <Footer />
        </div>
      </body>
    </html>
  )
}
