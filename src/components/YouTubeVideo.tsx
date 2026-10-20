import { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import YoutubePlayer from 'react-native-youtube-iframe';

type Props = {
  videoId: string;
};

/**
 * Pemutar YouTube resmi (IFrame Player lewat WebView).
 * Embed adalah cara yang diizinkan YouTube untuk menampilkan video kreator
 * — hak cipta tetap milik channel bersangkutan.
 */
export default function YouTubeVideo({ videoId }: Props) {
  const [ready, setReady] = useState(false);

  return (
    <View style={[styles.wrap, !ready && styles.placeholder]}>
      <YoutubePlayer
        height={220}
        videoId={videoId}
        onReady={() => setReady(true)}
        webViewProps={{
          allowsInlineMediaPlayback: true,
          mediaPlaybackRequiresUserAction: false,
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    width: '100%',
    borderRadius: 16,
    overflow: 'hidden',
    backgroundColor: '#000000',
  },
  placeholder: {
    opacity: 0.6,
  },
});
