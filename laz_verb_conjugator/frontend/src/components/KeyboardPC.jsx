import React from 'react';
import { Link } from 'react-router-dom';

const KeyboardPC = () => {
  return (
    <div className="max-w-4xl mx-auto p-6 prose">
      <h1 className="text-3xl font-bold">Bilgisayar İçin Klavye Kullanım Rehberi (Windows ve Mac)</h1>

      <div className="my-8 p-4 bg-blue-50 rounded-lg">
        <h2 className="text-2xl font-semibold">Varsayılan Klavye Düzeni</h2>
        <img 
          src="/images/keyboard/pc-default.jpg" 
          alt="Varsayılan klavye düzeni"
          className="border rounded-lg my-4 shadow-md"
        />
        <p>Ü harfi <strong>ʒ</strong> ile değiştirilmiştir.</p>
      </div>

      <div className="space-y-8">
        {/* Section 1 */}
        <div>
          <h3 className="text-xl font-semibold">Özel Karakterler</h3>
          <p>Ö tuşu <strong>˘</strong> ile değiştirilmiştir ve "sessiz tuş" olarak kullanabilirsiniz.</p>
        </div>

        {/* Section 2 */}
        <div>
          <h3 className="text-xl font-semibold">Sessiz Tuş Kullanımı</h3>
          <img 
            src="/images/keyboard/pc-combinations.jpg" 
            alt="Sessiz tuş kombinasyonları"
            className="border rounded-lg my-4 shadow-md"
          />
          <p>Sessiz tuş ile birlikte temel harflere basarak şu karakterleri oluşturabilirsiniz:</p>
          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="bg-gray-100 p-3 rounded-lg">
              <p><strong>˘ + ç</strong> → ç̌</p>
              <p><strong>˘ + k</strong> → k̆</p>
              <p><strong>˘ + p</strong> → p̌</p>
            </div>
            <div className="bg-gray-100 p-3 rounded-lg">
              <p><strong>˘ + t</strong> → t̆</p>
              <p><strong>˘ + z</strong> → ʒ</p>
              <p><strong>˘ + ʒ</strong> → ǯ</p>
            </div>
          </div>
        </div>

        {/* Section 3 */}
        <div>
          <h3 className="text-xl font-semibold">Ö ve Ü Yazma</h3>
          <img 
            src="/images/keyboard/pc-alt-combinations.jpg" 
            alt="ALT tuş kombinasyonları"
            className="border rounded-lg my-4 shadow-md"
          />
          <div className="bg-yellow-100 p-4 rounded-lg">
            <p className="font-bold">Normal Ö/Ü yazmak için:</p>
            <p>
              <strong>ALT</strong> (Mac'te <strong>Command</strong>) tuşunu basılı tutarak:
            </p>
            <ul className="list-disc pl-6 mt-2">
              <li>Ö tuşuna basabilirsiniz</li>
              <li>Ü tuşuna basabilirsiniz</li>
            </ul>
          </div>
        </div>

        {/* Section 4 */}
        <div className="bg-green-100 p-4 rounded-lg">
          <h3 className="text-xl font-semibold">Kısayol Tuşları</h3>
          <ul className="list-disc pl-6 space-y-2">
            <li><strong>ALT + SHIFT</strong>: Klavye dilini değiştirebilirsiniz</li>
            <li><strong>ALT + Ö</strong>: Normal ö yazabilirsiniz</li>
            <li><strong>ALT + Ü</strong>: Normal ü yazabilirsiniz</li>
          </ul>
        </div>
      </div>

      <div className="mt-12 p-4 bg-blue-50 rounded-lg flex justify-between">
        <Link to="/keyboard" className="text-blue-600 font-medium">
          ← Klavye Rehberine Dönünüz
        </Link>
      </div>
    </div>
  );
};

export default KeyboardPC;