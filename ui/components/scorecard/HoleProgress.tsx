import React from 'react';
import { View, ScrollView } from 'react-native';

type ScoredHole = { holeNumber: number; toPar: number };
type Props = { total: number; currentHole: number; scoredHoles: ScoredHole[] };

export function HoleProgress({ total, currentHole, scoredHoles }: Props) {
  const scoredMap = new Map(scoredHoles.map((h) => [h.holeNumber, h.toPar]));

  return (
    <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerClassName="px-4 py-2 gap-1.5 flex-row">
      {Array.from({ length: total }, (_, i) => {
        const holeNum = i + 1;
        const toPar = scoredMap.get(holeNum);
        const isScored = toPar !== undefined;
        const isCurrent = holeNum === currentHole;

        let bg = 'bg-[#e5e5e5] dark:bg-[#2a2a2a]';
        if (isScored) {
          bg = toPar < 0 ? 'bg-[#43a047]' : toPar > 0 ? 'bg-[#e53935]' : 'bg-[#888]';
        }

        return (
          <View
            key={holeNum}
            testID="hole-dot"
            className={`w-3 h-3 rounded-full ${bg} ${isCurrent && !isScored ? 'border-2 border-[#111] dark:border-white' : ''}`}
          />
        );
      })}
    </ScrollView>
  );
}
