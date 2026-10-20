import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';
import {
  Image,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import DoaCard from '@/components/DoaCard';
import { DOAS } from '@/data/doas';
import { colors, shadow } from '@/theme';

export default function Beranda() {
  const insets = useSafeAreaInsets();

  return (
    <ScrollView
      style={{ backgroundColor: colors.bg }}
      contentContainerStyle={{ paddingBottom: 32 }}
      showsVerticalScrollIndicator={false}
    >
      {/* Header gradasi */}
      <LinearGradient
        colors={['#4FC3F7', '#2F80ED']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={[styles.header, { paddingTop: insets.top + 20 }]}
      >
        <View style={styles.headerRow}>
          <View style={{ flex: 1 }}>
            <Text style={styles.appName}>Doa Anak</Text>
            <Text style={styles.appTagline}>
              Belajar & hafal doa sehari-hari 🌟
            </Text>
          </View>
          <View style={styles.logoBubble}>
            <Text style={styles.logoEmoji}>🕌</Text>
          </View>
        </View>

        <Image
          source={require('../../assets/header.png')}
          style={styles.banner}
          resizeMode="cover"
        />

        <View style={styles.chipsRow}>
          <View style={styles.chip}>
            <Text style={styles.chipText}>📖 {DOAS.length} doa</Text>
          </View>
          <View style={styles.chip}>
            <Text style={styles.chipText}>🎬 Video YouTube</Text>
          </View>
          <View style={styles.chip}>
            <Text style={styles.chipText}>✏️ Ilustrasi orisinal</Text>
          </View>
        </View>
      </LinearGradient>

      {/* Judul seksi */}
      <View style={styles.sectionHead}>
        <Text style={styles.sectionTitle}>Pilih doa yang mau dipelajari</Text>
        <Text style={styles.sectionSubtitle}>
          Ketuk kartu untuk melihat teks Arab, arti, dan videonya
        </Text>
      </View>

      {/* Grid doa dua kolom */}
      <View style={styles.grid}>
        {DOAS.map((doa) => (
          <DoaCard
            key={doa.id}
            doa={doa}
            onPress={() => router.push({ pathname: '/doa/[id]', params: { id: doa.id } })}
          />
        ))}
      </View>

      {/* Catatan referensi */}
      <View style={styles.noteCard}>
        <Text style={styles.noteTitle}>ℹ️ Tentang konten</Text>
        <Text style={styles.noteText}>
          • Teks doa bersumber dari hadits shahih (rujukan dicantumkan di tiap
          doa).{'\n'}
          • Semua gambar ilustrasi dibuat orisinal untuk aplikasi ini — bebas
          copyright.{'\n'}
          • Video YouTube ditampilkan dengan embed resmi; hak cipta tetap milik
          channel masing-masing.
        </Text>
        <Pressable style={styles.shareBtn} onPress={() => router.push('/tentang')}>
          <Ionicons name="information-circle" size={16} color="#FFFFFF" />
          <Text style={styles.shareBtnText}>Baca keterangan lengkap</Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  header: {
    paddingHorizontal: 18,
    paddingBottom: 22,
    borderBottomLeftRadius: 28,
    borderBottomRightRadius: 28,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  appName: {
    color: '#FFFFFF',
    fontSize: 30,
    fontWeight: '900',
    letterSpacing: 0.5,
  },
  appTagline: {
    color: '#EAF6FF',
    fontSize: 14,
    marginTop: 2,
    fontWeight: '600',
  },
  logoBubble: {
    backgroundColor: 'rgba(255,255,255,0.25)',
    width: 56,
    height: 56,
    borderRadius: 28,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoEmoji: {
    fontSize: 30,
  },
  banner: {
    width: '100%',
    height: 150,
    borderRadius: 20,
    marginTop: 16,
  },
  chipsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginTop: 14,
  },
  chip: {
    backgroundColor: 'rgba(255,255,255,0.22)',
    borderRadius: 999,
    paddingHorizontal: 12,
    paddingVertical: 6,
  },
  chipText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '700',
  },
  sectionHead: {
    paddingHorizontal: 18,
    marginTop: 22,
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '900',
    color: colors.text,
  },
  sectionSubtitle: {
    fontSize: 13,
    color: colors.muted,
    marginTop: 3,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    paddingHorizontal: 14,
  },
  noteCard: {
    marginTop: 10,
    marginHorizontal: 18,
    backgroundColor: '#FFF7E6',
    borderRadius: 20,
    padding: 16,
    borderWidth: 1,
    borderColor: '#FFE7B3',
    ...shadow,
  },
  noteTitle: {
    fontSize: 14,
    fontWeight: '900',
    color: '#8A5B00',
    marginBottom: 6,
  },
  noteText: {
    fontSize: 12.5,
    lineHeight: 20,
    color: '#7A5A1E',
  },
  shareBtn: {
    marginTop: 12,
    alignSelf: 'flex-start',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: colors.primary,
    borderRadius: 999,
    paddingHorizontal: 14,
    paddingVertical: 8,
  },
  shareBtnText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '800',
  },
});
