import { Image, Pressable, StyleSheet, Text, View } from 'react-native';

import type { Doa } from '@/data/doas';
import { colors, shadow } from '@/theme';

type Props = {
  doa: Doa;
  onPress: () => void;
};

/** Kartu doa untuk grid beranda. */
export default function DoaCard({ doa, onPress }: Props) {
  return (
    <Pressable
      onPress={onPress}
      style={({ pressed }) => [styles.card, pressed && styles.pressed]}
    >
      <View style={styles.imageWrap}>
        <Image source={doa.image} style={styles.image} resizeMode="cover" />
        <View style={styles.badge}>
          <Text style={styles.badgeEmoji}>{doa.emoji}</Text>
        </View>
      </View>
      <View style={styles.body}>
        <Text style={styles.title} numberOfLines={2}>
          {doa.title}
        </Text>
        <View style={styles.metaRow}>
          <Text style={styles.meta}>🎬 Video + teks Arab</Text>
        </View>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    width: '48%',
    backgroundColor: colors.card,
    borderRadius: 20,
    marginBottom: 14,
    ...shadow,
  },
  pressed: {
    transform: [{ scale: 0.97 }],
    opacity: 0.95,
  },
  imageWrap: {
    width: '100%',
    aspectRatio: 16 / 9,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    overflow: 'hidden',
  },
  image: {
    width: '100%',
    height: '100%',
  },
  badge: {
    position: 'absolute',
    left: 8,
    bottom: 8,
    backgroundColor: 'rgba(255,255,255,0.92)',
    borderRadius: 16,
    width: 32,
    height: 32,
    alignItems: 'center',
    justifyContent: 'center',
  },
  badgeEmoji: {
    fontSize: 17,
  },
  body: {
    paddingHorizontal: 10,
    paddingVertical: 10,
  },
  title: {
    fontSize: 14,
    fontWeight: '800',
    color: colors.text,
    lineHeight: 18,
  },
  metaRow: {
    marginTop: 5,
  },
  meta: {
    fontSize: 10,
    color: colors.muted,
    fontWeight: '600',
  },
});
