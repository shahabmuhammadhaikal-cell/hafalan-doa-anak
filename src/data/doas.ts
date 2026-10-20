import type { ImageSourcePropType } from 'react-native';

/**
 * Data hafalan doa anak.
 *
 * Kebijakan copyright:
 * - Teks doa bersumber dari hadits shahih (teks keagamaan/riwayat, bebas
 *   disebarluaskan) — rujukan lengkap dicantumkan di field `source`.
 * - Gambar ilustrasi dibuat orisinal oleh skrip `scripts/generate_assets.py`
 *   (tanpa mengambil artwork pihak lain).
 * - Video YouTube hanya di-*embed* lewat pemutar resmi YouTube; hak cipta
 *   video tetap milik kreator masing-masing (dicantumkan di `video.channel`).
 *   Semua video sudah dicek lewat endpoint oEmbed YouTube dan mengizinkan
 *   embedding.
 */

export type DoaVideo = {
  /** ID video YouTube (11 karakter) */
  id: string;
  /** Judul video persis seperti di YouTube */
  title: string;
  /** Nama channel asli (atribusi) */
  channel: string;
  /** Tautan video asli untuk ditonton di aplikasi YouTube */
  url: string;
};

export type Doa = {
  id: string;
  /** Judul doa untuk kartu */
  title: string;
  /** Emoji penanda (font sistem, bebas lisensi) */
  emoji: string;
  /** Teks Arab */
  arabic: string;
  /** Transliterasi latin */
  latin: string;
  /** Arti dalam bahasa Indonesia */
  meaning: string;
  /** Tips menghafal untuk anak */
  tip: string;
  /** Rujukan hadits */
  source: string;
  /** Ilustrasi orisinal */
  image: ImageSourcePropType;
  video: DoaVideo;
};

const v = (id: string, title: string, channel: string): DoaVideo => ({
  id,
  title,
  channel,
  url: `https://www.youtube.com/watch?v=${id}`,
});

export const DOAS: Doa[] = [
  {
    id: 'bangun-tidur',
    title: 'Doa Bangun Tidur',
    emoji: '⏰',
    arabic: 'الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ',
    latin: "Alḥamdu lillāhilladzī aḥyānā ba'da mā amātanā wa ilayhin nusyūr",
    meaning:
      'Segala puji bagi Allah yang telah menghidupkan kami setelah mematikan kami, dan kepada-Nya kami (akan) dibangkitkan.',
    tip: 'Bangun pagi, regangkan tangan lalu baca doa ini sambil tersenyum. Ulangi 3 kali sebelum turun dari kasur.',
    source: 'HR. al-Bukhārī 6312 dan Muslim 2711',
    image: require('../../assets/doa/bangun-tidur.png'),
    video: v(
      'jwo2aihF0lA',
      'Yuk, Belajar Doa Sehari-Hari: Doa Bangun Tidur - Yufid Kids',
      'Yufid Kids'
    ),
  },
  {
    id: 'sebelum-tidur',
    title: 'Doa Sebelum Tidur',
    emoji: '🌙',
    arabic: 'بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا',
    latin: 'Bismika Allāhumma amūtu wa aḥyā',
    meaning: 'Dengan nama-Mu ya Allah, aku mati dan aku hidup.',
    tip: 'Pejamkan mata, tarik napas, lalu ucapkan perlahan. Jadikan doa ini hal terakhir sebelum tidur setiap malam.',
    source: 'HR. al-Bukhārī 6324',
    image: require('../../assets/doa/sebelum-tidur.png'),
    video: v(
      't5bzkTgatBE',
      'Doa Sebelum Tidur dan Bangun Tidur - Kastari Animation Official',
      'Kastari Sentra'
    ),
  },
  {
    id: 'sebelum-makan',
    title: 'Doa Sebelum Makan',
    emoji: '🍚',
    arabic: 'بِسْمِ اللَّهِ أَوَّلَهُ وَآخِرَهُ',
    latin: 'Bismillāhi awwalahu wa ākhirah',
    meaning: 'Dengan nama Allah (di) awal dan akhirnya.',
    tip: 'Angkat tangan sedikit, ucapkan "Bismillah" dengan jelas, lalu mulai makan dengan tangan kanan.',
    source: 'HR. Abu Dawud 3767',
    image: require('../../assets/doa/sebelum-makan.png'),
    video: v('WCEFOR5jgAU', 'Doa Sebelum Makan Bersama Jamal Laeli #1', 'Jamal Laeli'),
  },
  {
    id: 'sesudah-makan',
    title: 'Doa Sesudah Makan',
    emoji: '🍽️',
    arabic:
      'الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَذَا وَرَزَقَنِيهِ مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ',
    latin:
      "Alḥamdu lillāhilladzī aṭ'amanī hādzā wa razaqanīhi min ghairiḥawlin minnī wa lā quwwah",
    meaning:
      'Segala puji bagi Allah yang telah memberiku makanan ini dan merizkikannya kepadaku tanpa daya dan kekuatan apa pun dariku.',
    tip: 'Selesai makan, jangan langsung pergi. Duduk sebentar dan ucapkan terima kasih kepada Allah dengan doa ini.',
    source: 'HR. at-Tirmidzī 3458',
    image: require('../../assets/doa/sesudah-makan.png'),
    video: v(
      'SmKlP8Ma0Qg',
      'DOA SEBELUM MAKAN & SESUDAH MAKAN | SERI DOA HARIAN ANAK DAN BALITA',
      'Sunatman Dunia Ibu dan Anak'
    ),
  },
  {
    id: 'minum',
    title: 'Doa Minum',
    emoji: '💧',
    arabic: 'بِسْمِ اللَّهِ',
    latin: 'Bismillāh',
    meaning:
      'Dengan nama Allah. Sesudah minum ucapkan: Alḥamdu lillāh (Segala puji bagi Allah).',
    tip: 'Minum sambil duduk, tiga teguk, dan mulai dengan Bismillah. Selesai, ucapkan Alhamdulillah.',
    source: 'HR. at-Tirmidzī 3457 dan HR. Muslim 1343 (adab minum tiga teguk)',
    image: require('../../assets/doa/minum.png'),
    video: v(
      'bbKdXxPQnsg',
      'Doa Sebelum dan Sesudah Minum Arab Latin dan Artinya',
      'RIFDA CHAN'
    ),
  },
  {
    id: 'masuk-kamar-mandi',
    title: 'Doa Masuk Kamar Mandi',
    emoji: '🚿',
    arabic: 'اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنَ النَّجَاسَةِ',
    latin: "Allāhumma innī as'aluka minan najāsah",
    meaning:
      'Ya Allah, sesungguhnya aku memohon kepada-Mu dari (gangguan) kotoran (jin jahat).',
    tip: 'Ingat: masuk dengan kaki kiri, keluar dengan kaki kanan — sambil membaca doa ini.',
    source: 'HR. Abu Dawud 61 dan at-Tirmidzī 60',
    image: require('../../assets/doa/masuk-kamar-mandi.png'),
    video: v(
      'Wqjk3vfgMTs',
      'Yuk Belajar Doa Sehari-Hari: Doa Masuk dan Keluar Kamar Mandi',
      'Yufid Kids'
    ),
  },
  {
    id: 'keluar-kamar-mandi',
    title: 'Doa Keluar Kamar Mandi',
    emoji: '🧼',
    arabic: 'غُفْرَانَكَ',
    latin: 'Ghufrānak',
    meaning: 'Aku memohon ampunan-Mu.',
    tip: 'Doanya pendek sekali — cukup sekali baca sambil keluar. Mudah dihapalkan balita!',
    source: 'HR. Abu Dawud 62 dan at-Tirmidzī 61',
    image: require('../../assets/doa/keluar-kamar-mandi.png'),
    video: v(
      'Wqjk3vfgMTs',
      'Yuk Belajar Doa Sehari-Hari: Doa Masuk dan Keluar Kamar Mandi',
      'Yufid Kids'
    ),
  },
  {
    id: 'keluar-rumah',
    title: 'Doa Keluar Rumah',
    emoji: '🚪',
    arabic:
      'بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ',
    latin:
      "Bismillāhi tawakkaltu 'alallāh, wa lā ḥawla wa lā quwwata illā billāh",
    meaning:
      'Dengan nama Allah, aku bertawakal kepada Allah. Tidak ada daya dan tidak ada kekuatan kecuali dengan pertolongan Allah.',
    tip: 'Baca sebelum melangkah keluar pintu, misalnya berangkat sekolah tiap pagi.',
    source: 'HR. Abu Dawud 5095, at-Tirmidzī 3426, an-Nasā’ī 5483',
    image: require('../../assets/doa/keluar-rumah.png'),
    video: v(
      'YY3IA2Hq1gY',
      'Super Hero Seri 16-Doa Keluar Rumah-Anak Islam-Bersama Jamal Laeli',
      'Jamal Laeli'
    ),
  },
  {
    id: 'masuk-rumah',
    title: 'Doa Masuk Rumah',
    emoji: '🏠',
    arabic:
      'بِسْمِ اللَّهِ وَلَجْنَا وَبِسْمِ اللَّهِ خَرَجْنَا وَعَلَى رَبِّنَا تَوَكَّلْنَا',
    latin:
      "Bismillāhi walajnā, wa bismillāhi kharajnā, wa 'ala rabbin tawakkalnā",
    meaning:
      'Dengan nama Allah kami masuk, dengan nama Allah kami keluar, dan kepada Tuhan kami kami bertawakal.',
    tip: 'Ucapkan saat kaki melangkah masuk pintu — sepulang sekolah atau pulang dari main.',
    source: 'HR. Abu Dawud 5096',
    image: require('../../assets/doa/masuk-rumah.png'),
    video: v(
      'YHmvRufrq0k',
      'DOA MASUK RUMAH DAN KELUAR RUMAH | SERI DOA HARIAN ANAK DAN BALITA',
      'Sunatman Dunia Ibu dan Anak'
    ),
  },
  {
    id: 'naik-kendaraan',
    title: 'Doa Naik Kendaraan',
    emoji: '🚗',
    arabic:
      'سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ وَإِنَّا إِلَى رَبِّنَا لَمُنْقَلِبُونَ',
    latin:
      'Subḥānalladzī sakhkhara lanā hādzā wa mā kunnā lahu muqrinīna wa innā ilā rabbinā lamunqalibūn',
    meaning:
      'Maha Suci Allah yang telah memudahkan ini untuk kami, padahal sebelumnya kami tidak mampu menguasanya, dan sesungguhnya kami akan kembali kepada Tuhan kami.',
    tip: 'Baca sebelum mobil/motor berjalan, misalnya tiap berangkat sekolah atau mudik.',
    source: 'HR. Muslim 1342',
    image: require('../../assets/doa/naik-kendaraan.png'),
    video: v(
      'Ix4ajTSf7dg',
      'Doa Naik Kendaraan - Belajar Doa Harian - Yufid Kids',
      'Yufid Kids'
    ),
  },
  {
    id: 'sebelum-belajar',
    title: 'Doa Sebelum Belajar',
    emoji: '📚',
    arabic: 'رَبِّ زِدْنِي عِلْمًا',
    latin: 'Rabbī zidnī ‘ilmā',
    meaning: 'Ya Tuhanku, tambahkanlah ilmu kepadaku.',
    tip: 'Baca sambil duduk rapi di depan buku, sebelum guru atau orang tua mulai mengajar.',
    source: 'HR. at-Tirmidzī 2490 (doa Nabi Musa ‘alaihissalam)',
    image: require('../../assets/doa/sebelum-belajar.png'),
    video: v(
      '2WAahi4Rgrg',
      'Seri Doa-Doa Sebelum Belajar-Anak Islam-Bersama Jamal Laeli',
      'Jamal Laeli'
    ),
  },
  {
    id: 'masuk-masjid',
    title: 'Doa Masuk Masjid',
    emoji: '🕌',
    arabic: 'اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ',
    latin: "Allāhummaf-taḥ lī abwāba raḥmatik",
    meaning: 'Ya Allah, bukakanlah untukku pintu-pintu rahmat-Mu.',
    tip: 'Langkah kanan masuk masjid, lalu doa ini. Cocok dilatih tiap hari Jumat bersama keluarga.',
    source: 'HR. Muslim 713',
    image: require('../../assets/doa/masuk-masjid.png'),
    video: v('H03MXiIn-N4', 'Doa Masuk Masjid (Kartun Anak) - Yufid Kids', 'Yufid Kids'),
  },
  {
    id: 'keluar-masjid',
    title: 'Doa Keluar Masjid',
    emoji: '🙏',
    arabic: 'اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ',
    latin: "Allāhumma innī as'aluka min faḍlik",
    meaning: 'Ya Allah, sesungguhnya aku memohon kepada-Mu dari karunia-Mu.',
    tip: 'Langkah kiri keluar masjid, lalu ucapkan doa ini dengan harapan mendapat karunia Allah.',
    source: 'HR. Muslim 713',
    image: require('../../assets/doa/keluar-masjid.png'),
    video: v('CFf8OVhJFzA', 'Doa Keluar Masjid (Kartun Anak) - Yufid Kids', 'Yufid Kids'),
  },
  {
    id: 'pulang-sekolah',
    title: 'Doa Pulang Sekolah',
    emoji: '🎒',
    arabic: 'آيِبُونَ تَائِبُونَ عَابِدُونَ لِرَبِّنَا حَامِدُونَ',
    latin: "Āyibūna tā'ibūna 'ābidūna lirobbinā ḥāmidūn",
    meaning:
      'Kami pulang, kembali (dari perjalanan), bertaubat, beribadah kepada Tuhan kami dan memuji-Nya.',
    tip: 'Doa ini juga dibaca Nabi ﷺ saat pulang dari bepergian — pas untuk sepulang sekolah atau liburan.',
    source: 'HR. al-Bukhārī 1642 dan Muslim 1343',
    image: require('../../assets/doa/pulang-sekolah.png'),
    video: v(
      'nYPebyMT9Jc',
      'Lagu dan Doa Pulang Sekolah untuk Anak PAUD / TK / RA',
      'Iin Aina'
    ),
  },
];

export const getDoaById = (id?: string): Doa | undefined =>
  DOAS.find((d) => d.id === id);
