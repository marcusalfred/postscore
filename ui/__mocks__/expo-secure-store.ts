const store: Record<string, string> = {};
export const getItemAsync = jest.fn(async (key: string) => store[key] ?? null);
export const setItemAsync = jest.fn(async (key: string, val: string) => { store[key] = val; });
export const deleteItemAsync = jest.fn(async (key: string) => { delete store[key]; });
