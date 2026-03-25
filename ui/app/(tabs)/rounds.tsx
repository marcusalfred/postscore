import React from 'react';
import { View, Text, FlatList, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { useRounds, useCourses, useCurrentPlayer } from '../../lib/queries';
import { RoundCard } from '../../components/rounds/RoundCard';

export default function RoundsTab() {
  const router = useRouter();
  const { data: me } = useCurrentPlayer();
  const { data: rounds, isLoading } = useRounds(me?.id ?? null);
  const { data: courses } = useCourses();

  if (isLoading) {
    return (
      <View className="flex-1 items-center justify-center bg-[#f5f5f5] dark:bg-[#111]">
        <ActivityIndicator />
      </View>
    );
  }

  const sorted = (rounds ?? []).slice().sort(
    (a, b) => new Date(b.start_time).getTime() - new Date(a.start_time).getTime()
  );

  return (
    <View className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      <View className="px-4 pt-12 pb-4">
        <Text className="text-2xl font-bold text-[#111] dark:text-white">Rounds</Text>
      </View>
      <FlatList
        data={sorted}
        keyExtractor={(r) => r.id}
        contentContainerClassName="px-4 pb-8"
        ListEmptyComponent={
          <Text className="text-[#888] text-center mt-12">
            No rounds yet. Head to the Play tab to start your first round.
          </Text>
        }
        renderItem={({ item }) => (
          <RoundCard
            round={item}
            courses={courses ?? []}
            onPress={() => router.push(`/rounds/${item.id}`)}
          />
        )}
      />
    </View>
  );
}
