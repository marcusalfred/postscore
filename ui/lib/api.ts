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
