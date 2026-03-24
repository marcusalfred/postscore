import * as SecureStore from 'expo-secure-store';
import { BASE_URL } from './api';

const TOKEN_KEY = 'postscore_token';

export async function getToken(): Promise<string | null> {
  return SecureStore.getItemAsync(TOKEN_KEY);
}

export async function setToken(token: string): Promise<void> {
  await SecureStore.setItemAsync(TOKEN_KEY, token);
}

export async function clearToken(): Promise<void> {
  await SecureStore.deleteItemAsync(TOKEN_KEY);
}

export async function login(email: string, password: string): Promise<string> {
  const res = await fetch(`${BASE_URL}/api/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username: email, password }).toString(),
  });
  if (!res.ok) throw new Error('Invalid credentials');
  const data = await res.json();
  await setToken(data.access_token);
  return data.access_token;
}

export async function signup(payload: {
  name: string;
  email: string;
  zip: string;
  password: string;
}): Promise<{ player: Record<string, unknown>; access_token: string }> {
  const res = await fetch(`${BASE_URL}/api/v1/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Signup failed');
  const data = await res.json();
  await setToken(data.access_token);
  return data;
}
