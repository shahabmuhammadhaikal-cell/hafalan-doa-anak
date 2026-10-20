# 🕌 Doa Anak — Hafalan Doa Harian

Aplikasi **React Native (Expo)** untuk membantu anak-anak menghafal doa-doa
sehari-hari dengan cara yang menyenangkan: ilustrasi cerah, teks Arab besar,
arti bahasa Indonesia, tips hafalan, dan **video YouTube yang di-embed resmi**
dari channel aslinya.

> Aplikasi edukasi non-komersial. Seluruh isi repository ini dirancang agar
> **bebas masalah copyright** — lihat bagian [Kebijakan Copyright](#-kebijakan-copyright).

## ✨ Fitur

- 📖 **14 doa harian anak** lengkap dengan teks Arab, transliterasi latin, dan arti
- 🎨 **Ilustrasi orisinal** untuk tiap doa (digambar program, bukan hasil unduhan)
- 🎬 **Video YouTube resmi** (embed IFrame) + tombol tonton langsung di YouTube
- 💡 **Tips menghafal** + 3 langkah sederhana: Dengarkan → Ulangi → Hafal
- 📚 **Referensi hadits** pada tiap doa (Bukhari, Muslim, Tirmidzi, Abu Dawud, dll.)
- 🕌 Halaman **Tentang & Referensi** yang menjelaskan asal-usul semua konten
- 📱 Tampilan cerah ramah anak, grid kartu dua kolom, navigasi Expo Router

## 🛠️ Cara Menjalankan

```bash
npm install
npx expo start
```

Pindai QR code dengan aplikasi **Expo Go** (Android/iOS). Tidak perlu build
native — semua dependensi (`react-native-webview`, `expo-router`,
`@expo/vector-icons`, dll.) sudah kompatibel dengan Expo Go.

> **Catatan aset:** file di `assets/` (ilustrasi, ikon, banner) dihasilkan oleh
> `scripts/generate_assets.py` dan disinkronkan otomatis oleh GitHub Actions
> (`.github/workflows/sync-assets.yml`) setiap push ke `main`.

Perintah lain:

```bash
npx tsc --noEmit       # typecheck
npx expo-doctor        # cek kesehatan project
npx expo export -p android   # uji bundling Metro
python3 scripts/generate_assets.py   # regenerate seluruh ilustrasi
```

## 📂 Struktur Proyek

```
src/
  app/                 # layar Expo Router
    _layout.tsx        #   navigasi (Stack)
    index.tsx          #   beranda (grid doa)
    doa/[id].tsx       #   detail doa (teks, video, referensi)
    tentang.tsx        #   keterangan copyright & referensi
  components/          # DoaCard, YouTubeVideo
  data/doas.ts         # data 14 doa + video
  theme.ts             # palet warna
scripts/
  generate_assets.py   # generator seluruh ilustrasi & ikon
assets/
  doa/*.png            # ilustrasi 1280x720 per doa
  header.png, icon.png # banner & ikon aplikasi
```

## 🎬 Referensi Video (Embed YouTube)

Semua video dicek lewat endpoint oEmbed YouTube dan **mengizinkan embedding**.
Video hanya di-embed — tidak diunduh maupun didistribusikan ulang.

| Doa | Judul video | Channel |
|-----|-------------|---------|
| Bangun Tidur | [Yuk, Belajar Doa Sehari-Hari: Doa Bangun Tidur](https://www.youtube.com/watch?v=jwo2aihF0lA) | Yufid Kids |
| Sebelum Tidur | [Doa Sebelum Tidur dan Bangun Tidur](https://www.youtube.com/watch?v=t5bzkTgatBE) | Kastari Sentra |
| Sebelum Makan | [Doa Sebelum Makan Bersama Jamal Laeli #1](https://www.youtube.com/watch?v=WCEFOR5jgAU) | Jamal Laeli |
| Sesudah Makan | [DOA SEBELUM MAKAN & SESUDAH MAKAN](https://www.youtube.com/watch?v=SmKlP8Ma0Qg) | Sunatman Dunia Ibu dan Anak |
| Minum | [Doa Sebelum dan Sesudah Minum Arab Latin dan Artinya](https://www.youtube.com/watch?v=bbKdXxPQnsg) | RIFDA CHAN |
| Masuk/Keluar Kamar Mandi | [Yuk Belajar Doa Sehari-Hari: Doa Masuk dan Keluar Kamar Mandi](https://www.youtube.com/watch?v=Wqjk3vfgMTs) | Yufid Kids |
| Keluar Rumah | [Super Hero Seri 16-Doa Keluar Rumah](https://www.youtube.com/watch?v=YY3IA2Hq1gY) | Jamal Laeli |
| Masuk Rumah | [DOA MASUK RUMAH DAN KELUAR RUMAH](https://www.youtube.com/watch?v=YHmvRufrq0k) | Sunatman Dunia Ibu dan Anak |
| Naik Kendaraan | [Doa Naik Kendaraan - Belajar Doa Harian](https://www.youtube.com/watch?v=Ix4ajTSf7dg) | Yufid Kids |
| Sebelum Belajar | [Seri Doa-Doa Sebelum Belajar](https://www.youtube.com/watch?v=2WAahi4Rgrg) | Jamal Laeli |
| Masuk Masjid | [Doa Masuk Masjid (Kartun Anak)](https://www.youtube.com/watch?v=H03MXiIn-N4) | Yufid Kids |
| Keluar Masjid | [Doa Keluar Masjid (Kartun Anak)](https://www.youtube.com/watch?v=CFf8OVhJFzA) | Yufid Kids |
| Pulang Sekolah | [Lagu dan Doa Pulang Sekolah untuk Anak PAUD / TK / RA](https://www.youtube.com/watch?v=nYPebyMT9Jc) | Iin Aina |

## 🛡️ Kebijakan Copyright

| Konten | Asal | Status copyright |
|--------|------|------------------|
| Teks doa & arti | Hadits shahih (riwayat ulama) | Teks keagamaan/riwayat — bebas disebarluaskan; rujukan dicantumkan per doa |
| Gambar ilustrasi | Digambar program oleh `scripts/generate_assets.py` | 100% orisinal, tidak mengambil artwork pihak lain |
| Video YouTube | Embed resmi IFrame YouTube | Hak cipta tetap milik channel masing-masing; hanya ditampilkan (tidak diunduh) |
| Emoji & font | Font bawaan sistem perangkat | Tidak menyertakan font pihak ketiga |
| Kode sumber | Proyek ini | MIT (lihat `LICENSE`) |

Bila Anda kreator video yang tercantum dan keberatan, silakan buka issue atau
hubungi pengembang untuk penghapusan tautan.

## 📄 Lisensi

Kode sumber berlisensi **MIT** — lihat [`LICENSE`](LICENSE).
Ilustrasi dibuat khusus untuk proyek ini dan mengikuti lisensi repository.
