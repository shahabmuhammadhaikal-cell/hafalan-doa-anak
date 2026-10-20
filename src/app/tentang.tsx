import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { colors, shadow } from '@/theme';

const SECTIONS = [
  {
    icon: '📖',
    title: 'Teks doa',
    body: 'Berasal dari hadits shahih yang diriwayatkan ulama besar (al-Bukhārī, Muslim, at-Tirmidzī, Abu Dawud, an-Nasā’ī). Teks keagamaan berupa warisan riwayat dan tidak terikat copyright. Rujukan hadits dicantumkan pada tiap doa.',
  },
  {
    icon: '✏️',
    title: 'Gambar ilustrasi',
    body: 'Semua gambar pada aplikasi ini dibuat orisinal dari nol dengan skrip scripts/generate_assets.py (bentuk vektor sederhana yang digambar program). Tidak ada gambar yang diunduh atau disalin dari pihak lain, sehingga bebas copyright.',
  },
  {
    icon: '🎬',
    title: 'Video YouTube',
    body: 'Video ditampilkan melalui embed resmi YouTube (IFrame Player). Cara ini diizinkan oleh YouTube dan pemilik video; hak cipta tetap sepenuhnya milik channel masing-masing. Aplikasi tidak mengunduh, menyalin, atau mendistribusikan ulang video. Semua video dicek lewat endpoint oEmbed YouTube dan dalam keadaan mengizinkan embedding.',
  },
  {
    icon: '🔤',
    title: 'Font & emoji',
    body: 'Aplikasi memakai font bawaan sistem perangkat dan emoji bawaan sistem — tidak menyertakan font pihak ketiga.',
  },
  {
    icon: '🕌',
    title: 'Tujuan aplikasi',
    body: 'Aplikasi edukasi non-komersial untuk membantu anak-anak menghafal doa harian. Bila Anda kreator video yang tercantum dan keberatan, silakan hubungi pengembang untuk penghapusan tautan.',
  },
];

export default function Tentang() {
  const insets = useSafeAreaInsets();

  return (
    <View style={{ flex: 1, backgroundColor: colors.bg }}>
      <View style={[styles.topBar, { paddingTop: insets.top + 8 }]}>
        <Pressable style={styles.backBtn} onPress={() => router.back()}>
          <Ionicons name="chevron-back" size={24} color="#FFFFFF" />
        </Pressable>
        <Text style={styles.topTitle}>Tentang & Referensi</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView
        contentContainerStyle={{ padding: 16, paddingBottom: 40 }}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.heroBox}>
          <Text style={styles.heroEmoji}>🌟</Text>
          <Text style={styles.heroTitle}>Doa Anak</Text>
          <Text style={styles.heroSub}>
            Aplikasi edukasi hafalan doa harian untuk anak — aman dari
            masalah copyright.
          </Text>
        </View>

        {SECTIONS.map((s) => (
          <View key={s.title} style={styles.card}>
            <Text style={styles.cardTitle}>
              {s.icon} {s.title}
            </Text>
            <Text style={styles.cardBody}>{s.body}</Text>
          </View>
        ))}

        <View style={styles.card}>
          <Text style={styles.cardTitle}>🔗 Saluran video yang digunakan</Text>
          <Text style={styles.cardBody}>
            {'• Yufid Kids\n• Jamal Laeli\n• Kastari Sentra\n• Sunatman Dunia Ibu dan Anak\n• RIFDA CHAN\n• Iin Aina'}
          </Text>
          <Text style={[styles.cardBody, { marginTop: 8 }]}>
            Atribusi lengkap (judul + channel + tautan) juga tampil di halaman
            tiap doa.
          </Text>
        </View>

        <Pressable style={styles.homeBtn} onPress={() => router.push('/')}>
          <Ionicons name="home" size={18} color="#FFFFFF" />
          <Text style={styles.homeBtnText}>Kembali ke beranda</Text>
        </Pressable>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  topBar: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    backgroundColor: colors.primary,
    paddingHorizontal: 12,
    paddingBottom: 12,
  },
  backBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  topTitle: {
    flex: 1,
    color: '#FFFFFF',
    fontSize: 17,
    fontWeight: '900',
  },
  heroBox: {
    backgroundColor: '#EEF6FF',
    borderRadius: 22,
    padding: 20,
    alignItems: 'center',
    marginBottom: 14,
    borderWidth: 1,
    borderColor: colors.line,
    ...shadow,
  },
  heroEmoji: {
    fontSize: 40,
  },
  heroTitle: {
    fontSize: 22,
    fontWeight: '900',
    color: colors.text,
    marginTop: 6,
  },
  heroSub: {
    fontSize: 13.5,
    color: colors.muted,
    textAlign: 'center',
    marginTop: 6,
    lineHeight: 20,
  },
  card: {
    backgroundColor: colors.card,
    borderRadius: 22,
    padding: 16,
    marginBottom: 12,
    ...shadow,
  },
  cardTitle: {
    fontSize: 14.5,
    fontWeight: '900',
    color: colors.text,
    marginBottom: 8,
  },
  cardBody: {
    fontSize: 13.5,
    lineHeight: 22,
    color: colors.muted,
  },
  homeBtn: {
    marginTop: 6,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: colors.primary,
    borderRadius: 999,
    paddingVertical: 13,
  },
  homeBtnText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '900',
  },
});
