# ÖNEMLI - KURULUM TALİMATLARI

## GitHub'a Yüklemeden Önce

Eğer GitHub repo'nuzda eski dosyalar varsa:

1. **TÜM eski dosyaları silin** (özellikle `tsconfig.json`)
2. Veya yeni bir repo oluşturun
3. Sonra bu yeni dosyaları yükleyin

## Eğer Build Hatası Alırsanız

Eğer "TypeScript required" hatası alırsanız:

**GitHub repo'nuzda `tsconfig.json` dosyası varsa SİLİN!**

Bu proje sadece JavaScript kullanıyor, TypeScript dosyası olmamalı.

## Deploy Adımları

1. GitHub'da yeni repo oluşturun (veya eski dosyaları temizleyin)
2. Bu klasördeki TÜM dosyaları yükleyin
3. Vercel'e bağlayın
4. Deploy!

✅ `tsconfig.json` olmamalı
✅ Sadece `.js` dosyaları olmalı
✅ TypeScript paketleri yüklü olmamalı
