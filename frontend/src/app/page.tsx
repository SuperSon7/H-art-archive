import HeroSection from '@/components/sections/HeroSection';
import ServicesSection from '@/components/sections/ServicesSection';
import AdvantagesSection from '@/components/sections/AdvantagesSection';
import ArtDiscoverySection from '@/components/sections/ArtDiscoverySection';
import Footer from '@/components/layout/Footer';

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <HeroSection />
      <ServicesSection />
      <AdvantagesSection />
      <ArtDiscoverySection />
      {/* <Footer /> */}
    </main>
  );
}
