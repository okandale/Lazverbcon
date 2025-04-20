import React from 'react';
import { Link } from 'react-router-dom';

const KeyboardMAC = () => {
  return (
    <div className="max-w-4xl mx-auto p-6 prose">
      <h1 className="text-3xl font-bold">Mac için Lazca Klavye Kurulum Rehberi</h1>
      
      <div className="my-4 bg-blue-50 p-4 rounded-lg">
        <h2 className="text-xl font-semibold">Keyman ile Lazca Klavye Kurulumu</h2>
        <p>Bu rehberde Mac bilgisayarınıza Lazca klavye düzenini nasıl kuracağınız adım adım anlatılmaktadır.</p>
      </div>

      <div className="space-y-8">
        {/* Step 1 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">1. Keyman'ı İndirin</h3>
          <p>Alttaki linke tıklayarak Keyman uygulamasını indirin:</p>
          <a 
            href="https://keyman.com/mac/download" 
            className="text-blue-600 font-medium block my-2"
            target="_blank"
            rel="noopener noreferrer"
          >
            Download Keyman for Mac
          </a>
        </div>

        {/* Step 2 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">2. İndirme Butonuna Tıklayın</h3>
          <p>'Download Now' (şimdi indirin) butonuna tıklayınız.</p>
          <img 
            src="/images/keyboard/mac-step2.jpg" 
            alt="Keyman indirme butonu"
            className="border rounded-lg my-2 shadow-md"
          />
        </div>

        {/* Step 3 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">3. DMG Dosyasını Açın</h3>
          <p>İndirdikten sonra "İndirilenler" klasöründeki 'keyman-...dmg' dosyasını bulup çift tıklayarak açın.</p>
          <img 
            src="/images/keyboard/mac-step3.jpg" 
            alt="DMG dosyasını açma"
            className="border rounded-lg my-2 shadow-md"
          />
        </div>

        {/* Step 4 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">4. Güvenlik Uyarısını Onaylayın</h3>
          <p>Çıkan güvenlik uyarısında yüklemek için izin veriniz.</p>
          <img 
            src="/images/keyboard/mac-step4.jpg" 
            alt="Güvenlik uyarısı"
            className="border rounded-lg my-2 shadow-md"
          />
        </div>

        {/* Step 5 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">5. Keyman'ı Yükleyin</h3>
          <p>Açılan yükleme penceresinde 'Install' (Yükle) butonuna tıklayın.</p>
          <img 
            src="/images/keyboard/mac-step5.jpg" 
            alt="Keyman yükleme ekranı"
            className="border rounded-lg my-2 shadow-md"
          />
        </div>

        {/* Step 6 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">6. Sistem Ayarlarını Onaylayın</h3>
          <p>Yükleme tamamlandığında, sistem ayarlarında 'Install Keyman' seçeneğini onaylayın.</p>
          <img 
            src="/images/keyboard/mac-step6.jpg" 
            alt="Sistem ayarları onayı"
            className="border rounded-lg my-2 shadow-md"
          />
        </div>

        {/* Step 7 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">7. Kurulum Tamamlandı</h3>
          <p>Türkçe ve Keyman klavyesi yüklendi. 'Bitti' butonuna tıklayınız.</p>
          <img 
            src="/images/keyboard/mac-step7.jpg" 
            alt="Kurulum tamamlandı ekranı"
            className="border rounded-lg my-2 shadow-md"
          />
        </div>

        {/* Step 8 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">8. Lazca Klavye Paketini İndirin</h3>
          <p>Aşağıdaki linkten Lazca klavye paketini indirin:</p>
          <a 
            href="https://keyman.com/keyboards/laz" 
            className="text-blue-600 font-medium block my-2"
            target="_blank"
            rel="noopener noreferrer"
          >
            Lazca Klavye Paketini İndir
          </a>
          <img 
            src="/images/keyboard/mac-step8.jpg" 
            alt="Lazca klavye indirme sayfası"
            className="border rounded-lg my-2 shadow-md"
          />
        </div>

        {/* Step 9 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">9. Lazca Klavyeyi Yükleyin</h3>
          <p>İndirdiğiniz 'laz.kmp' dosyasını açın ve çıkan pencerede 'Install' (Yükle) butonuna tıklayın.</p>
          <img 
            src="/images/keyboard/mac-step9.jpg" 
            alt="Lazca klavye yükleme ekranı"
            className="border rounded-lg my-2 shadow-md"
          />
        </div>

        {/* Step 10 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">10. Lazca Klavyeyi Etkinleştirin</h3>
          <p>Keyman penceresinde Lazca klavyenin yanındaki kutuyu işaretleyerek etkinleştirin.</p>
          <img 
            src="/images/keyboard/mac-step10.jpg" 
            alt="Klavye etkinleştirme ekranı"
            className="border rounded-lg my-2 shadow-md"
          />
        </div>

        {/* Step 11 */}
        <div className="border-l-4 border-blue-500 pl-4">
          <h3 className="text-xl font-semibold">11. Klavyeyi Kullanmaya Başlayın</h3>
          <p>Mac'inizde Lazca klavyeye geçmek için:</p>
          <ul className="list-disc pl-6 space-y-1 my-2">
            <li>Üst sağdaki klavye simgesine tıklayın</li>
            <li>'Laz' seçeneğini seçin</li>
          </ul>
          <img 
            src="/images/keyboard/mac-step11.jpg" 
            alt="Klavye değiştirme ekranı"
            className="border rounded-lg my-2 shadow-md"
          />
        </div>

        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-xl font-semibold">Kurulum Tamamlandı!</h3>
          <p>Artık Mac'inizde Lazca yazabilirsiniz. Klavyeyi nasıl kullanacağınızı öğrenmek için:</p>
          <Link to="/keyboard/computer" className="text-blue-600 font-medium block mt-2">
            Mac için Klavye Kullanım Rehberi →
          </Link>
        </div>
      </div>

      <div className="mt-8 p-4 bg-blue-50 rounded-lg flex justify-between">
        <Link to="/keyboard" className="text-blue-600 font-medium">
          ← Klavye Rehberine Dön
        </Link>
        <a href="#" className="text-blue-600 font-medium">
          Video Rehberi İzle →
        </a>
      </div>
    </div>
  );
};

export default KeyboardMAC;