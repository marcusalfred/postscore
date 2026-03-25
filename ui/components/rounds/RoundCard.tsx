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
            <Text style={{ fontWeight: 'bold', fontSize: 16, color: '#111' }}>
              {course?.name ?? 'Unknown Course'}
            </Text>
            <Text style={{ color: '#888', fontSize: 14, marginTop: 2 }}>
              {date} {'\u00b7'} {tee?.tee ?? '\u2014'} {'\u00b7'} {round.holes} holes
            </Text>
          </View>
          <View style={{ alignItems: 'flex-end' }}>
            <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#111' }}>
              {round.total_score ?? '\u2014'}
            </Text>
          </View>
        </View>
      </Card>
    </Pressable>
  );
}
