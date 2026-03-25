import AsyncStorage from '@react-native-async-storage/async-storage';
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

beforeEach(() => {
  jest.clearAllMocks();
  (AsyncStorage as any).__resetStore();
});

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
