import React, { useState } from 'react';
import { View, Text, TextInput, Pressable, Alert, KeyboardAvoidingView, Platform } from 'react-native';
import { useRouter } from 'expo-router';
import { Button } from '../../components/shared/Button';
import { login } from '../../lib/auth';

export default function LoginScreen() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    if (!email || !password) return;
    setLoading(true);
    try {
      await login(email.trim(), password);
      router.replace('/');
    } catch {
      Alert.alert('Login failed', 'Check your email and password.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      className="flex-1 bg-[#f5f5f5] dark:bg-[#111] justify-center px-6"
    >
      <Text className="text-3xl font-bold text-[#111] dark:text-white mb-2">POSTscore</Text>
      <Text className="text-[#888] mb-8">Sign in to track your rounds</Text>

      <TextInput
        className="bg-white dark:bg-[#1c1c1e] rounded-xl px-4 py-4 text-base text-[#111] dark:text-white mb-3 border border-[#e5e5e5] dark:border-[#2a2a2a]"
        placeholder="Email"
        placeholderTextColor="#888"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        className="bg-white dark:bg-[#1c1c1e] rounded-xl px-4 py-4 text-base text-[#111] dark:text-white mb-6 border border-[#e5e5e5] dark:border-[#2a2a2a]"
        placeholder="Password"
        placeholderTextColor="#888"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <Button label="Log in" onPress={handleLogin} loading={loading} />

      <Pressable className="mt-4 items-center" onPress={() => router.push('/signup')}>
        <Text className="text-[#888]">
          No account? <Text className="text-[#111] dark:text-white font-semibold">Sign up</Text>
        </Text>
      </Pressable>
    </KeyboardAvoidingView>
  );
}
