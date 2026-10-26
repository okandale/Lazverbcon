import { text } from "./shared";
import type { Text } from "./shared";
type Link = { label: Text; href: string };
type Step = { title: Text; body: Text; image?: string; link?: Link };
export type Guide = {
  title: Text;
  intro: Text;
  steps: Step[];
  optional?: { title: Text; steps: Step[] }[];
  next: string;
};
const step = (
  en: string,
  tr: string,
  bodyEn: string,
  bodyTr: string,
  image?: string,
  link?: Link,
): Step => ({
  title: text(en, tr),
  body: text(bodyEn, bodyTr),
  image,
  link,
});
const keyboard = {
  label: text("Laz keyboard download", "Lazca klavyeyi indirin"),
  href: "https://keyman.com/keyboards/laz",
};
const phoneSettings = {
  title: text(
    "Keyboard height and installed keyboards",
    "Klavye yüksekliği ve yüklü klavyeler",
  ),
  steps: [
    step(
      "Open Keyman settings",
      "Keyman ayarlarını açın",
      "Open the Keyman app, tap the three-dot menu and choose Settings.",
      "Keyman uygulamasında üç nokta menüsüne dokunup Settings (Ayarlar) seçeneğini açın.",
      "iphone-step12.jpg",
    ),
    step(
      "Adjust keyboard height",
      "Klavye yüksekliğini ayarlayın",
      "Choose Adjust keyboard height. Drag the dotted boundary to a comfortable height and finish the adjustment.",
      "Adjust keyboard height seçeneğini açın. Noktalı sınırı sürükleyerek rahat bir yükseklik seçin ve ayarı tamamlayın.",
      "iphone-step14.jpg",
    ),
    step(
      "Manage installed languages",
      "Yüklü dilleri yönetin",
      "In Settings, open Installed languages. Select a language to see its keyboards and dictionaries. Keep the Laz keyboard installed.",
      "Ayarlar içinde Installed languages (Yüklü diller) bölümünü açın. Klavyeleri ve sözlükleri görmek için bir dil seçin. Lazca klavyeyi yüklü tutun.",
      "iphone-step18.jpg",
    ),
    step(
      "Remove an unused Keyman layout",
      "Kullanılmayan Keyman düzenini kaldırın",
      "If you want to remove a layout you do not use, select its language, open the keyboard and choose Uninstall keyboard. The original example removes EuroLatin under English. This is optional; you can keep other layouts.",
      "Kullanmadığınız bir düzeni kaldırmak isterseniz dilini seçin, klavyeyi açın ve Uninstall keyboard seçeneğine dokunun. İlk örnekte English altındaki EuroLatin kaldırılır. Bu isteğe bağlıdır; diğer düzenleri tutabilirsiniz.",
      "iphone-step21.jpg",
    ),
  ],
};
export const guides: Record<string, Guide> = {
  windows: {
    title: text("Laz on Windows", "Windows’ta Lazca"),
    intro: text(
      "Install Keyman, install the Laz package, then select it in Windows.",
      "Keyman’ı kurun, Lazca paketini yükleyin ve Windows’ta seçin.",
    ),
    steps: [
      step(
        "Download Keyman",
        "Keyman’ı indirin",
        "Open Keyman for Windows and choose Download Now. Find the downloaded keyman-…exe in Downloads.",
        "Windows için Keyman bağlantısını açıp Download Now seçeneğine tıklayın. İndirilenler klasöründe keyman-…exe dosyasını bulun.",
        "windows-step1.jpg",
        {
          label: text("Keyman for Windows", "Windows için Keyman"),
          href: "https://keyman.com/windows/download",
        },
      ),
      step(
        "Open the installer",
        "Kurulum dosyasını açın",
        "Double-click the downloaded installer. If Windows asks whether to allow the installer to make changes, confirm the Keyman installation.",
        "İndirdiğiniz kurulum dosyasına çift tıklayın. Windows değişiklik yapma izni sorarsa Keyman kurulumunu onaylayın.",
        "windows-step2.jpg",
      ),
      step(
        "Install Keyman",
        "Keyman’ı kurun",
        "Choose Install in the setup window and wait for completion.",
        "Kurulum penceresinde Install (Yükle) seçeneğine tıklayıp tamamlanmasını bekleyin.",
        "windows-step3.jpg",
      ),
      step(
        "Start Keyman",
        "Keyman’ı başlatın",
        "Choose Start Keyman when setup finishes. Installing Keyman alone does not install the Laz layout.",
        "Kurulum bitince Start Keyman seçeneğine tıklayın. Yalnızca Keyman’ı kurmak Lazca düzenini yüklemez.",
        "windows-step4.jpg",
      ),
      step(
        "Download the Laz package",
        "Lazca paketini indirin",
        "Open the Laz keyboard download. Select Laz and choose Install keyboard. If a .kmp package downloads, open it.",
        "Lazca klavye bağlantısını açın. Laz düzenini seçip Install keyboard seçeneğine tıklayın. Bir .kmp paketi indirilirse dosyayı açın.",
        "windows-step5.jpg",
        keyboard,
      ),
      step(
        "Open Keyman Configuration",
        "Keyman Configuration’ı açın",
        "If the browser asks to open Keyman Configuration, allow it to open the downloaded package.",
        "Tarayıcı Keyman Configuration’ı açmayı sorarsa indirilen paketi açmak için onaylayın.",
        "windows-step6.jpg",
      ),
      step(
        "Install the Laz keyboard",
        "Lazca klavyeyi yükleyin",
        "Check that the package is Laz, then choose Install. Read and confirm the package prompt to finish.",
        "Paketin Laz olduğunu kontrol edip Install seçeneğine tıklayın. Paket istemini okuyup onaylayarak tamamlayın.",
        "windows-step7.jpg",
      ),
      step(
        "Close the information window",
        "Bilgi penceresini kapatın",
        "The package information opens after installation. You can close it and return to the app where you want to type.",
        "Kurulumdan sonra paket bilgi penceresi açılır. Pencereyi kapatıp yazı yazacağınız uygulamaya dönebilirsiniz.",
        "windows-step8.jpg",
      ),
      step(
        "Select Laz in Windows",
        "Windows’ta Lazcayı seçin",
        "Open the input-language indicator near the clock (for example TUR) and select Laz / Keyman. On Windows 10 and 11, Windows + Space cycles through installed input methods.",
        "Saatin yanındaki giriş dili göstergesini (örneğin TUR) açıp Laz / Keyman seçeneğini seçin. Windows 10 ve 11’de Windows + Boşluk yüklü giriş yöntemleri arasında geçiş yapar.",
        "windows-step9.jpg",
      ),
      step(
        "Test the layout",
        "Klavye düzenini deneyin",
        "Open Notepad or another text field and type a few Laz letters. Use the input selector to return to another layout. Alt + Shift may also work if that shortcut is enabled in your Windows settings.",
        "Not Defteri’nde veya başka bir metin alanında birkaç Lazca harf yazın. Diğer düzene dönmek için giriş seçicisini kullanın. Windows ayarlarınızda etkinse Alt + Shift de çalışabilir.",
        "windows-step10.jpg",
      ),
    ],
    next: "computer",
  },
  mac: {
    title: text("Laz on Mac", "Mac’te Lazca"),
    intro: text(
      "Install Keyman, add its input source and install the Laz package.",
      "Keyman’ı kurun, giriş kaynağını ekleyin ve Lazca paketini yükleyin.",
    ),
    steps: [
      step(
        "Download Keyman for Mac",
        "Mac için Keyman’ı indirin",
        "Open the macOS download and choose Download Now.",
        "macOS indirme bağlantısını açıp Download Now seçeneğine tıklayın.",
        "mac-step2.jpg",
        {
          label: text("Keyman for macOS", "macOS için Keyman"),
          href: "https://keyman.com/mac/download",
        },
      ),
      step(
        "Open the DMG",
        "DMG dosyasını açın",
        "In Downloads, double-click keyman-…dmg to open the installer.",
        "İndirilenler klasöründe keyman-…dmg dosyasına çift tıklayarak kurulum dosyasını açın.",
        "mac-step3.jpg",
      ),
      step(
        "Install Keyman",
        "Keyman’ı kurun",
        "Open the installer inside the disk image and follow the installation prompts. Finish the installation before adding a keyboard.",
        "Disk görüntüsünün içindeki kurulum dosyasını açıp kurulum istemlerini izleyin. Klavye eklemeden önce kurulumu tamamlayın.",
        "mac-step5.jpg",
      ),
      step(
        "Add the input source",
        "Giriş kaynağını ekleyin",
        "If prompted, add Keyman in macOS keyboard input sources. In newer macOS versions this is under System Settings → Keyboard → Text Input → Edit. The older screenshot calls this Install Keyman.",
        "İstendiğinde macOS klavye giriş kaynaklarına Keyman’ı ekleyin. Yeni macOS sürümlerinde bu bölüm Sistem Ayarları → Klavye → Metin Girişi → Düzenle yolundadır. Eski görselde Install Keyman adı kullanılır.",
        "mac-step6.jpg",
      ),
      step(
        "Finish setup",
        "Kurulumu tamamlayın",
        "Choose Done after Keyman has been added. If its Configuration menu does not appear, restart the Mac as described in Keyman’s installation help.",
        "Keyman eklendikten sonra Done (Bitti) seçeneğine tıklayın. Configuration menüsü görünmüyorsa Keyman kurulum yardımında belirtildiği gibi Mac’i yeniden başlatın.",
        "mac-step7.jpg",
        {
          label: text("Official macOS setup", "Resmî macOS kurulumu"),
          href: "https://help.keyman.com/products/mac/current-version/start/install-keyman",
        },
      ),
      step(
        "Download Laz",
        "Lazcayı indirin",
        "Open the Laz keyboard page and download the Laz package.",
        "Lazca klavye sayfasını açıp Laz paketini indirin.",
        "mac-step8.jpg",
        keyboard,
      ),
      step(
        "Install the package",
        "Paketi yükleyin",
        "Open laz.kmp in Finder and confirm installation. Alternatively, in Keyman Configuration → Keyboard Layouts, use Download keyboard or drag the .kmp file into the keyboard list.",
        "Finder’da laz.kmp dosyasını açıp kurulumu onaylayın. Alternatif olarak Keyman Configuration → Keyboard Layouts bölümünde Download keyboard seçeneğini kullanın veya .kmp dosyasını klavye listesine sürükleyin.",
        "mac-step9.jpg",
      ),
      step(
        "Enable Laz",
        "Lazcayı etkinleştirin",
        "In Keyman Configuration, check the box beside Laz. Only enabled layouts appear in Keyman’s keyboard menu.",
        "Keyman Configuration içinde Laz yanındaki kutuyu işaretleyin. Keyman’ın klavye menüsünde yalnızca etkin düzenler görünür.",
        "mac-step10.jpg",
      ),
      step(
        "Switch to Laz and test",
        "Lazcaya geçip deneyin",
        "From the macOS input menu choose Keyman, then Laz. Open a text field and try the layout. Use the input menu to switch back.",
        "macOS giriş menüsünden Keyman’ı, ardından Lazcayı seçin. Bir metin alanında düzeni deneyin. Geri dönmek için giriş menüsünü kullanın.",
        "mac-step11.jpg",
      ),
    ],
    next: "computer",
  },
  android: {
    title: text("Laz on Android", "Android’de Lazca"),
    intro: text(
      "Install Laz inside Keyman, then enable Keyman for use in other apps.",
      "Lazcayı Keyman içinde yükleyin, ardından diğer uygulamalarda kullanmak için Keyman’ı etkinleştirin.",
    ),
    steps: [
      step(
        "Install Keyman",
        "Keyman’ı yükleyin",
        "Get Keyman from Google Play and open it.",
        "Google Play’den Keyman’ı yükleyip açın.",
        undefined,
        {
          label: text("Keyman on Google Play", "Google Play’de Keyman"),
          href: "https://play.google.com/store/apps/details?id=com.tavultesoft.kmapro",
        },
      ),
      step(
        "Add a keyboard",
        "Klavye ekleyin",
        "On Get Started, tap Add a keyboard for your language.",
        "Get Started ekranında Add a keyboard for your language seçeneğine dokunun.",
        "android-step2.jpg",
      ),
      step(
        "Open the keyboard catalog",
        "Klavye kataloğunu açın",
        "Choose Install from keyman.com.",
        "Install from keyman.com seçeneğini seçin.",
        "android-step3.jpg",
      ),
      step(
        "Search for Laz",
        "Lazca arayın",
        "Enter Laz in the search field.",
        "Arama alanına Laz yazın.",
        "android-step4.jpg",
      ),
      step(
        "Select the Laz layout",
        "Laz düzenini seçin",
        "Select the keyboard named Laz. The original guide distinguishes this layout from another result named Lazca Klavye.",
        "Laz adlı klavyeyi seçin. İlk rehber bu düzeni Lazca Klavye adlı diğer sonuçtan ayırır.",
        "android-step5.jpg",
      ),
      step(
        "Download the keyboard",
        "Klavyeyi indirin",
        "Tap Install keyboard on the keyboard page.",
        "Klavye sayfasında Install keyboard seçeneğine dokunun.",
        "android-step6.jpg",
      ),
      step(
        "Confirm installation",
        "Yüklemeyi onaylayın",
        "Back in Keyman, choose Install to add Laz.",
        "Keyman’a döndüğünüzde Lazcayı eklemek için Install seçeneğini seçin.",
        "android-step7.jpg",
      ),
      step(
        "Try Laz in Keyman",
        "Lazcayı Keyman’da deneyin",
        "Close the package information and type a few letters in the app. This checks the layout; the next step makes it available in other apps.",
        "Paket bilgisini kapatıp uygulamada birkaç harf yazın. Bu işlem düzeni dener; sonraki adım diğer uygulamalarda da kullanılmasını sağlar.",
        "android-step8.jpg",
      ),
      step(
        "Enable the system keyboard",
        "Sistem klavyesini etkinleştirin",
        "Return to Get Started and choose Enable Keyman as system-wide keyboard. In Android’s input-method settings, turn Keyman on and confirm the system prompt. Return to Keyman when finished.",
        "Get Started ekranına dönüp Enable Keyman as system-wide keyboard seçeneğini seçin. Android giriş yöntemi ayarlarında Keyman’ı açıp sistem istemini onaylayın. İşiniz bitince Keyman’a dönün.",
      ),
      step(
        "Select Keyman in another app",
        "Başka uygulamada Keyman’ı seçin",
        "Open a text field in another app and use Android’s keyboard switcher to select Keyman. Depending on the device, the switcher appears as a keyboard icon, globe or a notification. Select Laz in Keyman’s language menu if needed.",
        "Başka bir uygulamada metin alanını açıp Android’in klavye seçicisinden Keyman’ı seçin. Cihaza göre seçici klavye simgesi, dünya simgesi veya bildirim olarak görünür. Gerekirse Keyman’ın dil menüsünde Lazcayı seçin.",
      ),
    ],
    next: "phone",
  },
  iphone: {
    title: text("Laz on iPhone & iPad", "iPhone ve iPad’de Lazca"),
    intro: text(
      "Install Laz in Keyman and add Keyman to your iOS keyboards.",
      "Keyman’da Lazcayı yükleyin ve Keyman’ı iOS klavyelerinize ekleyin.",
    ),
    steps: [
      step(
        "Install Keyman",
        "Keyman’ı yükleyin",
        "Get Keyman from the App Store and open it.",
        "App Store’dan Keyman’ı yükleyip açın.",
        undefined,
        {
          label: text("Keyman on the App Store", "App Store’da Keyman"),
          href: "https://apps.apple.com/app/keyman/id933676545",
        },
      ),
      step(
        "Add a keyboard",
        "Klavye ekleyin",
        "Choose Add a keyboard for your language.",
        "Add a keyboard for your language seçeneğini seçin.",
        "iphone-step2.jpg",
      ),
      step(
        "Find Laz",
        "Lazcayı bulun",
        "Search for Laz in the keyboard catalog.",
        "Klavye kataloğunda Laz arayın.",
        "iphone-step3.jpg",
      ),
      step(
        "Select the Laz layout",
        "Laz düzenini seçin",
        "Choose Laz. The original guide distinguishes this layout from the result named Lazca Klavye.",
        "Laz seçeneğini seçin. İlk rehber bu düzeni Lazca Klavye adlı sonuçtan ayırır.",
        "iphone-step4.jpg",
      ),
      step(
        "Download the keyboard",
        "Klavyeyi indirin",
        "Tap Install keyboard.",
        "Install keyboard seçeneğine dokunun.",
        "iphone-step5.jpg",
      ),
      step(
        "Confirm installation",
        "Yüklemeyi onaylayın",
        "Choose Install in Keyman to finish adding Laz.",
        "Lazcayı eklemeyi tamamlamak için Keyman’da Install seçeneğini seçin.",
        "iphone-step6.jpg",
      ),
      step(
        "Test inside Keyman",
        "Keyman içinde deneyin",
        "Close the keyboard information and test Laz in the app. Continue below to use it in other apps.",
        "Klavye bilgisini kapatıp uygulamada Lazcayı deneyin. Diğer uygulamalarda kullanmak için aşağıdaki adımlara devam edin.",
        "iphone-step7.jpg",
      ),
      step(
        "Add Keyman in iOS Settings",
        "iOS Ayarları’nda Keyman’ı ekleyin",
        "Open Settings → General → Keyboard → Keyboards → Add New Keyboard. Select Keyman under third-party keyboards.",
        "Ayarlar → Genel → Klavye → Klavyeler → Yeni Klavye Ekle yolunu açın. Üçüncü taraf klavyeler arasından Keyman’ı seçin.",
        "iphone-step8.jpg",
      ),
      step(
        "Open Keyman’s keyboard settings",
        "Keyman’ın klavye ayarlarını açın",
        "In the iOS keyboard list, tap Keyman again to see its options.",
        "iOS klavye listesinde seçeneklerini görmek için Keyman’a yeniden dokunun.",
        "iphone-step9.jpg",
      ),
      step(
        "Check Full Access if the keyboard does not appear",
        "Klavye görünmüyorsa Tam Erişim’i kontrol edin",
        "Keyman’s current help requires Allow Full Access for its system keyboard on iOS 16 because of an iOS issue. Check the official system-keyboard help for your version before enabling this broader keyboard permission.",
        "Keyman’ın güncel yardımı, bir iOS sorunu nedeniyle iOS 16’da sistem klavyesi için Tam Erişime İzin Ver ayarını gerekli belirtir. Bu daha geniş klavye iznini etkinleştirmeden önce sürümünüz için resmî sistem klavyesi yardımına bakın.",
        "iphone-step10.jpg",
        {
          label: text(
            "Enable Keyman on iPhone & iPad",
            "iPhone ve iPad’de Keyman’ı etkinleştirme",
          ),
          href: "https://help.keyman.com/products/iphone-and-ipad/current-version/start/installing-system-keyboard",
        },
      ),
      step(
        "Switch to Keyman",
        "Keyman’a geçin",
        "Open a text field in another app. Press or hold the globe key and select Keyman, then select Laz in its language menu. Use the globe key to return to another keyboard.",
        "Başka bir uygulamada metin alanını açın. Dünya tuşuna basın veya basılı tutup Keyman’ı, ardından dil menüsünde Lazcayı seçin. Diğer klavyeye dönmek için dünya tuşunu kullanın.",
        "iphone-step15.jpg",
      ),
    ],
    optional: [phoneSettings],
    next: "phone",
  },
  computer: {
    title: text("Typing on a computer", "Bilgisayarda yazma"),
    intro: text(
      "The Laz layout and its key combinations on Windows and Mac.",
      "Windows ve Mac’te Lazca düzeni ve tuş birleşimleri.",
    ),
    steps: [
      step(
        "The layout",
        "Klavye düzeni",
        "With Laz selected, the Ü position produces ʒ. The Ö position is a dead key: press it, release it, then press another letter to make a special character.",
        "Lazca seçiliyken Ü tuşunun yerinde ʒ bulunur. Ö tuşunun yeri ölü tuştur: basıp bırakın, ardından özel karakter için başka bir harfe basın.",
        "pc-default.jpg",
      ),
      step(
        "Special characters",
        "Özel karakterler",
        "Dead key + ç → ç̌; + k → k̆; + p → p̌; + t → t̆; + z → ʒ; + ʒ → ǯ. These are sequential presses, not a shortcut held down together.",
        "Ölü tuş + ç → ç̌; + k → k̆; + p → p̌; + t → t̆; + z → ʒ; + ʒ → ǯ. Tuşlara aynı anda basılmaz; sırayla basılır.",
        "pc-combinations.jpg",
      ),
      step(
        "Typing ö and ü",
        "ö ve ü yazma",
        "The original Windows layout uses Alt + Ö and Alt + Ü for the ordinary letters. Its Mac guide gives Command as the modifier. Check the layout diagram and current keyboard help if your installed version behaves differently.",
        "İlk Windows düzeninde normal harfler için Alt + Ö ve Alt + Ü kullanılır. Mac rehberinde değiştirici tuş Command olarak verilir. Yüklü sürümünüz farklı çalışıyorsa düzen görseline ve güncel klavye yardımına bakın.",
        "pc-alt-combinations.jpg",
        {
          label: text(
            "Current Laz keyboard help",
            "Güncel Lazca klavye yardımı",
          ),
          href: "https://help.keyman.com/keyboard/laz",
        },
      ),
      step(
        "Change input layouts",
        "Giriş düzenini değiştirin",
        "Use the input-language menu to switch between Laz and another keyboard. On Windows, try Windows + Space; Alt + Shift depends on your settings. On Mac, use the input menu or your configured input-source shortcut.",
        "Lazca ve başka klavye arasında geçmek için giriş dili menüsünü kullanın. Windows’ta Windows + Boşluk’u deneyin; Alt + Shift ayarlarınıza bağlıdır. Mac’te giriş menüsünü veya yapılandırılmış giriş kaynağı kısayolunuzu kullanın.",
      ),
    ],
    next: "phone",
  },
  phone: {
    title: text("Typing on a phone", "Telefonda yazma"),
    intro: text(
      "Special characters, suggestions, emoji and keyboard settings.",
      "Özel karakterler, öneriler, emojiler ve klavye ayarları.",
    ),
    steps: [
      step(
        "Hold a letter for more choices",
        "Diğer seçenekler için harfe basılı tutun",
        "Hold t, k or ʒ to see its Laz variants. Slide to the character you want and release.",
        "Lazca biçimlerini görmek için t, k veya ʒ tuşuna basılı tutun. İstediğiniz karaktere kaydırıp bırakın.",
        "mobile-special-chars.jpg",
      ),
      step(
        "Use word suggestions",
        "Kelime önerilerini kullanın",
        "With a Laz dictionary installed, Keyman can suggest Laz words even when you type without special letters. Tap the correct suggestion. In the original layout, Space accepts the highlighted suggestion; check the resulting spelling.",
        "Lazca sözlük yüklüyse özel harfler kullanmadan yazdığınızda da Keyman Lazca kelimeler önerebilir. Doğru öneriye dokunun. İlk düzende Boşluk vurgulanan öneriyi kabul eder; çıkan yazılışı kontrol edin.",
        "mobile-dictionary.jpg",
      ),
      step(
        "Open emoji",
        "Emojileri açın",
        "In the original phone layout, hold the comma key, then choose the emoji tab. Return to the letter layout when finished.",
        "İlk telefon düzeninde virgül tuşuna basılı tutup emoji sekmesini seçin. İşiniz bitince harf düzenine dönün.",
        "mobile-emoji.jpg",
      ),
      step(
        "Change the keyboard or language",
        "Klavyeyi veya dili değiştirin",
        "Use the globe or keyboard switcher to select Keyman. To choose another installed Keyman language, open its language menu. If Keyman only works inside its app, complete the system-keyboard steps in the installation guide.",
        "Keyman’ı seçmek için dünya simgesini veya klavye seçicisini kullanın. Yüklü başka bir Keyman dilini seçmek için dil menüsünü açın. Keyman yalnızca kendi uygulamasında çalışıyorsa kurulum rehberindeki sistem klavyesi adımlarını tamamlayın.",
      ),
    ],
    optional: [phoneSettings],
    next: "computer",
  },
};
