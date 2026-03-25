import React from 'react';
import {
  View, Text, ScrollView, Pressable, ActivityIndicator,
} from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useRoundDetail, useRoundStats, useTeeBoxDetail } from '../../../lib/queries';
import { StatsGrid } from '../../../components/rounds/StatsGrid';
import { Card } from '../../../components/shared/Card';
import { ScoreLabel } from '../../../components/shared/ScoreLabel';

export default function RoundSummaryScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { data: round, isLoading: loadingRound, isError: errorRound, refetch } = useRoundDetail(id);
  const { data: stats, isLoading: loadingStats, isError: errorStats } = useRoundStats(id);
  const { data: teeBox } = useTeeBoxDetail(round?.tee_box_id ?? null);
  const holeMap = new Map(teeBox?.holes.map((h) => [h.id, h]) ?? []);

  if (loadingRound || loadingStats) {
    return (
      <View className="flex-1 items-center justify-center bg-[#f5f5f5] dark:bg-[#111]">
        <ActivityIndicator />
      </View>
    );
  }

  if (errorRound || errorStats) {
    return (
      <View className="flex-1 items-center justify-center bg-[#f5f5f5] dark:bg-[#111] px-6">
        <Text className="text-[#111] dark:text-white mb-4">Could not load round stats.</Text>
        <Pressable onPress={() => refetch()} className="px-6 py-3 bg-[#111] dark:bg-white rounded-xl">
          <Text className="text-white dark:text-[#111] font-semibold">Retry</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      <View className="px-4 pt-12 pb-6">
        <Text className="text-2xl font-bold text-[#111] dark:text-white mb-2">Round Summary</Text>

        {stats && (
          <Card style={{ marginBottom: 16 }}>
            <StatsGrid stats={stats} />
          </Card>
        )}

        <Card>
          <View className="flex-row border-b border-[#e5e5e5] dark:border-[#2a2a2a] pb-2 mb-2">
            {['Hole', 'Par', 'Score', '+/-'].map((h) => (
              <Text key={h} className="flex-1 text-center text-xs font-semibold text-[#888] uppercase">
                {h}
              </Text>
            ))}
          </View>
          {(round?.round_holes ?? [])
            .slice()
            .sort((a, b) => (holeMap.get(a.tee_box_hole_id)?.number ?? 0) - (holeMap.get(b.tee_box_hole_id)?.number ?? 0))
            .map((hole) => {
              const stub = holeMap.get(hole.tee_box_hole_id);
              const par = stub?.par ?? 4;
              const holeNumber = stub?.number ?? '?';
              const toPar = hole.score - par;
              return (
                <View key={hole.id} className="flex-row py-2 border-b border-[#e5e5e5] dark:border-[#2a2a2a]">
                  <Text className="flex-1 text-center text-[#111] dark:text-white">{holeNumber}</Text>
                  <Text className="flex-1 text-center text-[#888]">{par}</Text>
                  <Text className="flex-1 text-center font-bold text-[#111] dark:text-white">{hole.score}</Text>
                  <View className="flex-1 items-center">
                    <ScoreLabel toPar={toPar} size="sm" />
                  </View>
                </View>
              );
            })}
        </Card>

        <Pressable
          className="mt-6 items-center py-4"
          onPress={() => router.replace('/rounds')}
        >
          <Text className="font-semibold text-[#111] dark:text-white">Done</Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}
