# POSTscore UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a mobile-first Expo app (iOS/Android/web) that lets a friend group record golf rounds hole-by-hole and review stats and standings.

**Architecture:** Expo Router file-based navigation with three bottom tabs (Play, Rounds, Friends) and a Profile screen accessible from the Friends header. TanStack Query manages server state; AsyncStorage holds the in-progress round and offline queue; SecureStore holds the JWT token.

**Tech Stack:** Expo SDK 52, Expo Router v4, React Native, NativeWind v4 (Tailwind), TanStack Query v5, @react-native-async-storage/async-storage, @react-native-community/netinfo, expo-secure-store, Jest + jest-expo + @testing-library/react-native.

---

## File Map

### Created from scratch

```
ui/                                         # Expo project root
  app/
    _layout.tsx                             # Root layout — auth guard + theme provider
    (auth)/
      _layout.tsx                           # Auth stack layout (no tab bar)
      login.tsx                             # Login screen
      signup.tsx                            # Signup screen
    (tabs)/
      _layout.tsx                           # Tab bar definition
      index.tsx                             # Play tab (Start Round / Live Scorecard)
      rounds.tsx                            # Round history list
      rounds/[id].tsx                       # Round summary
      friends.tsx                           # Friends leaderboard
      profile.tsx                           # Profile / settings
  components/
    shared/
      Button.tsx                            # Primary + secondary variants
      Card.tsx                              # Surface container
      Avatar.tsx                            # Initials-based avatar
      ScoreLabel.tsx                        # Coloured +/-/E to-par label
    scorecard/
      ScoreStepper.tsx                      # −/value/+ control with par label
      PuttsStepper.tsx                      # 0-6 putts counter
      StatToggle.tsx                        # Multi-option pill toggle (GIR, Fairway)
      HoleProgress.tsx                      # Dot row: completed/current/upcoming
      HoleCard.tsx                          # Full current-hole panel
    rounds/
      RoundCard.tsx                         # History list item
      StatsGrid.tsx                         # Stats row on Round Summary
  lib/
    api.ts                                  # Typed fetch wrapper (base URL + auth header)
    auth.ts                                 # Login, signup, token SecureStore helpers
    queries.ts                              # TanStack Query hooks
    storage.ts                              # AsyncStorage helpers + offline queue
  constants/
    theme.ts                                # Color tokens for light + dark
  __tests__/
    lib/
      api.test.ts
      auth.test.ts
      storage.test.ts
    components/
      shared/Button.test.tsx
      shared/ScoreLabel.test.tsx
      shared/Avatar.test.tsx
      scorecard/ScoreStepper.test.tsx
      scorecard/PuttsStepper.test.tsx
      scorecard/StatToggle.test.tsx
      scorecard/HoleProgress.test.tsx
      scorecard/HoleCard.test.tsx
```

---

## Task 1: Scaffold Expo Project

**Files:**
- Create: `ui/` (entire project)
- Create: `ui/app.json`
- Create: `ui/.env.local`

- [ ] **Step 1: Create the Expo project**

Run from repo root:
```bash
npx create-expo-app@latest ui --template blank-typescript
cd ui
```

- [ ] **Step 2: Install all dependencies**

```bash
npx expo install expo-router expo-secure-store @react-native-async-storage/async-storage @react-native-community/netinfo
npm install nativewind@^4 tailwindcss@^3 @tanstack/react-query
npm install --save-dev jest-expo @testing-library/react-native @testing-library/jest-native babel-plugin-module-resolver
```

- [ ] **Step 3: Configure Expo Router in `app.json`**

Replace contents:
```json
{
  "expo": {
    "name": "POSTscore",
    "slug": "postscore",
    "version": "1.0.0",
    "scheme": "postscore",
    "web": {
      "bundler": "metro",
      "output": "static"
    },
    "plugins": [
      "expo-router",
      "expo-secure-store"
    ],
    "experiments": {
      "typedRoutes": true
    }
  }
}
```

- [ ] **Step 4: Configure NativeWind — create `tailwind.config.js`**

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,jsx,ts,tsx}', './components/**/*.{js,jsx,ts,tsx}'],
  presets: [require('nativewind/preset')],
  theme: { extend: {} },
  plugins: [],
};
```

- [ ] **Step 5: Update `babel.config.js`**

```js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: [
      ['babel-preset-expo', { jsxImportSource: 'nativewind' }],
      'nativewind/babel',
    ],
  };
};
```

- [ ] **Step 6: Add Metro config for NativeWind — create `metro.config.js`**

```js
const { getDefaultConfig } = require('expo/metro-config');
const { withNativeWind } = require('nativewind/metro');
const config = getDefaultConfig(__dirname);
module.exports = withNativeWind(config, { input: './global.css' });
```

- [ ] **Step 7: Create `global.css`**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- [ ] **Step 8: Configure Jest in `package.json` — add jest block**

```json
"jest": {
  "preset": "jest-expo",
  "setupFilesAfterFrameworks": ["@testing-library/jest-native/extend-expect"],
  "transformIgnorePatterns": [
    "node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg)"
  ]
}
```

- [ ] **Step 9: Create environment file `ui/.env.local`**

```
EXPO_PUBLIC_API_URL=http://localhost:8000
```

- [ ] **Step 10: Create `nativewind-env.d.ts` for TypeScript**

```ts
/// <reference types="nativewind/types" />
```

- [ ] **Step 11: Verify the project starts**

```bash
npx expo start --web
```
Expected: Expo dev server starts, opens browser (will show blank screen — that's fine)

- [ ] **Step 12: Commit**

```bash
git add ui/
git commit -m "feat: scaffold Expo project with Router, NativeWind, TanStack Query"
```

---

## Task 2: Theme Constants

**Files:**
- Create: `ui/constants/theme.ts`

- [ ] **Step 1: Create the theme file**

```ts
// ui/constants/theme.ts

export const Colors = {
  light: {
    background: '#f5f5f5',
    surface: '#ffffff',
    surfaceElevated: '#f0f0f0',
    textPrimary: '#111111',
    textSecondary: '#888888',
    textMuted: '#bbbbbb',
    border: '#e5e5e5',
    actionBg: '#111111',
    actionText: '#ffffff',
  },
  dark: {
    background: '#111111',
    surface: '#1c1c1e',
    surfaceElevated: '#2a2a2a',
    textPrimary: '#ffffff',
    textSecondary: '#666666',
    textMuted: '#444444',
    border: '#2a2a2a',
    actionBg: '#ffffff',
    actionText: '#111111',
  },
  // Scoring accents — same in both modes
  birdie: '#43a047',
  bogey: '#e53935',
} as const;

export type ColorScheme = 'light' | 'dark';
```

- [ ] **Step 2: Commit**

```bash
git add ui/constants/theme.ts
git commit -m "feat: add theme color tokens"
```

---

## Task 3: Shared Components

**Files:**
- Create: `ui/components/shared/Button.tsx`
- Create: `ui/components/shared/Card.tsx`
- Create: `ui/components/shared/Avatar.tsx`
- Create: `ui/components/shared/ScoreLabel.tsx`
- Create: `ui/__tests__/components/shared/Button.test.tsx`
- Create: `ui/__tests__/components/shared/ScoreLabel.test.tsx`
- Create: `ui/__tests__/components/shared/Avatar.test.tsx`

### Button

- [ ] **Step 1: Write the failing Button test**

```tsx
// ui/__tests__/components/shared/Button.test.tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { Button } from '../../../components/shared/Button';

describe('Button', () => {
  it('renders label', () => {
    const { getByText } = render(<Button label="Log in" onPress={() => {}} />);
    expect(getByText('Log in')).toBeTruthy();
  });

  it('calls onPress when tapped', () => {
    const onPress = jest.fn();
    const { getByText } = render(<Button label="Go" onPress={onPress} />);
    fireEvent.press(getByText('Go'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });

  it('is disabled when loading', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <Button label="Go" onPress={onPress} loading />
    );
    fireEvent.press(getByText('Go'));
    expect(onPress).not.toHaveBeenCalled();
  });
});
```

- [ ] **Step 2: Run to confirm it fails**

```bash
cd ui && npx jest __tests__/components/shared/Button.test.tsx
```
Expected: FAIL — module not found

- [ ] **Step 3: Implement Button**

```tsx
// ui/components/shared/Button.tsx
import React from 'react';
import { Pressable, Text, ActivityIndicator } from 'react-native';

type Props = {
  label: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary';
  loading?: boolean;
  disabled?: boolean;
};

export function Button({
  label,
  onPress,
  variant = 'primary',
  loading = false,
  disabled = false,
}: Props) {
  const isPrimary = variant === 'primary';
  const isDisabled = disabled || loading;

  return (
    <Pressable
      onPress={isDisabled ? undefined : onPress}
      className={`rounded-xl px-6 py-4 items-center justify-center ${
        isPrimary
          ? 'bg-[#111] dark:bg-white'
          : 'border border-[#e5e5e5] dark:border-[#2a2a2a]'
      } ${isDisabled ? 'opacity-40' : ''}`}
    >
      {loading ? (
        <ActivityIndicator color={isPrimary ? '#fff' : '#111'} />
      ) : (
        <Text
          className={`font-semibold text-base ${
            isPrimary ? 'text-white dark:text-[#111]' : 'text-[#111] dark:text-white'
          }`}
        >
          {label}
        </Text>
      )}
    </Pressable>
  );
}
```

- [ ] **Step 4: Run to confirm it passes**

```bash
npx jest __tests__/components/shared/Button.test.tsx
```
Expected: 3 tests PASS

### ScoreLabel

- [ ] **Step 5: Write the failing ScoreLabel test**

```tsx
// ui/__tests__/components/shared/ScoreLabel.test.tsx
import React from 'react';
import { render } from '@testing-library/react-native';
import { ScoreLabel } from '../../../components/shared/ScoreLabel';

describe('ScoreLabel', () => {
  it('shows E for even par', () => {
    const { getByText } = render(<ScoreLabel toPar={0} />);
    expect(getByText('E')).toBeTruthy();
  });

  it('shows +2 with red colour for over par', () => {
    const { getByText } = render(<ScoreLabel toPar={2} />);
    expect(getByText('+2')).toBeTruthy();
  });

  it('shows -1 with green colour for under par', () => {
    const { getByText } = render(<ScoreLabel toPar={-1} />);
    expect(getByText('-1')).toBeTruthy();
  });
});
```

- [ ] **Step 6: Implement ScoreLabel**

```tsx
// ui/components/shared/ScoreLabel.tsx
import React from 'react';
import { Text } from 'react-native';

type Props = { toPar: number; size?: 'sm' | 'md' | 'lg' };

export function ScoreLabel({ toPar, size = 'md' }: Props) {
  const label = toPar === 0 ? 'E' : toPar > 0 ? `+${toPar}` : `${toPar}`;
  const colorClass =
    toPar < 0
      ? 'text-[#43a047]'
      : toPar > 0
      ? 'text-[#e53935]'
      : 'text-[#888]';
  const sizeClass =
    size === 'lg' ? 'text-2xl font-bold' : size === 'sm' ? 'text-sm' : 'text-base font-semibold';

  return <Text className={`${colorClass} ${sizeClass}`}>{label}</Text>;
}
```

- [ ] **Step 7: Write the failing Avatar test**

```tsx
// ui/__tests__/components/shared/Avatar.test.tsx
import React from 'react';
import { render } from '@testing-library/react-native';
import { Avatar } from '../../../components/shared/Avatar';

it('renders initials from name', () => {
  const { getByText } = render(<Avatar name="Alex Golfer" />);
  expect(getByText('AG')).toBeTruthy();
});
```

- [ ] **Step 7a: Run to confirm it fails**

```bash
npx jest __tests__/components/shared/Avatar.test.tsx
```
Expected: FAIL — module not found

- [ ] **Step 7b: Implement Avatar**

```tsx
// ui/components/shared/Avatar.tsx
import React from 'react';
import { View, Text } from 'react-native';

type Props = { name: string; size?: number };

export function Avatar({ name, size = 40 }: Props) {
  const initials = name
    .split(' ')
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() ?? '')
    .join('');

  return (
    <View
      style={{ width: size, height: size, borderRadius: size / 2 }}
      className="bg-[#e5e5e5] dark:bg-[#2a2a2a] items-center justify-center"
    >
      <Text className="font-bold text-[#111] dark:text-white" style={{ fontSize: size * 0.35 }}>
        {initials}
      </Text>
    </View>
  );
}
```

```tsx
// ui/components/shared/Card.tsx
import React from 'react';
import { View, ViewProps } from 'react-native';

export function Card({ children, style, ...props }: ViewProps) {
  return (
    <View
      className="bg-white dark:bg-[#1c1c1e] rounded-2xl p-4 shadow-sm"
      style={style}
      {...props}
    >
      {children}
    </View>
  );
}
```

- [ ] **Step 8: Run all shared component tests**

```bash
npx jest __tests__/components/shared/
```
Expected: all PASS

- [ ] **Step 9: Commit**

```bash
git add components/ __tests__/components/shared/
git commit -m "feat: add shared components (Button, Card, Avatar, ScoreLabel)"
```

---

## Task 4: API and Auth Library

**Files:**
- Create: `ui/lib/api.ts`
- Create: `ui/lib/auth.ts`
- Create: `ui/__tests__/lib/api.test.ts`
- Create: `ui/__tests__/lib/auth.test.ts`

- [ ] **Step 1: Write the failing API tests**

```ts
// ui/__tests__/lib/api.test.ts
import { buildRequest, BASE_URL } from '../../lib/api';

describe('buildRequest', () => {
  it('builds a JSON GET request with auth header', () => {
    const req = buildRequest('GET', '/api/v1/courses/', 'tok123');
    expect(req.method).toBe('GET');
    expect(req.headers.get('Authorization')).toBe('Bearer tok123');
    expect(req.url).toBe(`${BASE_URL}/api/v1/courses/`);
  });

  it('builds a form-encoded POST for login', () => {
    const req = buildRequest('POST', '/api/v1/auth/login', null, {
      formEncoded: true,
      body: { username: 'a@b.com', password: 'pass' },
    });
    expect(req.headers.get('Content-Type')).toContain('application/x-www-form-urlencoded');
  });

  it('builds a JSON POST with body', () => {
    const req = buildRequest('POST', '/api/v1/rounds/', 'tok', {
      body: { course_id: '123' },
    });
    expect(req.headers.get('Content-Type')).toBe('application/json');
  });
});
```

- [ ] **Step 2: Run to confirm failure**

```bash
npx jest __tests__/lib/api.test.ts
```

- [ ] **Step 3: Implement `lib/api.ts`**

```ts
// ui/lib/api.ts
export const BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

type RequestOptions = {
  body?: Record<string, unknown>;
  formEncoded?: boolean;
};

export function buildRequest(
  method: string,
  path: string,
  token: string | null,
  options: RequestOptions = {}
): Request {
  const headers = new Headers();
  if (token) headers.set('Authorization', `Bearer ${token}`);

  let body: BodyInit | undefined;

  if (options.body) {
    if (options.formEncoded) {
      headers.set('Content-Type', 'application/x-www-form-urlencoded');
      body = new URLSearchParams(options.body as Record<string, string>).toString();
    } else {
      headers.set('Content-Type', 'application/json');
      body = JSON.stringify(options.body);
    }
  }

  return new Request(`${BASE_URL}${path}`, { method, headers, body });
}

export async function apiFetch<T>(
  method: string,
  path: string,
  token: string | null,
  options: RequestOptions = {}
): Promise<T> {
  const req = buildRequest(method, path, token, options);
  const res = await fetch(req);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}
```

- [ ] **Step 4: Run to confirm tests pass**

```bash
npx jest __tests__/lib/api.test.ts
```

- [ ] **Step 5: Implement `lib/auth.ts`**

Note: `expo-secure-store` cannot run in Jest (native module). Mock it in tests.

```ts
// ui/lib/auth.ts
import * as SecureStore from 'expo-secure-store';
import { apiFetch, BASE_URL } from './api';

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
```

- [ ] **Step 6: Write auth tests with SecureStore mocked**

Create `ui/__mocks__/expo-secure-store.ts`:
```ts
const store: Record<string, string> = {};
export const getItemAsync = jest.fn(async (key: string) => store[key] ?? null);
export const setItemAsync = jest.fn(async (key: string, val: string) => { store[key] = val; });
export const deleteItemAsync = jest.fn(async (key: string) => { delete store[key]; });
```

```ts
// ui/__tests__/lib/auth.test.ts
import { getToken, setToken, clearToken } from '../../lib/auth';

// SecureStore is mocked via __mocks__/expo-secure-store.ts
beforeEach(() => jest.clearAllMocks());

it('stores and retrieves a token', async () => {
  await setToken('abc123');
  const tok = await getToken();
  expect(tok).toBe('abc123');
});

it('clears the token', async () => {
  await setToken('abc123');
  await clearToken();
  const tok = await getToken();
  expect(tok).toBeNull();
});
```

- [ ] **Step 7: Run auth tests**

```bash
npx jest __tests__/lib/auth.test.ts
```
Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add lib/ __tests__/lib/ __mocks__/
git commit -m "feat: add api fetch wrapper and auth token helpers"
```

---

## Task 5: AsyncStorage Helpers

**Files:**
- Create: `ui/lib/storage.ts`
- Create: `ui/__tests__/lib/storage.test.ts`

- [ ] **Step 1: Create mock for AsyncStorage**

Create `ui/__mocks__/@react-native-async-storage/async-storage.ts`:
```ts
const store: Record<string, string> = {};
export default {
  getItem: jest.fn(async (key: string) => store[key] ?? null),
  setItem: jest.fn(async (key: string, val: string) => { store[key] = val; }),
  removeItem: jest.fn(async (key: string) => { delete store[key]; }),
  multiRemove: jest.fn(async (keys: string[]) => keys.forEach(k => delete store[k])),
};
```

- [ ] **Step 2: Write the failing storage tests**

```ts
// ui/__tests__/lib/storage.test.ts
import {
  saveActiveRound,
  getActiveRound,
  clearActiveRound,
  enqueueOfflineHole,
  getOfflineQueue,
  removeFromQueue,
  getTheme,
  setTheme,
} from '../../lib/storage';

beforeEach(() => jest.clearAllMocks());

const mockRound = {
  round_id: 'r1',
  course_id: 'c1',
  tee_box_id: 't1',
  tee_box_holes: [{ id: 'h1', number: 1, par: 4, yards: 420 }],
  holes_total: 18,
  scored_holes: [],
};

it('saves and retrieves an active round', async () => {
  await saveActiveRound(mockRound);
  const result = await getActiveRound();
  expect(result?.round_id).toBe('r1');
  expect(result?.scored_holes).toEqual([]);
});

it('clears the active round', async () => {
  await saveActiveRound(mockRound);
  await clearActiveRound();
  const result = await getActiveRound();
  expect(result).toBeNull();
});

it('enqueues and retrieves offline holes', async () => {
  const hole = { round_id: 'r1', tee_box_hole_id: 'h1', score: 4, gir: true, putts: 2 };
  await enqueueOfflineHole(hole);
  const queue = await getOfflineQueue();
  expect(queue).toHaveLength(1);
  expect(queue[0].score).toBe(4);
});

it('removes an item from the queue by index', async () => {
  const hole = { round_id: 'r1', tee_box_hole_id: 'h1', score: 4, gir: true, putts: 2 };
  await enqueueOfflineHole(hole);
  await removeFromQueue(0);
  const queue = await getOfflineQueue();
  expect(queue).toHaveLength(0);
});

it('saves and retrieves theme preference', async () => {
  await setTheme('dark');
  const theme = await getTheme();
  expect(theme).toBe('dark');
});
```

- [ ] **Step 3: Run to confirm failure**

```bash
npx jest __tests__/lib/storage.test.ts
```

- [ ] **Step 4: Implement `lib/storage.ts`**

```ts
// ui/lib/storage.ts
import AsyncStorage from '@react-native-async-storage/async-storage';

const KEYS = {
  ACTIVE_ROUND: 'postscore_active_round',
  OFFLINE_QUEUE: 'postscore_offline_queue',
  THEME: 'postscore_theme',
};

export type TeeBoxHoleStub = {
  id: string;
  number: number;
  par: number;
  yards: number;
};

export type ScoredHoleEntry = {
  holeNumber: number;
  toPar: number;
};

export type ActiveRound = {
  round_id: string;
  course_id: string;
  tee_box_id: string;
  tee_box_holes: TeeBoxHoleStub[];
  holes_total: number;
  scored_holes: ScoredHoleEntry[]; // tracks hole number AND to-par for progress dot colouring
};

export type OfflineHolePayload = {
  round_id: string;
  tee_box_hole_id: string;
  score: number;
  gir: boolean;
  putts: number;
  fairway?: string;
  penalties?: number;
};

export async function saveActiveRound(round: ActiveRound): Promise<void> {
  await AsyncStorage.setItem(KEYS.ACTIVE_ROUND, JSON.stringify(round));
}

export async function getActiveRound(): Promise<ActiveRound | null> {
  const raw = await AsyncStorage.getItem(KEYS.ACTIVE_ROUND);
  return raw ? (JSON.parse(raw) as ActiveRound) : null;
}

export async function clearActiveRound(): Promise<void> {
  await AsyncStorage.removeItem(KEYS.ACTIVE_ROUND);
}

export async function enqueueOfflineHole(payload: OfflineHolePayload): Promise<void> {
  const queue = await getOfflineQueue();
  queue.push(payload);
  await AsyncStorage.setItem(KEYS.OFFLINE_QUEUE, JSON.stringify(queue));
}

export async function getOfflineQueue(): Promise<OfflineHolePayload[]> {
  const raw = await AsyncStorage.getItem(KEYS.OFFLINE_QUEUE);
  return raw ? (JSON.parse(raw) as OfflineHolePayload[]) : [];
}

export async function removeFromQueue(index: number): Promise<void> {
  const queue = await getOfflineQueue();
  queue.splice(index, 1);
  await AsyncStorage.setItem(KEYS.OFFLINE_QUEUE, JSON.stringify(queue));
}

export async function getTheme(): Promise<'light' | 'dark' | 'system' | null> {
  const val = await AsyncStorage.getItem(KEYS.THEME);
  return val as 'light' | 'dark' | 'system' | null;
}

export async function setTheme(theme: 'light' | 'dark' | 'system'): Promise<void> {
  await AsyncStorage.setItem(KEYS.THEME, theme);
}
```

- [ ] **Step 5: Run to confirm tests pass**

```bash
npx jest __tests__/lib/storage.test.ts
```
Expected: 5 tests PASS

- [ ] **Step 6: Commit**

```bash
git add lib/storage.ts __tests__/lib/storage.test.ts __mocks__/
git commit -m "feat: add AsyncStorage helpers with offline queue"
```

---

## Task 6: TanStack Query Hooks

**Files:**
- Create: `ui/lib/queries.ts`
- Create: `ui/lib/queryClient.ts`

No unit tests for query hooks — integration-level behavior is covered by the screens.

- [ ] **Step 1: Create query client**

```ts
// ui/lib/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 30_000 },
  },
});
```

- [ ] **Step 2: Create query hooks**

```ts
// ui/lib/queries.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiFetch } from './api';
import { getToken } from './auth';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function token(): Promise<string> {
  const t = await getToken();
  if (!t) throw new Error('Not authenticated');
  return t;
}

// ---------------------------------------------------------------------------
// Courses — staleTime Infinity: course data rarely changes during a session
// ---------------------------------------------------------------------------

export function useCourses() {
  return useQuery({
    queryKey: ['courses'],
    queryFn: async () => {
      // Courses endpoint is public — no auth needed
      return apiFetch<CourseResponse[]>('GET', '/api/v1/courses/', null);
    },
    staleTime: Infinity,
  });
}

export function useTeeBoxDetail(teeBoxId: string | null) {
  return useQuery({
    queryKey: ['teeBox', teeBoxId],
    queryFn: async () => {
      const t = await token();
      return apiFetch<TeeBoxDetailResponse>('GET', `/api/v1/courses/tee-boxes/${teeBoxId}`, t);
    },
    enabled: !!teeBoxId,
    staleTime: Infinity,
  });
}

// ---------------------------------------------------------------------------
// Rounds
// ---------------------------------------------------------------------------

export function useRounds(playerId: string | null) {
  return useQuery({
    queryKey: ['rounds', playerId],
    queryFn: async () => {
      const t = await token();
      return apiFetch<RoundResponse[]>('GET', `/api/v1/rounds/?player_id=${playerId}`, t);
    },
    enabled: !!playerId,
  });
}

export function useRoundDetail(roundId: string | null) {
  return useQuery({
    queryKey: ['round', roundId],
    queryFn: async () => {
      const t = await token();
      return apiFetch<RoundWithHolesResponse>('GET', `/api/v1/rounds/${roundId}`, t);
    },
    enabled: !!roundId,
  });
}

export function useRoundStats(roundId: string | null) {
  return useQuery({
    queryKey: ['roundStats', roundId],
    queryFn: async () => {
      const t = await token();
      return apiFetch<RoundStatsResponse>('GET', `/api/v1/rounds/${roundId}/stats`, t);
    },
    enabled: !!roundId,
  });
}

// ---------------------------------------------------------------------------
// Players
// ---------------------------------------------------------------------------

export function useCurrentPlayer() {
  return useQuery({
    queryKey: ['me'],
    queryFn: async () => {
      const t = await token();
      return apiFetch<PlayerResponse>('GET', '/api/v1/auth/me', t);
    },
  });
}

export function usePlayers() {
  return useQuery({
    queryKey: ['players'],
    queryFn: async () => {
      const t = await token();
      return apiFetch<PlayerResponse[]>('GET', '/api/v1/players/', t);
    },
  });
}

// ---------------------------------------------------------------------------
// Mutations
// ---------------------------------------------------------------------------

export function useStartRound() {
  return useMutation({
    mutationFn: async (payload: {
      course_id: string;
      tee_box_id: string;
      holes: number;
    }) => {
      const t = await token();
      return apiFetch<RoundResponse>('POST', '/api/v1/rounds/', t, { body: payload });
    },
  });
}

export function useScoreHole() {
  return useMutation({
    mutationFn: async (payload: {
      round_id: string;
      tee_box_hole_id: string;
      score: number;
      gir: boolean;
      putts: number;
      fairway?: string;
      penalties?: number;
    }) => {
      const t = await token();
      return apiFetch('POST', '/api/v1/rounds/holes', t, { body: payload });
    },
  });
}

export function useFinishRound() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ roundId }: { roundId: string }) => {
      const t = await token();
      return apiFetch('PATCH', `/api/v1/rounds/${roundId}`, t, {
        body: { end_time: new Date().toISOString() },
      });
    },
    onSuccess: (_, { roundId }) => {
      qc.invalidateQueries({ queryKey: ['rounds'] });
      qc.invalidateQueries({ queryKey: ['round', roundId] });
    },
  });
}

export function useUpdatePlayer() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({
      playerId,
      data,
    }: {
      playerId: string;
      data: { name?: string; handicap?: number };
    }) => {
      const t = await token();
      return apiFetch('PATCH', `/api/v1/players/${playerId}`, t, { body: data });
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['me'] }),
  });
}

// ---------------------------------------------------------------------------
// Type stubs — replace with generated types if available
// ---------------------------------------------------------------------------

export type CourseResponse = {
  id: string;
  name: string;
  city: string;
  state: string;
  tees: TeeBoxBase[];
};

export type TeeBoxBase = {
  tee_id: string;
  name: string;
  rating: number;
  slope: number;
  yardage: number;
};

export type TeeBoxDetailResponse = {
  id: string;
  name: string;
  rating: number;
  slope: number;
  yardage: number;
  holes: TeeBoxHoleResponse[];
};

export type TeeBoxHoleResponse = {
  id: string;
  number: number;
  par: number;
  yards: number;
  handicap: number;
};

export type RoundResponse = {
  id: string;
  course_id: string;
  tee_box_id: string;
  player_id: string;
  total_score: number | null;
  holes: number;
  start_time: string;
  end_time: string | null;
};

export type RoundWithHolesResponse = RoundResponse & {
  round_holes: RoundHoleResponse[];
};

export type RoundHoleResponse = {
  id: string;
  tee_box_hole_id: string;
  score: number;
  gir: boolean;
  fairway: string | null;
  putts: number;
  penalties: number;
};

export type RoundStatsResponse = {
  total_score: number;
  par: number;
  to_par: number;
  greens_in_regulation: number;
  gir_percentage: number;
  fairways_hit: number;
  fairways_percentage: number;
  total_putts: number;
  avg_putts_per_hole: number;
  penalties: number;
};

export type PlayerResponse = {
  id: string;
  name: string;
  email: string;
  handicap: number | null;
  zip: string;
};
```

- [ ] **Step 3: Commit**

```bash
git add lib/queries.ts lib/queryClient.ts
git commit -m "feat: add TanStack Query hooks for all API endpoints"
```

---

## Task 7: Root Layout and Auth Guard

**Files:**
- Modify: `ui/app/_layout.tsx`
- Create: `ui/app/(auth)/_layout.tsx`

- [ ] **Step 1: Implement root layout**

```tsx
// ui/app/_layout.tsx
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
    });

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
      setReady(true);
    })();
  }, [segments]);

  if (!ready) return null;

  return (
    <QueryClientProvider client={queryClient}>
      <Stack screenOptions={{ headerShown: false }} />
    </QueryClientProvider>
  );
}
```

- [ ] **Step 2: Create auth stack layout**

```tsx
// ui/app/(auth)/_layout.tsx
import { Stack } from 'expo-router';

export default function AuthLayout() {
  return <Stack screenOptions={{ headerShown: false }} />;
}
```

- [ ] **Step 3: Commit**

```bash
git add app/_layout.tsx app/'(auth)'/_layout.tsx
git commit -m "feat: root layout with auth guard and QueryClient provider"
```

---

## Task 8: Login Screen

**Files:**
- Create: `ui/app/(auth)/login.tsx`

- [ ] **Step 1: Implement login screen**

```tsx
// ui/app/(auth)/login.tsx
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
```

- [ ] **Step 2: Commit**

```bash
git add app/'(auth)'/login.tsx
git commit -m "feat: login screen"
```

---

## Task 9: Signup Screen

**Files:**
- Create: `ui/app/(auth)/signup.tsx`

- [ ] **Step 1: Implement signup screen**

```tsx
// ui/app/(auth)/signup.tsx
import React, { useState } from 'react';
import { View, Text, TextInput, Pressable, Alert, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
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
```

- [ ] **Step 2: Commit**

```bash
git add app/'(auth)'/signup.tsx
git commit -m "feat: signup screen"
```

---

## Task 10: Tab Bar Layout

**Files:**
- Create: `ui/app/(tabs)/_layout.tsx`

- [ ] **Step 1: Implement tab layout**

```tsx
// ui/app/(tabs)/_layout.tsx
import React from 'react';
import { Tabs } from 'expo-router';
import { Text } from 'react-native';

function TabIcon({ emoji, focused }: { emoji: string; focused: boolean }) {
  return <Text style={{ fontSize: 20, opacity: focused ? 1 : 0.5 }}>{emoji}</Text>;
}

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: '#ffffff',
          borderTopColor: '#e5e5e5',
        },
        tabBarActiveTintColor: '#111',
        tabBarInactiveTintColor: '#888',
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Play',
          tabBarIcon: ({ focused }) => <TabIcon emoji="⛳" focused={focused} />,
        }}
      />
      <Tabs.Screen
        name="rounds"
        options={{
          title: 'Rounds',
          tabBarIcon: ({ focused }) => <TabIcon emoji="📋" focused={focused} />,
        }}
      />
      <Tabs.Screen
        name="friends"
        options={{
          title: 'Friends',
          tabBarIcon: ({ focused }) => <TabIcon emoji="👥" focused={focused} />,
        }}
      />
      <Tabs.Screen name="profile" options={{ href: null }} />
      <Tabs.Screen name="rounds/[id]" options={{ href: null }} />
    </Tabs>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add app/'(tabs)'/_layout.tsx
git commit -m "feat: tab bar layout (Play, Rounds, Friends)"
```

---

## Task 11: Scorecard Components

**Files:**
- Create: `ui/components/scorecard/ScoreStepper.tsx`
- Create: `ui/components/scorecard/PuttsStepper.tsx`
- Create: `ui/components/scorecard/StatToggle.tsx`
- Create: `ui/components/scorecard/HoleProgress.tsx`
- Create: `ui/components/scorecard/HoleCard.tsx`
- Create: `ui/__tests__/components/scorecard/ScoreStepper.test.tsx`
- Create: `ui/__tests__/components/scorecard/StatToggle.test.tsx`
- Create: `ui/__tests__/components/scorecard/HoleProgress.test.tsx`

### ScoreStepper

- [ ] **Step 1: Write failing ScoreStepper test**

```tsx
// ui/__tests__/components/scorecard/ScoreStepper.test.tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { ScoreStepper } from '../../../components/scorecard/ScoreStepper';

describe('ScoreStepper', () => {
  it('displays the current score', () => {
    const { getByText } = render(
      <ScoreStepper value={4} par={4} onChange={() => {}} />
    );
    expect(getByText('4')).toBeTruthy();
  });

  it('increments on + press', () => {
    const onChange = jest.fn();
    const { getByText } = render(<ScoreStepper value={4} par={4} onChange={onChange} />);
    fireEvent.press(getByText('+'));
    expect(onChange).toHaveBeenCalledWith(5);
  });

  it('decrements on − press', () => {
    const onChange = jest.fn();
    const { getByText } = render(<ScoreStepper value={4} par={4} onChange={onChange} />);
    fireEvent.press(getByText('−'));
    expect(onChange).toHaveBeenCalledWith(3);
  });

  it('does not go below 1', () => {
    const onChange = jest.fn();
    const { getByText } = render(<ScoreStepper value={1} par={4} onChange={onChange} />);
    fireEvent.press(getByText('−'));
    expect(onChange).not.toHaveBeenCalled();
  });

  it('shows PAR label when score equals par', () => {
    const { getByText } = render(<ScoreStepper value={4} par={4} onChange={() => {}} />);
    expect(getByText('PAR')).toBeTruthy();
  });

  it('shows BIRDIE label when score is par - 1', () => {
    const { getByText } = render(<ScoreStepper value={3} par={4} onChange={() => {}} />);
    expect(getByText('BIRDIE')).toBeTruthy();
  });
});
```

- [ ] **Step 2: Implement ScoreStepper**

```tsx
// ui/components/scorecard/ScoreStepper.tsx
import React from 'react';
import { View, Text, Pressable } from 'react-native';

const PAR_LABELS: Record<number, string> = {
  [-3]: 'ALBATROSS',
  [-2]: 'EAGLE',
  [-1]: 'BIRDIE',
  [0]: 'PAR',
  [1]: 'BOGEY',
  [2]: 'DOUBLE',
};

function getLabel(diff: number): string {
  if (diff in PAR_LABELS) return PAR_LABELS[diff];
  return `+${diff}`;
}

type Props = { value: number; par: number; onChange: (v: number) => void };

export function ScoreStepper({ value, par, onChange }: Props) {
  const diff = value - par;
  const borderColor = diff < 0 ? '#43a047' : diff > 0 ? '#e53935' : '#e5e5e5';
  const label = getLabel(diff);

  return (
    <View className="items-center">
      <View className="flex-row items-center gap-6">
        <Pressable
          onPress={() => value > 1 && onChange(value - 1)}
          hitSlop={12}
          className="w-12 h-12 items-center justify-center"
        >
          <Text className="text-3xl text-[#111] dark:text-white">−</Text>
        </Pressable>

        <View
          className="w-20 h-20 rounded-full items-center justify-center border-2"
          style={{ borderColor }}
        >
          <Text className="text-3xl font-bold text-[#111] dark:text-white">{value}</Text>
        </View>

        <Pressable
          onPress={() => onChange(value + 1)}
          hitSlop={12}
          className="w-12 h-12 items-center justify-center"
        >
          <Text className="text-3xl text-[#111] dark:text-white">+</Text>
        </Pressable>
      </View>

      <Text
        className="mt-2 text-sm font-semibold"
        style={{ color: diff < 0 ? '#43a047' : diff > 0 ? '#e53935' : '#888' }}
      >
        {label}
      </Text>
    </View>
  );
}
```

- [ ] **Step 3: Run ScoreStepper tests**

```bash
npx jest __tests__/components/scorecard/ScoreStepper.test.tsx
```
Expected: 6 PASS

### StatToggle

- [ ] **Step 4: Write failing StatToggle test**

```tsx
// ui/__tests__/components/scorecard/StatToggle.test.tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { StatToggle } from '../../../components/scorecard/StatToggle';

describe('StatToggle', () => {
  const options = ['YES', 'NO'];

  it('renders all options', () => {
    const { getByText } = render(
      <StatToggle options={options} value="YES" onChange={() => {}} />
    );
    expect(getByText('YES')).toBeTruthy();
    expect(getByText('NO')).toBeTruthy();
  });

  it('calls onChange when an option is pressed', () => {
    const onChange = jest.fn();
    const { getByText } = render(
      <StatToggle options={options} value="YES" onChange={onChange} />
    );
    fireEvent.press(getByText('NO'));
    expect(onChange).toHaveBeenCalledWith('NO');
  });
});
```

- [ ] **Step 5: Implement StatToggle**

```tsx
// ui/components/scorecard/StatToggle.tsx
import React from 'react';
import { View, Text, Pressable } from 'react-native';

type Props = { options: string[]; value: string; onChange: (v: string) => void; label?: string };

export function StatToggle({ options, value, onChange, label }: Props) {
  return (
    <View className="items-center">
      {label && <Text className="text-xs font-semibold text-[#888] mb-2 uppercase tracking-wide">{label}</Text>}
      <View className="flex-row rounded-xl overflow-hidden border border-[#e5e5e5] dark:border-[#2a2a2a]">
        {options.map((opt) => (
          <Pressable
            key={opt}
            onPress={() => onChange(opt)}
            className={`px-4 py-2 ${opt === value ? 'bg-[#111] dark:bg-white' : 'bg-white dark:bg-[#1c1c1e]'}`}
          >
            <Text
              className={`text-sm font-semibold ${opt === value ? 'text-white dark:text-[#111]' : 'text-[#111] dark:text-white'}`}
            >
              {opt}
            </Text>
          </Pressable>
        ))}
      </View>
    </View>
  );
}
```

### HoleProgress

- [ ] **Step 6: Write failing HoleProgress test**

```tsx
// ui/__tests__/components/scorecard/HoleProgress.test.tsx
import React from 'react';
import { render } from '@testing-library/react-native';
import { HoleProgress } from '../../../components/scorecard/HoleProgress';

it('renders the correct number of dots', () => {
  const scores = [4, 3]; // 2 scored holes
  const { getAllByTestId } = render(
    <HoleProgress total={9} currentHole={3} scoredHoles={[{ holeNumber: 1, toPar: 0 }, { holeNumber: 2, toPar: -1 }]} />
  );
  // 9 dots total
  expect(getAllByTestId('hole-dot')).toHaveLength(9);
});
```

- [ ] **Step 7: Implement HoleProgress**

```tsx
// ui/components/scorecard/HoleProgress.tsx
import React from 'react';
import { View, ScrollView } from 'react-native';

type ScoredHole = { holeNumber: number; toPar: number };
type Props = { total: number; currentHole: number; scoredHoles: ScoredHole[] };

export function HoleProgress({ total, currentHole, scoredHoles }: Props) {
  const scoredMap = new Map(scoredHoles.map((h) => [h.holeNumber, h.toPar]));

  return (
    <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerClassName="px-4 py-2 gap-1.5 flex-row">
      {Array.from({ length: total }, (_, i) => {
        const holeNum = i + 1;
        const toPar = scoredMap.get(holeNum);
        const isScored = toPar !== undefined;
        const isCurrent = holeNum === currentHole;

        let bg = 'bg-[#e5e5e5] dark:bg-[#2a2a2a]';
        if (isScored) {
          bg = toPar < 0 ? 'bg-[#43a047]' : toPar > 0 ? 'bg-[#e53935]' : 'bg-[#888]';
        }

        return (
          <View
            key={holeNum}
            testID="hole-dot"
            className={`w-3 h-3 rounded-full ${bg} ${isCurrent && !isScored ? 'border-2 border-[#111] dark:border-white' : ''}`}
          />
        );
      })}
    </ScrollView>
  );
}
```

- [ ] **Step 8: Write failing PuttsStepper test**

```tsx
// ui/__tests__/components/scorecard/PuttsStepper.test.tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { PuttsStepper } from '../../../components/scorecard/PuttsStepper';

describe('PuttsStepper', () => {
  it('displays the current putts value', () => {
    const { getByText } = render(<PuttsStepper value={2} onChange={() => {}} />);
    expect(getByText('2')).toBeTruthy();
  });

  it('increments up to 6', () => {
    const onChange = jest.fn();
    const { getAllByText } = render(<PuttsStepper value={2} onChange={onChange} />);
    fireEvent.press(getAllByText('+')[0]);
    expect(onChange).toHaveBeenCalledWith(3);
  });

  it('does not go above 6', () => {
    const onChange = jest.fn();
    const { getAllByText } = render(<PuttsStepper value={6} onChange={onChange} />);
    fireEvent.press(getAllByText('+')[0]);
    expect(onChange).not.toHaveBeenCalled();
  });

  it('does not go below 0', () => {
    const onChange = jest.fn();
    const { getAllByText } = render(<PuttsStepper value={0} onChange={onChange} />);
    fireEvent.press(getAllByText('\u2212')[0]); // Unicode minus U+2212
    expect(onChange).not.toHaveBeenCalled();
  });
});
```

Note: The `−` character in both `PuttsStepper` and `ScoreStepper` implementations is Unicode minus (U+2212, `\u2212`), not a hyphen. Test strings must use the same character — the safest approach is to use `\u2212` in test source or copy the character directly from the component source.

- [ ] **Step 8a: Run to confirm it fails**

```bash
npx jest __tests__/components/scorecard/PuttsStepper.test.tsx
```
Expected: FAIL — module not found

- [ ] **Step 8b: Implement PuttsStepper**

```tsx
// ui/components/scorecard/PuttsStepper.tsx
import React from 'react';
import { View, Text, Pressable } from 'react-native';

type Props = { value: number; onChange: (v: number) => void };

export function PuttsStepper({ value, onChange }: Props) {
  return (
    <View className="items-center">
      <Text className="text-xs font-semibold text-[#888] mb-2 uppercase tracking-wide">Putts</Text>
      <View className="flex-row items-center gap-4">
        <Pressable onPress={() => value > 0 && onChange(value - 1)} hitSlop={12}>
          <Text className="text-2xl text-[#111] dark:text-white">−</Text>
        </Pressable>
        <Text className="text-2xl font-bold text-[#111] dark:text-white w-8 text-center">{value}</Text>
        <Pressable onPress={() => value < 6 && onChange(value + 1)} hitSlop={12}>
          <Text className="text-2xl text-[#111] dark:text-white">+</Text>
        </Pressable>
      </View>
    </View>
  );
}
```

- [ ] **Step 9: Write failing HoleCard test**

```tsx
// ui/__tests__/components/scorecard/HoleCard.test.tsx
import React from 'react';
import { render } from '@testing-library/react-native';
import { HoleCard, HoleCardState } from '../../../components/scorecard/HoleCard';

const baseState: HoleCardState = { score: 4, gir: false, fairway: 'o', putts: 2 };

describe('HoleCard', () => {
  it('displays hole number and par', () => {
    const { getByText } = render(
      <HoleCard holeNumber={5} par={4} yards={420} state={baseState} onChange={() => {}} />
    );
    expect(getByText('Hole 5')).toBeTruthy();
    expect(getByText('Par 4 · 420 yds')).toBeTruthy();
  });

  it('hides fairway toggle on par-3', () => {
    const par3State: HoleCardState = { score: 3, gir: true, fairway: null, putts: 1 };
    const { queryByText } = render(
      <HoleCard holeNumber={3} par={3} yards={155} state={par3State} onChange={() => {}} />
    );
    expect(queryByText('Fairway')).toBeNull();
  });

  it('shows fairway toggle on par-4', () => {
    const { getByText } = render(
      <HoleCard holeNumber={1} par={4} yards={400} state={baseState} onChange={() => {}} />
    );
    expect(getByText('Fairway')).toBeTruthy();
  });
});
```

- [ ] **Step 9a: Run to confirm it fails**

```bash
npx jest __tests__/components/scorecard/HoleCard.test.tsx
```
Expected: FAIL — module not found

- [ ] **Step 9b: Implement HoleCard**

```tsx
// ui/components/scorecard/HoleCard.tsx
import React from 'react';
import { View, Text } from 'react-native';
import { Card } from '../shared/Card';
import { ScoreStepper } from './ScoreStepper';
import { StatToggle } from './StatToggle';
import { PuttsStepper } from './PuttsStepper';

const FAIRWAY_OPTIONS = ['HIT', 'LEFT', 'RIGHT', 'SHORT', 'LONG'];
// Maps display label → API value
const FAIRWAY_API_MAP: Record<string, string> = {
  HIT: 'o', LEFT: '<', RIGHT: '>', SHORT: 'v', LONG: '^',
};

export type HoleCardState = {
  score: number;
  gir: boolean;
  fairway: string | null; // null for par-3
  putts: number;
};

type Props = {
  holeNumber: number;
  par: number;
  yards: number;
  state: HoleCardState;
  onChange: (state: HoleCardState) => void;
};

export function HoleCard({ holeNumber, par, yards, state, onChange }: Props) {
  const isParThree = par === 3;

  return (
    <Card>
      <View className="flex-row justify-between mb-4">
        <Text className="text-lg font-bold text-[#111] dark:text-white">Hole {holeNumber}</Text>
        <Text className="text-[#888]">Par {par} · {yards} yds</Text>
      </View>

      <ScoreStepper
        value={state.score}
        par={par}
        onChange={(score) => onChange({ ...state, score })}
      />

      <View className="mt-6 flex-row justify-around">
        <StatToggle
          label="GIR"
          options={['YES', 'NO']}
          value={state.gir ? 'YES' : 'NO'}
          onChange={(v) => onChange({ ...state, gir: v === 'YES' })}
        />
        {!isParThree && (
          <StatToggle
            label="Fairway"
            options={FAIRWAY_OPTIONS}
            value={
              state.fairway
                ? (Object.entries(FAIRWAY_API_MAP).find(([, api]) => api === state.fairway)?.[0] ?? 'HIT')
                : 'HIT'
            }
            onChange={(v) => onChange({ ...state, fairway: FAIRWAY_API_MAP[v] })}
          />
        )}
        <PuttsStepper
          value={state.putts}
          onChange={(putts) => onChange({ ...state, putts })}
        />
      </View>
    </Card>
  );
}
```

- [ ] **Step 10: Run all scorecard component tests**

```bash
npx jest __tests__/components/scorecard/
```
Expected: ScoreStepper (6), PuttsStepper (4), StatToggle (2), HoleProgress (1), HoleCard (3) — all PASS

- [ ] **Step 11: Commit**

```bash
git add components/scorecard/ __tests__/components/scorecard/
git commit -m "feat: scorecard components (ScoreStepper, PuttsStepper, StatToggle, HoleProgress, HoleCard)"
```

---

## Task 12: Play Tab — Start Round Screen

**Files:**
- Create: `ui/app/(tabs)/index.tsx` (Start Round state only — Live Scorecard added in Task 13)

- [ ] **Step 1: Implement Start Round screen**

```tsx
// ui/app/(tabs)/index.tsx
import React, { useState } from 'react';
import {
  View, Text, ScrollView, TextInput, Pressable, ActivityIndicator, Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useCourses, useTeeBoxDetail, useStartRound, CourseResponse, TeeBoxBase } from '../../lib/queries';
import { saveActiveRound, getActiveRound } from '../../lib/storage';
import { Button } from '../../components/shared/Button';
import { useEffect } from 'react';

export default function PlayTab() {
  const router = useRouter();
  const [activeRound, setActiveRound] = useState<Awaited<ReturnType<typeof getActiveRound>>>(null);
  const [search, setSearch] = useState('');
  const [selectedCourse, setSelectedCourse] = useState<CourseResponse | null>(null);
  const [selectedTeeId, setSelectedTeeId] = useState<string | null>(null);
  const [holes, setHoles] = useState<9 | 18>(18);

  const { data: courses, isLoading: loadingCourses } = useCourses();
  const { data: teeDetail } = useTeeBoxDetail(selectedTeeId);
  const startRound = useStartRound();

  useEffect(() => {
    getActiveRound().then(setActiveRound);
  }, []);

  // If there's an active round, show the scorecard (Task 13 adds this component)
  if (activeRound) {
    return <ActiveScorecard round={activeRound} onClear={() => setActiveRound(null)} />;
  }

  const filtered = (courses ?? []).filter((c) =>
    c.name.toLowerCase().includes(search.toLowerCase())
  );

  async function handleStart() {
    if (!selectedCourse || !selectedTeeId || !teeDetail) return;
    try {
      const round = await startRound.mutateAsync({
        course_id: selectedCourse.id,
        tee_box_id: selectedTeeId,
        holes,
      });
      const active = {
        round_id: round.id,
        course_id: selectedCourse.id,
        tee_box_id: selectedTeeId,
        tee_box_holes: teeDetail.holes.map((h) => ({
          id: h.id,
          number: h.number,
          par: h.par,
          yards: h.yards,
        })),
        holes_total: holes,
        scored_holes: [],
      };
      await saveActiveRound(active);
      setActiveRound(active);
    } catch {
      Alert.alert('Error', 'Could not start round. Try again.');
    }
  }

  return (
    <ScrollView className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      <View className="px-4 pt-12 pb-6">
        <Text className="text-2xl font-bold text-[#111] dark:text-white mb-6">Start Round</Text>

        {/* Course search */}
        <Text className="text-xs font-semibold text-[#888] uppercase tracking-wide mb-2">Course</Text>
        <TextInput
          className="bg-white dark:bg-[#1c1c1e] rounded-xl px-4 py-3 text-base text-[#111] dark:text-white mb-2 border border-[#e5e5e5] dark:border-[#2a2a2a]"
          placeholder="Search courses..."
          placeholderTextColor="#888"
          value={search}
          onChangeText={setSearch}
        />

        {loadingCourses && <ActivityIndicator className="my-4" />}
        {!loadingCourses && filtered.length === 0 && (
          <Text className="text-[#888] text-center my-4">No courses available. Add via the API.</Text>
        )}
        {filtered.map((course) => (
          <Pressable
            key={course.id}
            onPress={() => { setSelectedCourse(course); setSelectedTeeId(null); setSearch(course.name); }}
            className={`rounded-xl px-4 py-3 mb-1 ${selectedCourse?.id === course.id ? 'bg-[#111] dark:bg-white' : 'bg-white dark:bg-[#1c1c1e]'} border border-[#e5e5e5] dark:border-[#2a2a2a]`}
          >
            <Text className={selectedCourse?.id === course.id ? 'text-white dark:text-[#111] font-semibold' : 'text-[#111] dark:text-white'}>
              {course.name}
            </Text>
            <Text className="text-[#888] text-sm">{course.city}, {course.state}</Text>
          </Pressable>
        ))}

        {/* Tee box selector */}
        {selectedCourse && (
          <>
            <Text className="text-xs font-semibold text-[#888] uppercase tracking-wide mt-6 mb-2">Tees</Text>
            <View className="flex-row flex-wrap gap-2">
              {selectedCourse.tees.map((tee: TeeBoxBase) => (
                <Pressable
                  key={tee.tee_id}
                  onPress={() => setSelectedTeeId(tee.tee_id)}
                  className={`px-4 py-2 rounded-full border ${selectedTeeId === tee.tee_id ? 'bg-[#111] dark:bg-white border-[#111] dark:border-white' : 'bg-white dark:bg-[#1c1c1e] border-[#e5e5e5] dark:border-[#2a2a2a]'}`}
                >
                  <Text className={selectedTeeId === tee.tee_id ? 'text-white dark:text-[#111] font-semibold' : 'text-[#111] dark:text-white'}>
                    {tee.name}
                  </Text>
                </Pressable>
              ))}
            </View>
          </>
        )}

        {/* Holes selector */}
        <Text className="text-xs font-semibold text-[#888] uppercase tracking-wide mt-6 mb-2">Holes</Text>
        <View className="flex-row gap-2">
          {([9, 18] as const).map((n) => (
            <Pressable
              key={n}
              onPress={() => setHoles(n)}
              className={`px-6 py-2 rounded-full border ${holes === n ? 'bg-[#111] dark:bg-white border-[#111] dark:border-white' : 'bg-white dark:bg-[#1c1c1e] border-[#e5e5e5] dark:border-[#2a2a2a]'}`}
            >
              <Text className={holes === n ? 'text-white dark:text-[#111] font-semibold' : 'text-[#111] dark:text-white'}>{n}</Text>
            </Pressable>
          ))}
        </View>

        <View className="mt-8">
          <Button
            label="Start Round"
            onPress={handleStart}
            loading={startRound.isPending}
            disabled={!selectedCourse || !selectedTeeId}
          />
        </View>
      </View>
    </ScrollView>
  );
}

// Placeholder — replaced in Task 13
function ActiveScorecard({ round, onClear }: { round: NonNullable<Awaited<ReturnType<typeof getActiveRound>>>; onClear: () => void }) {
  return (
    <View className="flex-1 items-center justify-center bg-[#f5f5f5] dark:bg-[#111]">
      <Text className="text-[#111] dark:text-white">Round in progress...</Text>
      <Pressable onPress={onClear} className="mt-4">
        <Text className="text-[#e53935]">Abandon Round</Text>
      </Pressable>
    </View>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add app/'(tabs)'/index.tsx
git commit -m "feat: Play tab — Start Round screen"
```

---

## Task 13: Live Scorecard

**Files:**
- Create: `ui/components/scorecard/LiveScorecard.tsx`
- Modify: `ui/app/(tabs)/index.tsx` (replace placeholder `ActiveScorecard`)

- [ ] **Step 1: Implement LiveScorecard component**

```tsx
// ui/components/scorecard/LiveScorecard.tsx
import React, { useState } from 'react';
import { View, Text, ScrollView, Pressable, Modal } from 'react-native';
import { HoleCard, HoleCardState } from './HoleCard';
import { HoleProgress } from './HoleProgress';
import { ScoreLabel } from '../shared/ScoreLabel';
import { Button } from '../shared/Button';
import { ActiveRound, ScoredHoleEntry, saveActiveRound, clearActiveRound, enqueueOfflineHole } from '../../lib/storage';
import { useScoreHole, useFinishRound } from '../../lib/queries';

type Props = {
  round: ActiveRound;
  onRoundUpdate: (updated: ActiveRound) => void;
  onFinish: (roundId: string) => void;
  onAbandon: () => void;
};

export function LiveScorecard({ round, onRoundUpdate, onFinish, onAbandon }: Props) {
  const scoreHole = useScoreHole();
  const finishRound = useFinishRound();

  const currentIndex = round.scored_holes.length;
  const currentHoleStub = round.tee_box_holes[currentIndex];
  const isLastHole = currentIndex === round.holes_total - 1;
  const [showAbandon, setShowAbandon] = useState(false);

  const [cardState, setCardState] = useState<HoleCardState>({
    score: currentHoleStub?.par ?? 4,
    gir: false,
    fairway: currentHoleStub?.par !== 3 ? 'o' : null,
    putts: 2,
  });

  if (!currentHoleStub) return null;

  // scored_holes carries {holeNumber, toPar} — used for progress dot colouring
  const runningToPar = round.scored_holes.reduce((sum, h) => sum + h.toPar, 0);

  async function submitHole() {
    const toPar = cardState.score - currentHoleStub.par;
    const payload = {
      round_id: round.round_id,
      tee_box_hole_id: currentHoleStub.id,
      score: cardState.score,
      gir: cardState.gir,
      putts: cardState.putts,
      ...(cardState.fairway !== null ? { fairway: cardState.fairway } : {}),
    };

    const entry: ScoredHoleEntry = { holeNumber: currentHoleStub.number, toPar };
    const updated: ActiveRound = {
      ...round,
      scored_holes: [...round.scored_holes, entry],
    };

    // Always record locally first — then notify parent (no prop mutation)
    await saveActiveRound(updated);
    onRoundUpdate(updated);

    // Try to submit; queue on failure (non-blocking)
    try {
      await scoreHole.mutateAsync(payload);
    } catch {
      await enqueueOfflineHole(payload);
    }

    if (isLastHole) {
      // Finish the round — send only end_time (total_score is auto-computed by API)
      try {
        await finishRound.mutateAsync({ roundId: round.round_id });
      } catch {
        // v1 known gap: PATCH not queued offline — round remains open in backend
        // until next session or manual close
      }
      await clearActiveRound();
      onFinish(round.round_id);
    } else {
      const nextHoleStub = round.tee_box_holes[currentIndex + 1];
      setCardState({
        score: nextHoleStub.par,
        gir: false,
        fairway: nextHoleStub.par !== 3 ? 'o' : null,
        putts: 2,
      });
    }
  }

  return (
    <ScrollView className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      {/* Header */}
      <View className="px-4 pt-12 pb-2 flex-row items-center justify-between">
        <View>
          <Text className="text-lg font-bold text-[#111] dark:text-white">Round</Text>
          <Text className="text-[#888] text-sm">Thru {round.scored_holes.length}</Text>
        </View>
        <View className="flex-row items-center gap-3">
          <ScoreLabel toPar={runningToPar} size="lg" />
          <Pressable onPress={() => setShowAbandon(true)} hitSlop={8}>
            <Text className="text-[#888] text-xl">···</Text>
          </Pressable>
        </View>
      </View>

      {/* Hole progress dots — scored_holes carries toPar for colouring */}
      <HoleProgress
        total={round.holes_total}
        currentHole={currentHoleStub.number}
        scoredHoles={round.scored_holes}
      />

      {/* Current hole card */}
      <View className="px-4 py-4">
        <HoleCard
          holeNumber={currentHoleStub.number}
          par={currentHoleStub.par}
          yards={currentHoleStub.yards}
          state={cardState}
          onChange={setCardState}
        />
      </View>

      {/* Next / Finish button */}
      <View className="px-4 pb-8">
        <Button
          label={isLastHole ? 'Finish Round' : 'Next Hole →'}
          onPress={submitHole}
          loading={scoreHole.isPending || finishRound.isPending}
        />
      </View>

      {/* Abandon confirmation */}
      <Modal visible={showAbandon} transparent animationType="fade">
        <View className="flex-1 bg-black/50 items-center justify-center px-6">
          <View className="bg-white dark:bg-[#1c1c1e] rounded-2xl p-6 w-full">
            <Text className="text-lg font-bold text-[#111] dark:text-white mb-2">Abandon round?</Text>
            <Text className="text-[#888] mb-6">The round will remain incomplete in the backend.</Text>
            <Button label="Yes, abandon" onPress={async () => { await clearActiveRound(); setShowAbandon(false); onAbandon(); }} />
            <Pressable className="mt-3 items-center" onPress={() => setShowAbandon(false)}>
              <Text className="text-[#888]">Cancel</Text>
            </Pressable>
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
}
```

- [ ] **Step 2: Wire LiveScorecard into the Play tab**

Replace the `ActiveScorecard` placeholder in `ui/app/(tabs)/index.tsx`:

```tsx
// Replace the placeholder ActiveScorecard function and its usage
// At the top, add:
import { LiveScorecard } from '../../components/scorecard/LiveScorecard';

// Replace the if (activeRound) block:
if (activeRound) {
  return (
    <LiveScorecard
      round={activeRound}
      onRoundUpdate={(updated) => setActiveRound(updated)}
      onFinish={(roundId) => {
        setActiveRound(null);
        router.push(`/rounds/${roundId}`);
      }}
      onAbandon={() => setActiveRound(null)}
    />
  );
}
```

And remove the placeholder `ActiveScorecard` function at the bottom of the file.

- [ ] **Step 3: Commit**

```bash
git add components/scorecard/LiveScorecard.tsx app/'(tabs)'/index.tsx
git commit -m "feat: Live Scorecard with hole-by-hole scoring and abandon flow"
```

---

## Task 14: Offline Queue Processor

**Files:**
- Create: `ui/lib/offlineQueue.ts`
- Modify: `ui/app/_layout.tsx` (mount queue processor on reconnect)

- [ ] **Step 1: Implement offline queue processor**

```ts
// ui/lib/offlineQueue.ts
import NetInfo from '@react-native-community/netinfo';
import { getOfflineQueue, removeFromQueue } from './storage';
import { apiFetch } from './api';
import { getToken } from './auth';

export function startOfflineQueueProcessor(): () => void {
  const unsubscribe = NetInfo.addEventListener(async (state) => {
    if (!state.isConnected) return;

    const queue = await getOfflineQueue();
    if (queue.length === 0) return;

    const token = await getToken();
    if (!token) return;

    // Process in order, stop on first failure
    for (let i = 0; i < queue.length; i++) {
      const item = queue[i];
      try {
        await apiFetch('POST', '/api/v1/rounds/holes', token, { body: item as unknown as Record<string, unknown> });
        await removeFromQueue(0); // always remove index 0 since we process in order
      } catch {
        break; // Still offline or server error — try again next reconnect
      }
    }
  });

  return unsubscribe;
}
```

- [ ] **Step 2: Mount in root layout**

In `ui/app/_layout.tsx`, add inside the component:

```tsx
import { startOfflineQueueProcessor } from '../lib/offlineQueue';

useEffect(() => {
  const unsub = startOfflineQueueProcessor();
  return unsub;
}, []);
```

- [ ] **Step 3: Commit**

```bash
git add lib/offlineQueue.ts app/_layout.tsx
git commit -m "feat: offline queue processor — flushes on reconnect"
```

---

## Task 15: Round Summary Screen

**Files:**
- Create: `ui/app/(tabs)/rounds/[id].tsx`
- Create: `ui/components/rounds/StatsGrid.tsx`

- [ ] **Step 1: Implement StatsGrid**

```tsx
// ui/components/rounds/StatsGrid.tsx
import React from 'react';
import { View, Text } from 'react-native';
import { ScoreLabel } from '../shared/ScoreLabel';
import type { RoundStatsResponse } from '../../lib/queries';

type Props = { stats: RoundStatsResponse };

export function StatsGrid({ stats }: Props) {
  const items = [
    { label: 'Score', value: `${stats.total_score}` },
    { label: 'To Par', node: <ScoreLabel toPar={stats.to_par} size="md" /> },
    { label: 'GIR', value: `${stats.gir_percentage.toFixed(0)}%` },
    { label: 'FIR', value: `${stats.fairways_percentage.toFixed(0)}%` },
    { label: 'Putts', value: `${stats.avg_putts_per_hole.toFixed(1)}/hole` },
    { label: 'Penalties', value: `${stats.penalties}` },
  ];

  return (
    <View className="flex-row flex-wrap">
      {items.map(({ label, value, node }) => (
        <View key={label} className="w-1/3 items-center py-3">
          <Text className="text-xs text-[#888] uppercase tracking-wide mb-1">{label}</Text>
          {node ?? <Text className="text-lg font-bold text-[#111] dark:text-white">{value}</Text>}
        </View>
      ))}
    </View>
  );
}
```

- [ ] **Step 2: Implement Round Summary screen**

```tsx
// ui/app/(tabs)/rounds/[id].tsx
import React from 'react';
import {
  View, Text, ScrollView, Pressable, ActivityIndicator,
} from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useRoundDetail, useRoundStats, useTeeBoxDetail } from '../../../lib/queries';
import { StatsGrid } from '../../../components/rounds/StatsGrid';
import { Card } from '../../../components/shared/Card';
import { ScoreLabel } from '../../../components/shared/ScoreLabel';

export default function RoundSummaryScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { data: round, isLoading: loadingRound, isError: errorRound, refetch } = useRoundDetail(id);
  const { data: stats, isLoading: loadingStats, isError: errorStats } = useRoundStats(id);
  // Fetch tee box detail to resolve hole numbers and par from tee_box_hole_id
  const { data: teeBox } = useTeeBoxDetail(round?.tee_box_id ?? null);
  const holeMap = new Map(teeBox?.holes.map((h) => [h.id, h]) ?? []);

  if (loadingRound || loadingStats) {
    return (
      <View className="flex-1 items-center justify-center bg-[#f5f5f5] dark:bg-[#111]">
        <ActivityIndicator />
      </View>
    );
  }

  if (errorRound || errorStats) {
    return (
      <View className="flex-1 items-center justify-center bg-[#f5f5f5] dark:bg-[#111] px-6">
        <Text className="text-[#111] dark:text-white mb-4">Could not load round stats.</Text>
        <Pressable onPress={() => refetch()} className="px-6 py-3 bg-[#111] dark:bg-white rounded-xl">
          <Text className="text-white dark:text-[#111] font-semibold">Retry</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      <View className="px-4 pt-12 pb-6">
        <Text className="text-2xl font-bold text-[#111] dark:text-white mb-2">Round Summary</Text>

        {/* Stats */}
        {stats && (
          <Card className="mb-4">
            <StatsGrid stats={stats} />
          </Card>
        )}

        {/* Hole grid */}
        <Card>
          {/* Header row */}
          <View className="flex-row border-b border-[#e5e5e5] dark:border-[#2a2a2a] pb-2 mb-2">
            {['Hole', 'Par', 'Score', '+/-'].map((h) => (
              <Text key={h} className="flex-1 text-center text-xs font-semibold text-[#888] uppercase">
                {h}
              </Text>
            ))}
          </View>
          {(round?.round_holes ?? [])
            .slice()
            .sort((a, b) => (holeMap.get(a.tee_box_hole_id)?.number ?? 0) - (holeMap.get(b.tee_box_hole_id)?.number ?? 0))
            .map((hole) => {
              const stub = holeMap.get(hole.tee_box_hole_id);
              const par = stub?.par ?? 4;
              const holeNumber = stub?.number ?? '?';
              const toPar = hole.score - par;
              return (
                <View key={hole.id} className="flex-row py-2 border-b border-[#e5e5e5] dark:border-[#2a2a2a]">
                  <Text className="flex-1 text-center text-[#111] dark:text-white">{holeNumber}</Text>
                  <Text className="flex-1 text-center text-[#888]">{par}</Text>
                  <Text className="flex-1 text-center font-bold text-[#111] dark:text-white">{hole.score}</Text>
                  <View className="flex-1 items-center">
                    <ScoreLabel toPar={toPar} size="sm" />
                  </View>
                </View>
              );
            })}
        </Card>

        <Pressable
          className="mt-6 items-center py-4"
          onPress={() => router.replace('/rounds')}
        >
          <Text className="font-semibold text-[#111] dark:text-white">Done</Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add app/'(tabs)'/rounds/ components/rounds/StatsGrid.tsx
git commit -m "feat: Round Summary screen with stats grid and hole grid"
```

---

## Task 16: Rounds History Tab

**Files:**
- Create: `ui/app/(tabs)/rounds.tsx`
- Create: `ui/components/rounds/RoundCard.tsx`

- [ ] **Step 1: Implement RoundCard**

```tsx
// ui/components/rounds/RoundCard.tsx
import React from 'react';
import { View, Text, Pressable } from 'react-native';
import { Card } from '../shared/Card';
import { ScoreLabel } from '../shared/ScoreLabel';
import type { RoundResponse, CourseResponse } from '../../lib/queries';

type Props = {
  round: RoundResponse;
  courses: CourseResponse[];
  onPress: () => void;
};

export function RoundCard({ round, courses, onPress }: Props) {
  const course = courses.find((c) => c.id === round.course_id);
  const tee = course?.tees.find((t) => t.tee_id === round.tee_box_id);
  const date = new Date(round.start_time).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  });
  const toPar = round.total_score !== null && course
    ? null // we don't have par from course list; show score only
    : null;

  return (
    <Pressable onPress={onPress}>
      <Card className="mb-3">
        <View className="flex-row justify-between items-start">
          <View className="flex-1">
            <Text className="font-bold text-base text-[#111] dark:text-white">
              {course?.name ?? 'Unknown Course'}
            </Text>
            <Text className="text-[#888] text-sm mt-0.5">
              {date} · {tee?.name ?? '—'} · {round.holes} holes
            </Text>
          </View>
          <View className="items-end">
            <Text className="text-2xl font-bold text-[#111] dark:text-white">
              {round.total_score ?? '—'}
            </Text>
          </View>
        </View>
      </Card>
    </Pressable>
  );
}
```

- [ ] **Step 2: Implement Rounds history tab**

```tsx
// ui/app/(tabs)/rounds.tsx
import React from 'react';
import { View, Text, FlatList, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { useRounds, useCourses, useCurrentPlayer } from '../../lib/queries';
import { RoundCard } from '../../components/rounds/RoundCard';

export default function RoundsTab() {
  const router = useRouter();
  const { data: me } = useCurrentPlayer();
  const { data: rounds, isLoading } = useRounds(me?.id ?? null);
  const { data: courses } = useCourses();

  if (isLoading) {
    return (
      <View className="flex-1 items-center justify-center bg-[#f5f5f5] dark:bg-[#111]">
        <ActivityIndicator />
      </View>
    );
  }

  const sorted = (rounds ?? []).slice().sort(
    (a, b) => new Date(b.start_time).getTime() - new Date(a.start_time).getTime()
  );

  return (
    <View className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      <View className="px-4 pt-12 pb-4">
        <Text className="text-2xl font-bold text-[#111] dark:text-white">Rounds</Text>
      </View>
      <FlatList
        data={sorted}
        keyExtractor={(r) => r.id}
        contentContainerClassName="px-4 pb-8"
        ListEmptyComponent={
          <Text className="text-[#888] text-center mt-12">
            No rounds yet. Head to the Play tab to start your first round.
          </Text>
        }
        renderItem={({ item }) => (
          <RoundCard
            round={item}
            courses={courses ?? []}
            onPress={() => router.push(`/rounds/${item.id}`)}
          />
        )}
      />
    </View>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add app/'(tabs)'/rounds.tsx components/rounds/RoundCard.tsx
git commit -m "feat: Rounds history tab with RoundCard list"
```

---

## Task 17: Friends Leaderboard Tab

**Files:**
- Create: `ui/app/(tabs)/friends.tsx`

- [ ] **Step 1: Implement Friends leaderboard**

```tsx
// ui/app/(tabs)/friends.tsx
import React from 'react';
import { View, Text, FlatList, ActivityIndicator, Pressable } from 'react-native';
import { useRouter } from 'expo-router';
import { useQueries, useQuery } from '@tanstack/react-query';
import { usePlayers, useCurrentPlayer, RoundResponse, PlayerResponse } from '../../lib/queries';
import { Avatar } from '../../components/shared/Avatar';
import { ScoreLabel } from '../../components/shared/ScoreLabel';
import { apiFetch } from '../../lib/api';
import { getToken } from '../../lib/auth';

type LeaderboardRow = {
  player: PlayerResponse;
  roundCount: number;
  avgScore: number | null;
  avgToPar: number | null;
};

export default function FriendsTab() {
  const router = useRouter();
  const { data: players, isLoading: loadingPlayers } = usePlayers();
  const { data: me } = useCurrentPlayer();

  // Fetch rounds for each player in parallel
  const roundQueries = useQueries({
    queries: (players ?? []).map((player) => ({
      queryKey: ['rounds', player.id],
      queryFn: async () => {
        const token = await getToken();
        return apiFetch<RoundResponse[]>('GET', `/api/v1/rounds/?player_id=${player.id}`, token);
      },
      enabled: !!players,
    })),
  });

  if (loadingPlayers) {
    return (
      <View className="flex-1 items-center justify-center bg-[#f5f5f5] dark:bg-[#111]">
        <ActivityIndicator />
      </View>
    );
  }

  // Build leaderboard — skip players whose rounds failed to load
  const rows: LeaderboardRow[] = (players ?? [])
    .map((player, i) => {
      const result = roundQueries[i];
      if (!result.data) return null; // skip failed / loading
      const last5 = result.data
        .filter((r) => r.total_score !== null)
        .sort((a, b) => new Date(b.start_time).getTime() - new Date(a.start_time).getTime())
        .slice(0, 5);
      if (last5.length === 0) return { player, roundCount: result.data.length, avgScore: null, avgToPar: null };
      const avgScore = last5.reduce((s, r) => s + (r.total_score ?? 0), 0) / last5.length;
      // avgToPar requires course par — use avgScore - 72 as a rough proxy (par 72 assumption)
      // A production improvement would fetch course par per round and compute exactly.
      const avgToPar = Math.round(avgScore - 72);
      return { player, roundCount: result.data.length, avgScore, avgToPar };
    })
    .filter(Boolean)
    .sort((a, b) => {
      if (a!.avgScore === null) return 1;
      if (b!.avgScore === null) return -1;
      return a!.avgScore - b!.avgScore;
    }) as LeaderboardRow[];

  return (
    <View className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      <View className="px-4 pt-12 pb-4 flex-row items-center justify-between">
        <Text className="text-2xl font-bold text-[#111] dark:text-white">Friends</Text>
        <Pressable onPress={() => router.push('/profile')} hitSlop={8}>
          <Text className="text-xl">⚙</Text>
        </Pressable>
      </View>

      <FlatList
        data={rows}
        keyExtractor={(r) => r.player.id}
        contentContainerClassName="px-4 pb-8"
        ListEmptyComponent={
          <Text className="text-[#888] text-center mt-12">
            Invite friends to join and their scores will appear here.
          </Text>
        }
        renderItem={({ item, index }) => (
          <View className="flex-row items-center py-3 border-b border-[#e5e5e5] dark:border-[#2a2a2a]">
            <Text className="w-8 text-[#888] font-bold">{index + 1}</Text>
            <Avatar name={item.player.name} size={36} />
            <View className="flex-1 ml-3">
              <Text className="font-semibold text-[#111] dark:text-white">
                {item.player.name}{item.player.id === me?.id ? ' (you)' : ''}
              </Text>
              <Text className="text-[#888] text-sm">{item.roundCount} rounds</Text>
            </View>
            <View className="items-end">
              {item.avgScore !== null ? (
                <>
                  <Text className="font-bold text-lg text-[#111] dark:text-white">
                    {item.avgScore.toFixed(1)}
                  </Text>
                  <ScoreLabel toPar={item.avgToPar ?? 0} size="sm" />
                </>
              ) : (
                <Text className="text-[#888]">—</Text>
              )}
            </View>
          </View>
        )}
      />
    </View>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add app/'(tabs)'/friends.tsx
git commit -m "feat: Friends leaderboard with parallel player round fetches"
```

---

## Task 18: Profile Screen

**Files:**
- Create: `ui/app/(tabs)/profile.tsx`

- [ ] **Step 1: Implement Profile screen**

```tsx
// ui/app/(tabs)/profile.tsx
import React, { useState } from 'react';
import { View, Text, TextInput, Pressable, Alert, ScrollView, Appearance } from 'react-native';
import { useRouter } from 'expo-router';
import { useCurrentPlayer, useUpdatePlayer } from '../../lib/queries';
import { clearToken } from '../../lib/auth';
import { getTheme, setTheme } from '../../lib/storage';
import { Button } from '../../components/shared/Button';
import { Avatar } from '../../components/shared/Avatar';
import { useEffect } from 'react';

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
    // Apply immediately — don't wait for next cold start
    Appearance.setColorScheme(t !== 'system' ? t : null);
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
          <Text className="text-[#888]">← Back</Text>
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
          placeholder="—"
          placeholderTextColor="#888"
        />

        <Button label="Save" onPress={handleSave} loading={updatePlayer.isPending} />

        {/* Theme selector */}
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
```

- [ ] **Step 2: Commit**

```bash
git add app/'(tabs)'/profile.tsx
git commit -m "feat: Profile screen with edit, theme toggle, and logout"
```

---

## Task 19: Smoke Test on Device

- [ ] **Step 1: Start the backend**

From the repo root:
```bash
docker compose up --build -d
alembic upgrade head
docker exec -i postscore_db psql -U postgres -d postscore < seed_data.sql
```

- [ ] **Step 2: Start the Expo dev server**

```bash
cd ui
npx expo start
```

- [ ] **Step 3: Manual smoke test checklist**

- [ ] Signup creates an account and lands on Play tab
- [ ] Login with existing account works
- [ ] Start Round: select course → select tee box → select 18 holes → tap Start
- [ ] Live Scorecard: score stepper works, fairway toggle hides on par-3s
- [ ] Hole Progress dots fill correctly as holes are scored
- [ ] Finish Round lands on Round Summary with stats
- [ ] Rounds tab shows the completed round
- [ ] Friends tab shows all players ranked by avg score
- [ ] Profile: name edit saves, theme toggle changes appearance, logout returns to Login
- [ ] Kill the app mid-round, reopen — scorecard resumes at correct hole

- [ ] **Step 4: Run the full test suite**

```bash
npx jest
```
Expected: all tests PASS

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "feat: POSTscore UI — complete Expo app"
```

---

## Notes for Implementer

**Test setup gotcha:** `jest-expo` requires `transformIgnorePatterns` to be set or native modules will fail to transform. The config in Task 1 covers this.

**NativeWind dark mode:** Use `dark:` class variants. NativeWind v4 reads from the `colorScheme` of `useColorScheme()`. To apply user-stored dark mode preference, call `Appearance.setColorScheme(preferredScheme)` in the root layout after reading the AsyncStorage preference.

**Route ordering in `(tabs)/_layout.tsx`:** `profile` and `rounds/[id]` must be listed with `href: null` to hide them from the tab bar while keeping them navigable.

**Hole par lookup in Round Summary:** `RoundWithHolesResponse.round_holes` contains `tee_box_hole_id` but not the par value. Cross-reference with the TanStack Query `['teeBox', teeBoxId]` cache (which was fetched at Start Round time) to resolve par per hole. The Round Summary screen in Task 15 has a TODO comment for this — implement when course cache is confirmed to be populated.

**Offline PATCH (Finish Round):** If the device is offline when the user taps "Finish Round", the `PATCH /api/v1/rounds/{id}` will fail. The offline queue processor only handles hole submissions. A production improvement would be to queue the PATCH as well. For v1, the round remains open in the backend until connectivity is restored and the user re-finishes, or an admin closes it.
