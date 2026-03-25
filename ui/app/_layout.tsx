import '../global.css';
import React, { useEffect, useState } from 'react';
import { Stack, useRouter, useSegments } from 'expo-router';
import { QueryClientProvider } from '@tanstack/react-query';
import { Appearance } from 'react-native';
import { queryClient } from '../lib/queryClient';
import { getToken } from '../lib/auth';
import { getTheme } from '../lib/storage';
import { startOfflineQueueProcessor } from '../lib/offlineQueue';

export default function RootLayout() {
  const router = useRouter();
  const segments = useSegments();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // Apply stored theme preference before first render
    getTheme().then((storedTheme) => {
      if (storedTheme && storedTheme !== 'system') {
        Appearance.setColorScheme(storedTheme);
      }
    }).catch(console.error);

    // Start offline queue processor
    const unsub = startOfflineQueueProcessor();
    return unsub;
  }, []);

  useEffect(() => {
    (async () => {
      const token = await getToken();
      const inAuthGroup = segments[0] === '(auth)';
      if (!token && !inAuthGroup) {
        router.replace('/login');
      } else if (token && inAuthGroup) {
        router.replace('/');
      }
      if (!ready) setReady(true);
    })();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [segments]);

  if (!ready) return null;

  return (
    <QueryClientProvider client={queryClient}>
      <Stack screenOptions={{ headerShown: false }} />
    </QueryClientProvider>
  );
}
