import React from 'react';
import { View, Text, Pressable } from 'react-native';
import { Card } from '../shared/Card';
import type { RoundResponse, CourseResponse } from '../../lib/queries';

type Props = {
  round: RoundResponse;
  courses: CourseResponse[];
  onPress: () => void;
};

export function RoundCard({ round, courses, onPress }: Props) {
  const course = courses.find((c) => c.id === round.course_id);
  const tee = course?.tees.find((t) => t.tee_id === round.tee_box_id);
  const date = new Date(round.start_time).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  });

  return (
    <Pressable onPress={onPress}>
      <Card style={{ marginBottom: 12 }}>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <View style={{ flex: 1 }}>
            <Text className="font-bold text-base text-[#111] dark:text-white">
              {course?.name ?? 'Unknown Course'}
            </Text>
            <Text style={{ color: '#888', fontSize: 14, marginTop: 2 }}>
              {date} {'\u00b7'} {tee?.tee ?? '\u2014'} {'\u00b7'} {round.holes} holes
            </Text>
          </View>
          <View style={{ alignItems: 'flex-end' }}>
            <Text className="text-2xl font-bold text-[#111] dark:text-white">
              {round.total_score ?? '\u2014'}
            </Text>
          </View>
        </View>
      </Card>
    </Pressable>
  );
}
