import React from 'react';
import { View, Text } from 'react-native';
import { ScoreLabel } from '../shared/ScoreLabel';
import type { RoundStatsResponse } from '../../lib/queries';

type Props = { stats: RoundStatsResponse };

export function StatsGrid({ stats }: Props) {
  const items = [
    { label: 'Score', value: `${stats.total_score}` },
    { label: 'To Par', node: <ScoreLabel toPar={stats.to_par} size="md" /> },
    { label: 'GIR', value: `${stats.gir_percentage.toFixed(0)}%` },
    { label: 'FIR', value: `${stats.fairways_percentage.toFixed(0)}%` },
    { label: 'Putts', value: `${stats.avg_putts_per_hole.toFixed(1)}/hole` },
    { label: 'Penalties', value: `${stats.penalties}` },
  ];

  return (
    <View className="flex-row flex-wrap">
      {items.map(({ label, value, node }) => (
        <View key={label} className="w-1/3 items-center py-3">
          <Text className="text-xs text-[#888] uppercase tracking-wide mb-1">{label}</Text>
          {node ?? <Text className="text-lg font-bold text-[#111] dark:text-white">{value}</Text>}
        </View>
      ))}
    </View>
  );
}
