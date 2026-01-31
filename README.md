# Adana Hava Durumu Uygulaması

Bu uygulama, Adana'nın anlık hava durumunu ve 3 günlük tahminini gösteren bir Next.js uygulamasıdır.

## Özellikler

- 📍 Adana için güncel hava durumu
- 🌡️ Sıcaklık, nem, rüzgar hızı ve yağış bilgileri
- 📅 3 günlük hava durumu tahmini
- 🎨 Modern ve şık kullanıcı arayüzü
- ⚡ Otomatik güncelleme (her 10 dakikada bir)
- 📱 Responsive tasarım (mobil uyumlu)

## Vercel'e Deploy Etme

### 1. Yöntem: Vercel Dashboard Üzerinden

1. GitHub hesabınıza giriş yapın ve yeni bir repository oluşturun
2. Bu projeyi GitHub repository'nize yükleyin
3. [Vercel](https://vercel.com)'e gidin ve GitHub hesabınızla giriş yapın
4. "New Project" butonuna tıklayın
5. GitHub repository'nizi seçin
6. Framework olarak "Next.js" otomatik algılanacak
7. "Deploy" butonuna tıklayın

### 2. Yöntem: Vercel CLI ile

```bash
# Vercel CLI'yi yükleyin (eğer yüklü değilse)
npm i -g vercel

# Proje klasörüne gidin
cd weather-app

# Deploy edin
vercel
```

## Yerel Geliştirme

```bash
# Bağımlılıkları yükleyin
npm install

# Geliştirme sunucusunu başlatın
npm run dev
```

Tarayıcınızda [http://localhost:3000](http://localhost:3000) adresini açın.

## Teknolojiler

- **Next.js 14** - React framework
- **TypeScript** - Tip güvenliği
- **Tailwind CSS** - Styling
- **Open-Meteo API** - Ücretsiz hava durumu API'si

## API

Uygulama, ücretsiz [Open-Meteo API](https://open-meteo.com)'sini kullanmaktadır. API anahtarına ihtiyaç yoktur.

## Lisans

MIT

---

Geliştirici: Claude AI tarafından oluşturuldu
