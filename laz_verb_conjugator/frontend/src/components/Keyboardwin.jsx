import React from 'react';
import { Link } from 'react-router-dom';

const KeyboardWin = () => {
  return (
    <div className="max-w-4xl mx-auto p-6 prose">
      <h1 className="text-3xl font-bold">Windows için Lazca Klavye Kurulumu</h1>
      
      <div className="mb-8 p-4 bg-blue-50 rounded-lg">
        <a href="#" className="text-blue-600 font-medium">📹 Video rehberi için buraya tıklayın</a>
      </div>

      <ol className="list-decimal pl-6 space-y-8">
        {/* Step 1 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Alttaki linke tıklayınız:</h3>
          <a href="https://keyman.com/windows/download" 
             className="text-blue-600 break-all">
            https://keyman.com/windows/download
          </a>
        </li>

        {/* Step 2 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">‘Download Now’ (şimdi indirin) butonuna tıklayınız. Biraz aşağıya doğru kaydırmanız gerekebilir. </h3>
          <img 
            src="/images/keyboard/windows-step1.jpg" 
            alt="Download page screenshot"
            className="border rounded-lg my-4 shadow-md"
          />
        </li>

        {/* Step 3 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">İndirdikten sonra “İndirilenler” klasörünüzünde ‘keyman-…exe’ programı bulunmaktadır. Tıklayıp yükleyiniz.</h3>
          <img 
            src="/images/keyboard/windows-step2.jpg" 
            alt="Downloaded executable"
            className="border rounded-lg my-4 shadow-md max-w-md"
          />
        </li>

        {/* Step 4 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Uyarı penceresi açılacak. Yüklemek için izin veriniz.</h3>
        </li>

        {/* Step 5 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Keyman’ın yükleme penceresi açılacak ve ‘Install’(Yükleyin)’a tıklayınız.</h3>
          <img 
            src="/images/keyboard/windows-step3.jpg" 
            alt="Installation screen"
            className="border rounded-lg my-4 shadow-md max-w-md"
          />
        </li>

        {/* Step 6 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Yükledikten sonra yeni pencere açılacak. ‘Start Keyman’ (Keyman’ı başlat) butonuna tıklayınız.</h3>
          <img 
            src="/images/keyboard/windows-step4.jpg" 
            alt="Completion screen"
            className="border rounded-lg my-4 shadow-md max-w-md"
          />
        </li>

        {/* Step 7 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Lazca klavye paketini indirin:</h3>
          <a href="https://keyman.com/keyboards/laz" 
             className="text-blue-600 break-all">
            https://keyman.com/keyboards/laz
          </a>
          <img 
            src="/images/keyboard/windows-step5.jpg" 
            alt="Keyboard download page"
            className="border rounded-lg my-4 shadow-md"
          />
        </li>

        {/* Step 8 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">‘Open Keyman Configuration?’ (Keyman ayarla kısmını açılacak mı?) diye bir pencere açılacak ve ‘Open Keyman Configuration’ (Keyman ayarla kısmını açın) mesajına tıklayınız.</h3>
          <img 
            src="/images/keyboard/windows-step6.jpg" 
            alt="Configuration prompt"
            className="border rounded-lg my-4 shadow-md max-w-md"
          />
        </li>

        {/* Step 9 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Lazca klavyesi için bir yükleme penceresi açılacak ve ‘Install’ seçiniz. Dikkat yazan uyarı mesajını onaylayınız.</h3>
          <img 
            src="/images/keyboard/windows-step7.jpg" 
            alt="Keyboard installation"
            className="border rounded-lg my-4 shadow-md max-w-md"
          />
        </li>

        {/* Step 10 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Bilgi dosyasını kapatabilirsiniz:</h3>
          <img 
            src="/images/keyboard/windows-step8.jpg" 
            alt="Information document"
            className="border rounded-lg my-4 shadow-md"
          />
          <p>
            Türkçe kullanım kılavuzu için{' '}
            <a href="https://docs.google.com/document/d/1JLY4qcwJR4nA5wuZYJCBwIhxntavC5X4A_IL94IosCM/edit?usp=sharing" 
               className="text-blue-600">
              bu sayfayı
            </a> ziyaret edin
          </p>
        </li>

        {/* Step 11 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Sistem tepsisindeki 'TUR' butonundan Lazca'yı seçin:</h3>
          <img 
            src="/images/keyboard/windows-step9.jpg" 
            alt="Language selection"
            className="border rounded-lg my-4 shadow-md"
          />
          <div className="bg-yellow-100 p-3 rounded-lg">
            <span className="font-bold">1.</span> TUR butonuna tıklayın<br />
            <span className="font-bold">2.</span> Lazca'yı seçin
          </div>
        </li>

        {/* Step 12 */}
        <li className="pl-2">
          <h3 className="text-xl font-semibold mt-6">Klavyeniz hazır! Kısayol: ALT + SHIFT</h3>
          <img 
            src="/images/keyboard/windows-step10.jpg" 
            alt="Keyboard shortcut"
            className="border rounded-lg my-4 shadow-md max-w-md"
          />
          <div className="bg-green-100 p-3 rounded-lg">
            <p className="font-bold">Klavye-skani xažiri ren! (Klavyeniz hazır!)</p>
            <p>Hızlı geçiş için: ALT tuşunu basılı tutarak SHIFT'e basın</p>
          </div>
        </li>
      </ol>

      <div className="mt-12 p-4 bg-blue-50 rounded-lg flex justify-between">
        <Link to="/keyboard" className="text-blue-600 font-medium">
          ← Klavye Rehberine Dön
        </Link>
        <Link to="/keyboard/computer" className="text-blue-600 font-medium">
          Lazca Klavye Kullanım Kılavuzu →
        </Link>
      </div>
    </div>
  );
};

export default KeyboardWin;