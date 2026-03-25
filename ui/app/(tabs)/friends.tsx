import React from 'react';
import { View, Text, FlatList, ActivityIndicator, Pressable } from 'react-native';
import { useRouter } from 'expo-router';
import { useQueries } from '@tanstack/react-query';
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
    .map((player, i): LeaderboardRow | null => {
      const result = roundQueries[i];
      if (!result.data) return null;
      const last5 = result.data
        .filter((r) => r.total_score !== null)
        .sort((a, b) => new Date(b.start_time).getTime() - new Date(a.start_time).getTime())
        .slice(0, 5);
      if (last5.length === 0) return { player, roundCount: result.data.length, avgScore: null, avgToPar: null };
      const avgScore = last5.reduce((s, r) => s + (r.total_score ?? 0), 0) / last5.length;
      // avgToPar: use avgScore - 72 as a proxy (par 72 assumption)
      const avgToPar = Math.round(avgScore - 72);
      return { player, roundCount: result.data.length, avgScore, avgToPar };
    })
    .filter((r): r is LeaderboardRow => r !== null)
    .sort((a, b) => {
      if (a.avgScore === null) return 1;
      if (b.avgScore === null) return -1;
      return a.avgScore - b.avgScore;
    });

  return (
    <View className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      <View className="px-4 pt-12 pb-4 flex-row items-center justify-between">
        <Text className="text-2xl font-bold text-[#111] dark:text-white">Friends</Text>
        <Pressable onPress={() => router.push('/profile')} hitSlop={8}>
          <Text className="text-xl">{'\u2699'}</Text>
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
                <Text className="text-[#888]">{'\u2014'}</Text>
              )}
            </View>
          </View>
        )}
      />
    </View>
  );
}
