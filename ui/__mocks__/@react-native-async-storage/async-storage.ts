const store: Record<string, string> = {};

const mock = {
  getItem: jest.fn(async (key: string) => store[key] ?? null),
  setItem: jest.fn(async (key: string, val: string) => { store[key] = val; }),
  removeItem: jest.fn(async (key: string) => { delete store[key]; }),
  multiRemove: jest.fn(async (keys: string[]) => { keys.forEach((k) => delete store[k]); }),
  __resetStore: () => { Object.keys(store).forEach((k) => delete store[k]); },
};

export default mock;
