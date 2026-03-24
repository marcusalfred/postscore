import { getToken, setToken, clearToken } from '../../lib/auth';

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
