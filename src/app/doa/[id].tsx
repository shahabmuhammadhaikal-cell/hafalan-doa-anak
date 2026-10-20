import { Ionicons } from '@expo/vector-icons';
import { Redirect, router, useLocalSearchParams } from 'expo-router';
import {
  Image,
  Linking,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import YouTubeVideo from '@/components/YouTubeVideo';
import { getDoaById } from '@/data/doas';
import { colors, shadow } from '@/theme';

const STEPS = ['👂 Dengarkan', '👄 Ulangi', '🧠 Hafal'];

export default function DetailDoa() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const insets = useSafeAreaInsets();
  const doa = getDoaById(id);

  if (!doa) {
    return <Redirect href="/" />;
  }

  return (
    <View style={{ flex: 1, backgroundColor: colors.bg }}>
      {/* Bar atas */}
      <View style={[styles.topBar, { paddingTop: insets.top + 8 }]}>
        <Pressable style={styles.backBtn} onPress={() => router.back()}>
          <Ionicons name="chevron-back" size={24} color="#FFFFFF" />
        </Pressable>
        <Text style={styles.topTitle} numberOfLines={1}>
          {doa.emoji} {doa.title}
        </Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView
        contentContainerStyle={{ padding: 16, paddingBottom: 40 }}
        showsVerticalScrollIndicator={false}
      >
        {/* Ilustrasi */}
        <Image source={doa.image} style={styles.hero} resizeMode="cover" />

        {/* Teks doa */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>📖 Teks Doa</Text>
          <View style={styles.arabicBox}>
            <Text style={styles.arabic}>{doa.arabic}</Text>
          </View>
          <Text style={styles.latin}>{doa.latin}</Text>
          <View style={styles.divider} />
          <Text style={styles.meaningLabel}>Artinya:</Text>
          <Text style={styles.meaning}>{doa.meaning}</Text>
        </View>

        {/* Tips hafalan */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>💡 Tips Menghafal</Text>
          <Text style={styles.meaning}>{doa.tip}</Text>
          <View style={styles.stepsRow}>
            {STEPS.map((s, i) => (
              <View key={s} style={styles.step}>
                <Text style={styles.stepNum}>{i + 1}</Text>
                <Text style={styles.stepText}>{s}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Video YouTube */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>🎬 Video Pembelajaran</Text>
          <YouTubeVideo videoId={doa.video.id} />
          <Text style={styles.videoTitle}>{doa.video.title}</Text>
          <Text style={styles.videoChannel}>Channel: {doa.video.channel}</Text>
          <Pressable
            style={styles.watchBtn}
            onPress={() => Linking.openURL(doa.video.url)}
          >
            <Ionicons name="logo-youtube" size={16} color="#FFFFFF" />
            <Text style={styles.watchBtnText}>Tonton di YouTube</Text>
          </Pressable>
          <Text style={styles.footnote}>
            Video ditampilkan dengan embed resmi YouTube — hak cipta tetap milik
            channel {doa.video.channel}.
          </Text>
        </View>

        {/* Referensi */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>📚 Referensi</Text>
          <Text style={styles.refLabel}>Teks doa:</Text>
          <Text style={styles.refValue}>{doa.source}</Text>
          <Text style={[styles.refLabel, { marginTop: 10 }]}>Video:</Text>
          <Text style={styles.refValue}>
            {doa.video.title} — {doa.video.channel}
          </Text>
          <Text style={[styles.refLabel, { marginTop: 10 }]}>Ilustrasi:</Text>
          <Text style={styles.refValue}>
            Gambar orisinal hasil generasi skrip scripts/generate_assets.py —
            dibuat khusus untuk aplikasi ini (bebas copyright).
          </Text>
        </View>

        <Pressable style={styles.nextBtn} onPress={() => router.push('/')}>
          <Ionicons name="home" size={18} color="#FFFFFF" />
          <Text style={styles.nextBtnText}>Kembali ke daftar doa</Text>
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
  hero: {
    width: '100%',
    aspectRatio: 16 / 9,
    borderRadius: 20,
    marginBottom: 14,
  },
  card: {
    backgroundColor: colors.card,
    borderRadius: 22,
    padding: 16,
    marginBottom: 14,
    ...shadow,
  },
  cardTitle: {
    fontSize: 15,
    fontWeight: '900',
    color: colors.text,
    marginBottom: 10,
  },
  arabicBox: {
    backgroundColor: colors.arabicBg,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: colors.line,
    paddingVertical: 16,
    paddingHorizontal: 14,
  },
  arabic: {
    fontSize: 28,
    lineHeight: 56,
    textAlign: 'right',
    writingDirection: 'rtl',
    color: colors.text,
  },
  latin: {
    marginTop: 10,
    fontSize: 15,
    fontStyle: 'italic',
    lineHeight: 24,
    color: colors.primary,
    fontWeight: '600',
  },
  divider: {
    height: 1,
    backgroundColor: colors.line,
    marginVertical: 12,
  },
  meaningLabel: {
    fontSize: 12,
    fontWeight: '900',
    color: colors.muted,
    marginBottom: 4,
    textTransform: 'uppercase',
  },
  meaning: {
    fontSize: 14.5,
    lineHeight: 24,
    color: colors.text,
  },
  stepsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 14,
    gap: 8,
  },
  step: {
    flex: 1,
    backgroundColor: '#EEF6FF',
    borderRadius: 14,
    paddingVertical: 10,
    alignItems: 'center',
    gap: 4,
  },
  stepNum: {
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: colors.primary,
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '900',
    textAlign: 'center',
    lineHeight: 22,
  },
  stepText: {
    fontSize: 12,
    fontWeight: '700',
    color: colors.text,
  },
  videoTitle: {
    marginTop: 10,
    fontSize: 13.5,
    fontWeight: '800',
    color: colors.text,
    lineHeight: 19,
  },
  videoChannel: {
    marginTop: 3,
    fontSize: 12,
    color: colors.muted,
    fontWeight: '600',
  },
  watchBtn: {
    marginTop: 10,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#E53935',
    borderRadius: 999,
    paddingVertical: 11,
  },
  watchBtnText: {
    color: '#FFFFFF',
    fontSize: 13.5,
    fontWeight: '900',
  },
  footnote: {
    marginTop: 8,
    fontSize: 11,
    lineHeight: 16,
    color: colors.muted,
  },
  refLabel: {
    fontSize: 11.5,
    fontWeight: '900',
    color: colors.muted,
    textTransform: 'uppercase',
  },
  refValue: {
    marginTop: 2,
    fontSize: 13.5,
    lineHeight: 20,
    color: colors.text,
  },
  nextBtn: {
    marginTop: 4,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: colors.primary,
    borderRadius: 999,
    paddingVertical: 13,
  },
  nextBtnText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '900',
  },
});
