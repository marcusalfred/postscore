import React, { useState, useEffect } from 'react';
import {
  View, Text, ScrollView, TextInput, Pressable, ActivityIndicator, Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useCourses, useTeeBoxDetail, useStartRound, CourseResponse, TeeBoxBase } from '../../lib/queries';
import { saveActiveRound, getActiveRound } from '../../lib/storage';
import { Button } from '../../components/shared/Button';

export default function PlayTab() {
  const router = useRouter();
  const [activeRound, setActiveRound] = useState<Awaited<ReturnType<typeof getActiveRound>>>(null);
  const [search, setSearch] = useState('');
  const [selectedCourse, setSelectedCourse] = useState<CourseResponse | null>(null);
  const [selectedTeeId, setSelectedTeeId] = useState<string | null>(null);
  const [holes, setHoles] = useState<9 | 18>(18);

  const { data: courses, isLoading: loadingCourses } = useCourses();
  const { data: teeDetail } = useTeeBoxDetail(selectedTeeId);
  const startRound = useStartRound();

  useEffect(() => {
    getActiveRound().then(setActiveRound);
  }, []);

  // If there's an active round, show the scorecard (Task 13 replaces this placeholder)
  if (activeRound) {
    return <ActiveScorecard round={activeRound} onClear={() => setActiveRound(null)} />;
  }

  const filtered = (courses ?? []).filter((c) =>
    c.name.toLowerCase().includes(search.toLowerCase())
  );

  async function handleStart() {
    if (!selectedCourse || !selectedTeeId || !teeDetail) return;
    try {
      const round = await startRound.mutateAsync({
        course_id: selectedCourse.id,
        tee_box_id: selectedTeeId,
        holes,
      });
      const active = {
        round_id: round.id,
        course_id: selectedCourse.id,
        tee_box_id: selectedTeeId,
        tee_box_holes: teeDetail.holes.map((h) => ({
          id: h.id,
          number: h.number,
          par: h.par,
          yards: h.yards,
        })),
        holes_total: holes,
        scored_holes: [],
      };
      await saveActiveRound(active);
      setActiveRound(active);
    } catch {
      Alert.alert('Error', 'Could not start round. Try again.');
    }
  }

  return (
    <ScrollView className="flex-1 bg-[#f5f5f5] dark:bg-[#111]">
      <View className="px-4 pt-12 pb-6">
        <Text className="text-2xl font-bold text-[#111] dark:text-white mb-6">Start Round</Text>

        {/* Course search */}
        <Text className="text-xs font-semibold text-[#888] uppercase tracking-wide mb-2">Course</Text>
        <TextInput
          className="bg-white dark:bg-[#1c1c1e] rounded-xl px-4 py-3 text-base text-[#111] dark:text-white mb-2 border border-[#e5e5e5] dark:border-[#2a2a2a]"
          placeholder="Search courses..."
          placeholderTextColor="#888"
          value={search}
          onChangeText={setSearch}
        />

        {loadingCourses && <ActivityIndicator className="my-4" />}
        {!loadingCourses && filtered.length === 0 && (
          <Text className="text-[#888] text-center my-4">No courses available. Add via the API.</Text>
        )}
        {filtered.map((course) => (
          <Pressable
            key={course.id}
            onPress={() => { setSelectedCourse(course); setSelectedTeeId(null); setSearch(course.name); }}
            className={`rounded-xl px-4 py-3 mb-1 ${selectedCourse?.id === course.id ? 'bg-[#111] dark:bg-white' : 'bg-white dark:bg-[#1c1c1e]'} border border-[#e5e5e5] dark:border-[#2a2a2a]`}
          >
            <Text className={selectedCourse?.id === course.id ? 'text-white dark:text-[#111] font-semibold' : 'text-[#111] dark:text-white'}>
              {course.name}
            </Text>
            <Text className="text-[#888] text-sm">{course.city}, {course.state}</Text>
          </Pressable>
        ))}

        {/* Tee box selector */}
        {selectedCourse && (
          <>
            <Text className="text-xs font-semibold text-[#888] uppercase tracking-wide mt-6 mb-2">Tees</Text>
            <View className="flex-row flex-wrap gap-2">
              {selectedCourse.tees.map((tee: TeeBoxBase) => (
                <Pressable
                  key={tee.tee_id}
                  onPress={() => setSelectedTeeId(tee.tee_id)}
                  className={`px-4 py-2 rounded-full border ${selectedTeeId === tee.tee_id ? 'bg-[#111] dark:bg-white border-[#111] dark:border-white' : 'bg-white dark:bg-[#1c1c1e] border-[#e5e5e5] dark:border-[#2a2a2a]'}`}
                >
                  <Text className={selectedTeeId === tee.tee_id ? 'text-white dark:text-[#111] font-semibold' : 'text-[#111] dark:text-white'}>
                    {tee.tee}
                  </Text>
                </Pressable>
              ))}
            </View>
          </>
        )}

        {/* Holes selector */}
        <Text className="text-xs font-semibold text-[#888] uppercase tracking-wide mt-6 mb-2">Holes</Text>
        <View className="flex-row gap-2">
          {([9, 18] as const).map((n) => (
            <Pressable
              key={n}
              onPress={() => setHoles(n)}
              className={`px-6 py-2 rounded-full border ${holes === n ? 'bg-[#111] dark:bg-white border-[#111] dark:border-white' : 'bg-white dark:bg-[#1c1c1e] border-[#e5e5e5] dark:border-[#2a2a2a]'}`}
            >
              <Text className={holes === n ? 'text-white dark:text-[#111] font-semibold' : 'text-[#111] dark:text-white'}>{n}</Text>
            </Pressable>
          ))}
        </View>

        <View className="mt-8">
          <Button
            label="Start Round"
            onPress={handleStart}
            loading={startRound.isPending}
            disabled={!selectedCourse || !selectedTeeId}
          />
        </View>
      </View>
    </ScrollView>
  );
}

// Placeholder — replaced in Task 13
function ActiveScorecard({ round, onClear }: { round: NonNullable<Awaited<ReturnType<typeof getActiveRound>>>; onClear: () => void }) {
  return (
    <View className="flex-1 items-center justify-center bg-[#f5f5f5] dark:bg-[#111]">
      <Text className="text-[#111] dark:text-white">Round in progress...</Text>
      <Pressable onPress={onClear} className="mt-4">
        <Text className="text-[#e53935]">Abandon Round</Text>
      </Pressable>
    </View>
  );
}
