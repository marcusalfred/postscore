import { buildRequest, BASE_URL } from '../../lib/api';

describe('buildRequest', () => {
  it('builds a GET request with auth header', () => {
    const req = buildRequest('GET', '/api/v1/courses/', 'tok123');
    expect(req.method).toBe('GET');
    expect(req.headers.get('Authorization')).toBe('Bearer tok123');
    expect(req.url).toBe(`${BASE_URL}/api/v1/courses/`);
  });

  it('builds form-encoded POST for login (no JSON)', () => {
    const req = buildRequest('POST', '/api/v1/auth/login', null, {
      formEncoded: true,
      body: { username: 'a@b.com', password: 'pass' },
    });
    expect(req.headers.get('Content-Type')).toContain('application/x-www-form-urlencoded');
  });

  it('builds JSON POST with body', () => {
    const req = buildRequest('POST', '/api/v1/rounds/', 'tok', {
      body: { course_id: '123' },
    });
    expect(req.headers.get('Content-Type')).toBe('application/json');
  });
});
