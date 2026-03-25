import React from 'react';
import { View, Text } from 'react-native';
import { Card } from '../shared/Card';
import { ScoreStepper } from './ScoreStepper';
import { StatToggle } from './StatToggle';
import { PuttsStepper } from './PuttsStepper';

const FAIRWAY_OPTIONS = ['HIT', 'LEFT', 'RIGHT', 'SHORT', 'LONG'];
const FAIRWAY_API_MAP: Record<string, string> = {
  HIT: 'o', LEFT: '<', RIGHT: '>', SHORT: 'v', LONG: '^',
};

export type HoleCardState = {
  score: number;
  gir: boolean;
  fairway: string | null;
  putts: number;
};

type Props = {
  holeNumber: number;
  par: number;
  yards: number;
  state: HoleCardState;
  onChange: (state: HoleCardState) => void;
};

export function HoleCard({ holeNumber, par, yards, state, onChange }: Props) {
  const isParThree = par === 3;

  return (
    <Card>
      <View className="flex-row justify-between mb-4">
        <Text className="text-lg font-bold text-[#111] dark:text-white">Hole {holeNumber}</Text>
        <Text className="text-[#888]">Par {par} {'\u00b7'} {yards} yds</Text>
      </View>

      <ScoreStepper
        value={state.score}
        par={par}
        onChange={(score) => onChange({ ...state, score })}
      />

      <View className="mt-6 flex-row justify-around">
        <StatToggle
          label="GIR"
          options={['YES', 'NO']}
          value={state.gir ? 'YES' : 'NO'}
          onChange={(v) => onChange({ ...state, gir: v === 'YES' })}
        />
        {!isParThree && (
          <StatToggle
            label="Fairway"
            options={FAIRWAY_OPTIONS}
            value={
              state.fairway
                ? (Object.entries(FAIRWAY_API_MAP).find(([, api]) => api === state.fairway)?.[0] ?? 'HIT')
                : 'HIT'
            }
            onChange={(v) => onChange({ ...state, fairway: FAIRWAY_API_MAP[v] })}
          />
        )}
        <PuttsStepper
          value={state.putts}
          onChange={(putts) => onChange({ ...state, putts })}
        />
      </View>
    </Card>
  );
}
