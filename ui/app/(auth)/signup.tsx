import React, { useState } from 'react';
import { Text, TextInput, Pressable, Alert, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { useRouter } from 'expo-router';
import { Button } from '../../components/shared/Button';
import { signup } from '../../lib/auth';

export default function SignupScreen() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [zip, setZip] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSignup() {
    if (!name || !email || !zip || !password) {
      Alert.alert('Missing fields', 'Please fill in all fields.');
      return;
    }
    setLoading(true);
    try {
      await signup({ name: name.trim(), email: email.trim(), zip: zip.trim(), password });
      router.replace('/');
    } catch {
      Alert.alert('Signup failed', 'That email may already be in use.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      className="flex-1 bg-[#f5f5f5] dark:bg-[#111]"
    >
      <ScrollView contentContainerClassName="px-6 pt-16 pb-8">
        <Text className="text-3xl font-bold text-[#111] dark:text-white mb-2">Create account</Text>
        <Text className="text-[#888] mb-8">Join your friend group on POSTscore</Text>

        {[
          { label: 'Name', value: name, set: setName, caps: 'words' as const },
          { label: 'Email', value: email, set: setEmail, caps: 'none' as const, keyboard: 'email-address' as const },
          { label: 'ZIP Code', value: zip, set: setZip, caps: 'none' as const, keyboard: 'numeric' as const },
        ].map(({ label, value, set, caps, keyboard }) => (
          <TextInput
            key={label}
            className="bg-white dark:bg-[#1c1c1e] rounded-xl px-4 py-4 text-base text-[#111] dark:text-white mb-3 border border-[#e5e5e5] dark:border-[#2a2a2a]"
            placeholder={label}
            placeholderTextColor="#888"
            autoCapitalize={caps}
            keyboardType={keyboard}
            value={value}
            onChangeText={set}
          />
        ))}

        <TextInput
          className="bg-white dark:bg-[#1c1c1e] rounded-xl px-4 py-4 text-base text-[#111] dark:text-white mb-6 border border-[#e5e5e5] dark:border-[#2a2a2a]"
          placeholder="Password"
          placeholderTextColor="#888"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />

        <Button label="Create account" onPress={handleSignup} loading={loading} />

        <Pressable className="mt-4 items-center" onPress={() => router.back()}>
          <Text className="text-[#888]">
            Have an account? <Text className="text-[#111] dark:text-white font-semibold">Log in</Text>
          </Text>
        </Pressable>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
