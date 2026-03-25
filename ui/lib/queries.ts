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
