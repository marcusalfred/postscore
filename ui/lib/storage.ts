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
  scored_holes: ScoredHoleEntry[];
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
