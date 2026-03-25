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
