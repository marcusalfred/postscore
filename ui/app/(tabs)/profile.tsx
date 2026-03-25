import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Pressable, Alert, ScrollView, Appearance } from 'react-native';
import { useRouter } from 'expo-router';
import { useCurrentPlayer, useUpdatePlayer } from '../../lib/queries';
import { clearToken } from '../../lib/auth';
import { getTheme, setTheme } from '../../lib/storage';
import { Button } from '../../components/shared/Button';
import { Avatar } from '../../components/shared/Avatar';

const THEME_OPTIONS = ['system', 'light', 'dark'] as const;
type ThemeOption = typeof THEME_OPTIONS[number];

export default function ProfileScreen() {
  const router = useRouter();
  const { data: me, isLoading } = useCurrentPlayer();
  const updatePlayer = useUpdatePlayer();
  const [name, setName] = useState('');
  const [handicap, setHandicap] = useState('');
  const [theme, setThemeLocal] = useState<ThemeOption>('system');

  useEffect(() => {
    if (me) { setName(me.name); setHandicap(me.handicap !== null ? String(me.handicap) : ''); }
    getTheme().then((t) => setThemeLocal((t as ThemeOption) ?? 'system'));
  }, [me]);

  async function handleSave() {
    if (!me) return;
    try {
      await updatePlayer.mutateAsync({
        playerId: me.id,
        data: {
          name: name.trim() || undefined,
          handicap: handicap ? parseFloat(handicap) : undefined,
        },
      });
      Alert.alert('Saved');
    } catch {
      Alert.alert('Error', 'Could not save changes.');
    }
  }

  async function handleThemeChange(t: ThemeOption) {
    setThemeLocal(t);
    await setTheme(t);
    Appearance.setColorScheme(t !== 'system' ? t : 'unspecified');
  }

  async function handleLogout() {
    await clearToken();
    router.replace('/login');
  }

  if (isLoading) return null;

  return (
    <ScrollView className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      <View className="px-4 pt-12 pb-6">
        <Pressable onPress={() => router.back()} hitSlop={8} className="mb-6">
          <Text className="text-[#888]">{'\u2190'} Back</Text>
        </Pressable>

        <View className="items-center mb-8">
          <Avatar name={me?.name ?? ''} size={72} />
          <Text className="text-xl font-bold text-[#111] dark:text-white mt-3">{me?.name}</Text>
          <Text className="text-[#888]">{me?.email}</Text>
        </View>

        <Text className="text-xs font-semibold text-[#888] uppercase tracking-wide mb-2">Name</Text>
        <TextInput
          className="bg-white dark:bg-[#1c1c1e] rounded-xl px-4 py-4 text-base text-[#111] dark:text-white mb-4 border border-[#e5e5e5] dark:border-[#2a2a2a]"
          value={name}
          onChangeText={setName}
          autoCapitalize="words"
        />

        <Text className="text-xs font-semibold text-[#888] uppercase tracking-wide mb-2">Handicap</Text>
        <TextInput
          className="bg-white dark:bg-[#1c1c1e] rounded-xl px-4 py-4 text-base text-[#111] dark:text-white mb-6 border border-[#e5e5e5] dark:border-[#2a2a2a]"
          value={handicap}
          onChangeText={setHandicap}
          keyboardType="decimal-pad"
          placeholder={'\u2014'}
          placeholderTextColor="#888"
        />

        <Button label="Save" onPress={handleSave} loading={updatePlayer.isPending} />

        <Text className="text-xs font-semibold text-[#888] uppercase tracking-wide mt-8 mb-3">Appearance</Text>
        <View className="flex-row gap-2">
          {THEME_OPTIONS.map((t) => (
            <Pressable
              key={t}
              onPress={() => handleThemeChange(t)}
              className={`flex-1 py-2 rounded-xl border items-center ${theme === t ? 'bg-[#111] dark:bg-white border-transparent' : 'bg-white dark:bg-[#1c1c1e] border-[#e5e5e5] dark:border-[#2a2a2a]'}`}
            >
              <Text className={`text-sm font-semibold capitalize ${theme === t ? 'text-white dark:text-[#111]' : 'text-[#111] dark:text-white'}`}>
                {t}
              </Text>
            </Pressable>
          ))}
        </View>

        <Pressable onPress={handleLogout} className="mt-8 items-center py-4">
          <Text className="text-[#e53935] font-semibold">Log out</Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}
