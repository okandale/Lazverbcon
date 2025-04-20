import React from 'react';
import { Link } from 'react-router-dom';

const KeyboardMobile = () => {
  return (
    <div className="max-w-4xl mx-auto p-6 prose">
      <h1 className="text-3xl font-bold">Telefon İçin Klavye Kullanım Rehberi</h1>

      <div className="my-8 p-4 bg-blue-50 rounded-lg">
        <h2 className="text-2xl font-semibold">Temel Kullanım</h2>
        <p className="text-lg">
          Telefonunuza yükledikten sonra, klavyeyi doğrudan kullanabilirsiniz.
        </p>
      </div>

      <div className="space-y-8">
        {/* Section 1 */}
        <div>
          <h3 className="text-xl font-semibold">Lazca'ya Özgü Harfler</h3>
          <img 
            src="/images/keyboard/mobile-special-chars.jpg" 
            alt="Lazca özel harfler"
            className="border rounded-lg my-4 shadow-md"
          />
          <p>
            Lazca'ya özgü harflere (<strong>ʒ̆, t̆, k̆</strong>...) ulaşmak için:
          </p>
          <div className="bg-gray-100 p-4 rounded-lg mt-4">
            <p>İlgili harfin varsayılan tuşuna (<strong>ʒ, t, k</strong>...) basılı tutun</p>
            <p>Çıkan menüden istediğiniz karakteri seçin</p>
          </div>
        </div>

        {/* Section 2 */}
        <div>
          <h3 className="text-xl font-semibold">Sözlük Kullanımı</h3>
          <img 
            src="/images/keyboard/mobile-dictionary.jpg" 
            alt="Sözlük kullanımı"
            className="border rounded-lg my-4 shadow-md"
          />
          <div className="bg-green-100 p-4 rounded-lg">
            <p>
              <strong>Sözlük özelliği:</strong> Lazca'ya özgü harfleri kullanmasanız bile 
              Laz kelimelerini algılayabilir ve önerebilir.
            </p>
          </div>
        </div>

        {/* Section 3 */}
        <div>
          <h3 className="text-xl font-semibold">Emoji ve Diğer Karakterler</h3>
          <img 
            src="/images/keyboard/mobile-emoji.jpg" 
            alt="Emoji kullanımı"
            className="border rounded-lg my-4 shadow-md"
          />
          <div className="bg-yellow-100 p-4 rounded-lg">
            <p><strong>Emoji'lere ulaşmak için:</strong></p>
            <p>"Virgül" tuşuna basılı tutun</p>
            <p>Çıkan menüden emoji sekmesini seçin</p>
          </div>
        </div>

        {/* Section 4 */}
        <div className="bg-purple-100 p-4 rounded-lg">
          <h3 className="text-xl font-semibold">Klavye Kısayolları</h3>
          <ul className="list-disc pl-6 space-y-2">
            <li><strong>Uzun basma:</strong> Özel karakterlere ulaşmak için harflere basılı tutun</li>
            <li><strong>Virgül tuşu:</strong> Emoji menüsüne erişim</li>
            <li><strong>Boşluk tuşu:</strong> Sözlük önerilerini kabul etme</li>
          </ul>
        </div>
      </div>

      <div className="mt-12 p-4 bg-blue-50 rounded-lg flex justify-between">
        <Link to="/keyboard" className="text-blue-600 font-medium">
          ← Klavye Rehberine Dön
        </Link>
        <Link to="/keyboard/android" className="text-blue-600 font-medium">
          Android Kurulum Rehberi →
        </Link>
      </div>
    </div>
  );
};

export default KeyboardMobile;