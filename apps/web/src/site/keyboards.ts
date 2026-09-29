import { text } from "./shared";
import type { Text } from "./shared";
export type Guide = {
  title: Text;
  intro: Text;
  steps: { title: Text; body: Text; image?: string }[];
  links: { label: Text; href: string }[];
  next: string;
};
const keyboard = {
  label: text("Laz keyboard download", "Lazca klavyeyi indirin"),
  href: "https://keyman.com/keyboards/laz",
};
const install = {
  title: text("Add the Laz keyboard", "Lazca klavyeyi ekleyin"),
  body: text(
    "Open the Laz keyboard download page on this device. Choose Install keyboard and follow Keyman’s installation steps.",
    "Bu cihazda Lazca klavye indirme sayfasını açın. Install keyboard seçeneğini seçin ve Keyman’ın kurulum adımlarını izleyin.",
  ),
};
export const guides: Record<string, Guide> = {
  windows: {
    title: text("Laz on Windows", "Windows’ta Lazca"),
    intro: text(
      "Install Keyman, add Laz and switch to it when you write.",
      "Keyman’ı kurun, Lazcayı ekleyin ve yazarken bu klavyeye geçin.",
    ),
    steps: [
      {
        title: text("Install Keyman", "Keyman’ı kurun"),
        body: text(
          "Download Keyman for Windows from the official site and run the installer.",
          "Resmî siteden Windows için Keyman’ı indirin ve kurulum dosyasını çalıştırın.",
        ),
        image: "windows-step1.jpg",
      },
      { ...install, image: "windows-step7.jpg" },
      {
        title: text("Choose Laz", "Lazcayı seçin"),
        body: text(
          "Open the Keyman menu near the clock and select the Laz keyboard. Try it in a text editor. Use your system’s language selector to switch back.",
          "Saatin yanındaki Keyman menüsünü açıp Lazca klavyeyi seçin. Bir metin düzenleyicide deneyin. Geri dönmek için sistemin dil seçicisini kullanın.",
        ),
      },
    ],
    links: [
      {
        label: text("Keyman for Windows", "Windows için Keyman"),
        href: "https://keyman.com/windows/download",
      },
      keyboard,
      {
        label: text("Official installation help", "Resmî kurulum yardımı"),
        href: "https://help.keyman.com/products/windows/current-version/start/download-and-install-keyboard",
      },
    ],
    next: "computer",
  },
  mac: {
    title: text("Laz on Mac", "Mac’te Lazca"),
    intro: text(
      "Use the Laz layout with Keyman for macOS.",
      "macOS için Keyman ile Lazca klavye düzenini kullanın.",
    ),
    steps: [
      {
        title: text("Install Keyman", "Keyman’ı kurun"),
        body: text(
          "Download Keyman for macOS and follow its setup instructions. Add Keyman as an input source when prompted.",
          "macOS için Keyman’ı indirin ve kurulum yönergelerini izleyin. İstendiğinde Keyman’ı giriş kaynağı olarak ekleyin.",
        ),
        image: "mac-step2.jpg",
      },
      { ...install, image: "mac-step10.jpg" },
      {
        title: text("Switch your input source", "Giriş kaynağını değiştirin"),
        body: text(
          "Select Keyman from the input menu, then choose Laz. Open a text editor and try the layout. Use the input menu to return to another keyboard.",
          "Giriş menüsünden Keyman’ı, ardından Lazcayı seçin. Bir metin düzenleyicide klavyeyi deneyin. Diğer klavyeye dönmek için giriş menüsünü kullanın.",
        ),
      },
    ],
    links: [
      {
        label: text("Keyman for macOS", "macOS için Keyman"),
        href: "https://keyman.com/mac/download",
      },
      keyboard,
      {
        label: text("Official macOS help", "Resmî macOS yardımı"),
        href: "https://help.keyman.com/products/mac/",
      },
    ],
    next: "computer",
  },
  android: {
    title: text("Laz on Android", "Android’de Lazca"),
    intro: text(
      "Add Laz to Keyman and use it in your other apps.",
      "Keyman’a Lazcayı ekleyin ve diğer uygulamalarınızda kullanın.",
    ),
    steps: [
      {
        title: text("Get Keyman", "Keyman’ı indirin"),
        body: text(
          "Install Keyman from Google Play and open the app.",
          "Google Play’den Keyman’ı yükleyin ve uygulamayı açın.",
        ),
      },
      {
        title: text("Find Laz", "Lazcayı bulun"),
        body: text(
          "Choose Add a keyboard, then install from keyman.com. Search for Laz, open its page and choose Install keyboard. You can also use the Laz keyboard link below.",
          "Add a keyboard seçeneğini ve ardından keyman.com’dan yüklemeyi seçin. Laz araması yapın, sayfasını açın ve Install keyboard seçeneğine dokunun. Aşağıdaki Lazca klavye bağlantısını da kullanabilirsiniz.",
        ),
        image: "android-step4.jpg",
      },
      {
        title: text(
          "Enable it in other apps",
          "Diğer uygulamalarda etkinleştirin",
        ),
        body: text(
          "In Keyman’s Get Started menu, choose Enable Keyman as system-wide keyboard. Enable Keyman in Android’s keyboard settings, then select it with your device’s keyboard switcher.",
          "Keyman’ın Get Started menüsünden Enable Keyman as system-wide keyboard seçeneğini açın. Android klavye ayarlarında Keyman’ı etkinleştirin ve cihazınızın klavye seçicisinden seçin.",
        ),
      },
    ],
    links: [
      {
        label: text("Keyman on Google Play", "Google Play’de Keyman"),
        href: "https://play.google.com/store/apps/details?id=com.tavultesoft.kmapro",
      },
      keyboard,
      {
        label: text("Official Android help", "Resmî Android yardımı"),
        href: "https://help.keyman.com/products/android/current-version/start/",
      },
    ],
    next: "phone",
  },
  iphone: {
    title: text("Laz on iPhone & iPad", "iPhone ve iPad’de Lazca"),
    intro: text(
      "Install the Laz keyboard and select it when typing.",
      "Lazca klavyeyi kurun ve yazarken seçin.",
    ),
    steps: [
      {
        title: text("Get Keyman", "Keyman’ı indirin"),
        body: text(
          "Install Keyman from the App Store, then open it.",
          "App Store’dan Keyman’ı yükleyip açın.",
        ),
      },
      {
        title: text("Install Laz", "Lazcayı yükleyin"),
        body: text(
          "Use Add a keyboard and find Laz on keyman.com, or open the Laz download link below on your phone. Choose Install keyboard and follow the prompts in Keyman.",
          "Add a keyboard seçeneğiyle keyman.com’da Laz arayın veya aşağıdaki Lazca indirme bağlantısını telefonunuzda açın. Install keyboard seçeneğini seçip Keyman’ın adımlarını izleyin.",
        ),
        image: "iphone-step4.jpg",
      },
      {
        title: text(
          "Add Keyman to your keyboards",
          "Keyman’ı klavyelerinize ekleyin",
        ),
        body: text(
          "In iOS Settings, open General → Keyboard → Keyboards → Add New Keyboard, and choose Keyman. When typing, use the globe key to select it.",
          "iOS Ayarları’nda Genel → Klavye → Klavyeler → Yeni Klavye Ekle yolunu izleyin ve Keyman’ı seçin. Yazarken dünya simgesini kullanarak bu klavyeye geçin.",
        ),
      },
    ],
    links: [
      {
        label: text("Keyman on the App Store", "App Store’da Keyman"),
        href: "https://apps.apple.com/app/keyman/id933676545",
      },
      keyboard,
      {
        label: text(
          "Official iPhone & iPad help",
          "Resmî iPhone ve iPad yardımı",
        ),
        href: "https://help.keyman.com/products/iphone-and-ipad/current-version/start/",
      },
    ],
    next: "phone",
  },
  computer: {
    title: text("Typing on a computer", "Bilgisayarda yazma"),
    intro: text(
      "Get to know the Laz layout on Windows and Mac.",
      "Windows ve Mac’te Lazca klavye düzenini tanıyın.",
    ),
    steps: [
      {
        title: text("The layout", "Klavye düzeni"),
        body: text(
          "With Laz selected, the Ü position produces ʒ. The Ö position acts as a dead key: press it, then a letter to make a special character.",
          "Lazca seçiliyken Ü tuşunun yerinde ʒ bulunur. Ö tuşunun yeri ölü tuş olarak çalışır: önce bu tuşa, sonra bir harfe basarak özel karakter oluşturun.",
        ),
        image: "pc-default.jpg",
      },
      {
        title: text("Special characters", "Özel karakterler"),
        body: text(
          "Press the dead key, then ç, k, p or t for their Laz variants. Combining it with z produces ʒ; combining it with ʒ produces ǯ. The diagram shows the combinations used in the original guide.",
          "Ölü tuştan sonra ç, k, p veya t tuşuna basarak Lazca biçimlerini yazın. z ile ʒ, ʒ ile ǯ oluşur. Görsel, ilk rehberdeki birleşimleri gösterir.",
        ),
        image: "pc-combinations.jpg",
      },
      {
        title: text(
          "Other letters and switching layouts",
          "Diğer harfler ve klavye değiştirme",
        ),
        body: text(
          "The diagram shows the alternate keys for ö and ü. Use your system’s input selector to change keyboards. If your version differs, open the current keyboard help below.",
          "Görsel, ö ve ü için alternatif tuşları gösterir. Klavye değiştirmek için sistemin giriş seçicisini kullanın. Sürümünüz farklıysa aşağıdaki güncel klavye yardımını açın.",
        ),
        image: "pc-alt-combinations.jpg",
      },
    ],
    links: [
      keyboard,
      {
        label: text("Current Laz keyboard help", "Güncel Lazca klavye yardımı"),
        href: "https://help.keyman.com/keyboard/laz",
      },
    ],
    next: "phone",
  },
  phone: {
    title: text("Typing on a phone", "Telefonda yazma"),
    intro: text(
      "Special characters and everyday shortcuts.",
      "Özel karakterler ve günlük kısayollar.",
    ),
    steps: [
      {
        title: text(
          "Hold a letter for more choices",
          "Diğer seçenekler için harfe basılı tutun",
        ),
        body: text(
          "Press and hold a letter such as t, k or ʒ to see its Laz variants. Slide to the character you want, then release.",
          "Lazca biçimlerini görmek için t, k veya ʒ gibi bir harfe basılı tutun. İstediğiniz karaktere kaydırıp bırakın.",
        ),
        image: "mobile-special-chars.jpg",
      },
      {
        title: text("Word suggestions", "Kelime önerileri"),
        body: text(
          "If a Laz dictionary is enabled in Keyman, use the suggestion bar to choose a word. Check its spelling before sending your message.",
          "Keyman’da Lazca sözlük etkinse öneri çubuğundan kelime seçebilirsiniz. Mesajı göndermeden önce yazılışı kontrol edin.",
        ),
        image: "mobile-dictionary.jpg",
      },
      {
        title: text(
          "Emoji and keyboard options",
          "Emoji ve klavye seçenekleri",
        ),
        body: text(
          "The original phone layout opens emoji options by holding the comma key. Use Keyman’s settings to adjust the keyboard height; labels may differ between versions.",
          "İlk telefon düzeninde virgül tuşuna basılı tutarak emoji seçenekleri açılır. Klavye yüksekliğini Keyman ayarlarından değiştirebilirsiniz; adlar sürüme göre değişebilir.",
        ),
        image: "mobile-emoji.jpg",
      },
    ],
    links: [
      keyboard,
      {
        label: text("Current Laz keyboard help", "Güncel Lazca klavye yardımı"),
        href: "https://help.keyman.com/keyboard/laz",
      },
    ],
    next: "computer",
  },
};
