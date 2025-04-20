import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import AndroidVideoOverlay from './AndroidVideoOverlay';

const KeyboardiPhone = () => {
  const [showVideo, setShowVideo] = useState(false);
  const videoUrl = "https://drive.google.com/file/d/199oEZqlYxm7T35TIX1u8YeahrQGmksae/preview";

  return (
    <div className="max-w-4xl mx-auto p-6 prose">
      {showVideo && <AndroidVideoOverlay videoUrl={videoUrl} onClose={() => setShowVideo(false)} />}
      
      <h1 className="text-3xl font-bold">iPhone için Lazca Klavye Kurulumu</h1>
      
      <div className="mb-8 p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition cursor-pointer"
           onClick={() => setShowVideo(true)}>
        <div className="flex items-center text-blue-600 font-medium">
          <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path d="M6.3 2.841A1.5 1.5 0 004 4.11v11.78a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
          </svg>
          Video rehberi için buraya tıklayın
        </div>
        <p className="mt-2 text-sm">Tıklamadan önce 1. Adımdaki linke tıklayıp uygulamayı indiriniz.</p>
      </div>

      <ol className="list-decimal pl-6 space-y-8">
        {/* Step 1 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Keyman uygulamasını indirin</h3>
          <p>Alttaki linke tıklayıp uygulamayı indirin:</p>
          <a href="https://apps.apple.com/tr/app/keyman/id933676545?l=tr" 
             className="text-blue-600 break-all"
             target="_blank"
             rel="noopener noreferrer">
            https://apps.apple.com/tr/app/keyman/id933676545?l=tr
          </a>
        </li>

        {/* Step 2 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Dil ekleme</h3>
          <p>Keyman'ı açtıktan sonra <span className="font-bold">'Add a keyboard for your language'</span> (Klavyenize dil ekleyin) mesajına tıklayınız.</p>
          <img 
            src="/images/keyboard/iphone-step2.jpg" 
            alt="Add language screen"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 3 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Lazca klavye arama</h3>
          <p>Açılan yeni pencerenin üst kısmındaki arama kutusuna <span className="font-bold">'Laz'</span> yazınız.</p>
          <img 
            src="/images/keyboard/iphone-step3.jpg" 
            alt="Search for Laz keyboard"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 4 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Doğru klavyeyi seçin</h3>
          <p>Alttaki <span className="font-bold bg-yellow-100 px-1">'Laz'</span> seçeneğine tıklayınız (<span className="text-red-500">Lazca Klavye değil!</span>).</p>
          <img 
            src="/images/keyboard/iphone-step4.jpg" 
            alt="Select Laz keyboard"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 5 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Klavyeyi yükleyin</h3>
          <p><span className="font-bold">'Install keyboard'</span> (klavyeyi yükleyin) butonuna basınız.</p>
          <img 
            src="/images/keyboard/iphone-step5.jpg" 
            alt="Install keyboard button"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 6 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Yükleme onayı</h3>
          <p>Yeni açılan pencerede <span className="font-bold">'INSTALL'</span> (Yükle)'a tıklayınız.</p>
          <img 
            src="/images/keyboard/iphone-step6.jpg" 
            alt="Install confirmation"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 7 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Bilgi penceresi</h3>
          <p>Yükledikten sonra klavye hakkında bir bilgi penceresi açılacak.</p>
          <img 
            src="/images/keyboard/iphone-step7.jpg" 
            alt="Keyboard info screen"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
          <p>
            Detaylı bilgiler için{' '}
            <a href="https://docs.google.com/document/d/1Tl0z-AFTk9S2usQ-ZLIEnm_wM9-oo8zQR0y3oeX4ZRg/edit#heading=h.vmno25izkhpx" 
               className="text-blue-600"
               target="_blank"
               rel="noopener noreferrer">
              bu sayfayı
            </a> ziyaret edin
          </p>
        </li>

        {/* Step 8 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">iPhone ayarlarına geçiş</h3>
          <p>Uygulamadan çıkıp iPhone'nun genel ayarlar kısmına geçin. <span className="font-bold">Klavyeler</span>'i açın ve Klavyeler'e tıklayın.</p>
          <img 
            src="/images/keyboard/iphone-step8.jpg" 
            alt="iPhone settings"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 9 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Keyman'ı seçin</h3>
          <p>'Keyman'a tıklayın.</p>
          <img 
            src="/images/keyboard/iphone-step9.jpg" 
            alt="Select Keyman"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 10 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Tam erişim izni</h3>
          <p>'Tam Erişime İzin Ver' butonuna tıklayın.</p>
          <img 
            src="/images/keyboard/iphone-step10.jpg" 
            alt="Full access permission"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 11 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Ayarlara erişim</h3>
          <p>Şu an klavyeniz çok kısa bir şekilde ve sadece bu uygulama içinde kullanılmaktadır. Bunu değiştirmek için üstteki üç noktaya tıklayın...</p>
          <img 
            src="/images/keyboard/iphone-step11.jpg" 
            alt="Access settings"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 12 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Ayarlar menüsü</h3>
          <p>... ve buradan <span className="font-bold">'Settings'</span> (Ayarlar) kısmına geçin.</p>
          <img 
            src="/images/keyboard/iphone-step12.jpg" 
            alt="Settings menu"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 13 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Klavye yüksekliği ayarı</h3>
          <p>Alttaki <span className="font-bold">'Adjust keyboard height'</span> (Klavyenin büyüklüğünü ayarlayın) ayarına tıklayın.</p>
          <img 
            src="/images/keyboard/iphone-step13.jpg" 
            alt="Keyboard height adjustment"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 14 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Klavye boyutunu ayarlayın</h3>
          <p>Burada, noktalı çizgiyi çekip isteğinize göre büyüklüğü seçebilirsiniz.</p>
          <img 
            src="/images/keyboard/iphone-step14.jpg" 
            alt="Adjust keyboard size"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Step 15 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Kurulum tamamlandı!</h3>
          <div className="bg-green-100 p-4 rounded-lg">
            <p className="font-bold">Klavye-skani xažiri ren! (Klavyeniz hazır!)</p>
            <p>Keyman'deki İngilizce klavyeyi kaldırmak isterseniz aşağıdaki adımları izleyin.</p>
          </div>
          <img 
            src="/images/keyboard/iphone-step15.jpg" 
            alt="Keyboard ready"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        {/* Steps 16-21 for removing English keyboard */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">İngilizce klavyeyi kaldırma</h3>
          <p>Tekrardan üç noktaya tıklayıp...</p>
          <img 
            src="/images/keyboard/iphone-step11.jpg" 
            alt="Three dots menu"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        <li className="pl-2">
          <p><span className="font-bold">'Settings'</span> (Ayarlar) kısmına geri dönün.</p>
          <img 
            src="/images/keyboard/iphone-step17.jpg" 
            alt="Settings menu"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        <li className="pl-2">
          <p>Bu sefer, <span className="font-bold">'installed languages (2)'</span> (yüklenen diller) kısmına girin.</p>
          <img 
            src="/images/keyboard/iphone-step18.jpg" 
            alt="Installed languages"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        <li className="pl-2">
          <p><span className="font-bold">English</span> (İngilizce)'i seçip...</p>
          <img 
            src="/images/keyboard/iphone-step19.jpg" 
            alt="Select English"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        <li className="pl-2">
          <p><span className="font-bold">EuroLatin (SIL) Keyboard</span>'a tıklayıp...</p>
          <img 
            src="/images/keyboard/iphone-step20.jpg" 
            alt="Select EuroLatin keyboard"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>

        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">İngilizce klavyeyi kaldırın</h3>
          <p><span className="font-bold">'Uninstall keyboard'</span> (klavyeyi kaldırın)'a tıklayın ve İngilizce klavyeyi silin!</p>
          <img 
            src="/images/keyboard/iphone-step21.jpg" 
            alt="Uninstall English keyboard"
            className="border rounded-lg my-4 shadow-md max-w-xs"
          />
        </li>
      </ol>

      <div className="mt-12 p-4 bg-blue-50 rounded-lg flex justify-between">
        <Link to="/keyboard" className="text-blue-600 font-medium">
          ← Klavye Rehberine Dön
        </Link>
        <a href="https://docs.google.com/document/d/1Tl0z-AFTk9S2usQ-ZLIEnm_wM9-oo8zQR0y3oeX4ZRg/edit#heading=h.vmno25izkhpx" 
           className="text-blue-600 font-medium"
           target="_blank"
           rel="noopener noreferrer">
          Lazca Klavye Kullanım Kılavuzu →
        </a>
      </div>
    </div>
  );
};

export default KeyboardiPhone;