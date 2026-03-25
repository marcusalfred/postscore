import React from 'react';
import { View, Text, Pressable } from 'react-native';

const PAR_LABELS: Record<number, string> = {
  [-3]: 'ALBATROSS',
  [-2]: 'EAGLE',
  [-1]: 'BIRDIE',
  [0]: 'PAR',
  [1]: 'BOGEY',
  [2]: 'DOUBLE',
};

function getLabel(diff: number): string {
  if (diff in PAR_LABELS) return PAR_LABELS[diff];
  return `+${diff}`;
}

type Props = { value: number; par: number; onChange: (v: number) => void };

export function ScoreStepper({ value, par, onChange }: Props) {
  const diff = value - par;
  const borderColor = diff < 0 ? '#43a047' : diff > 0 ? '#e53935' : '#e5e5e5';
  const label = getLabel(diff);

  return (
    <View className="items-center">
      <View className="flex-row items-center gap-6">
        <Pressable
          onPress={() => value > 1 && onChange(value - 1)}
          hitSlop={12}
          className="w-12 h-12 items-center justify-center"
        >
          <Text className="text-3xl text-[#111] dark:text-white">{'\u2212'}</Text>
        </Pressable>

        <View
          className="w-20 h-20 rounded-full items-center justify-center border-2"
          style={{ borderColor }}
        >
          <Text className="text-3xl font-bold text-[#111] dark:text-white">{value}</Text>
        </View>

        <Pressable
          onPress={() => onChange(value + 1)}
          hitSlop={12}
          className="w-12 h-12 items-center justify-center"
        >
          <Text className="text-3xl text-[#111] dark:text-white">+</Text>
        </Pressable>
      </View>

      <Text
        className="mt-2 text-sm font-semibold"
        style={{ color: diff < 0 ? '#43a047' : diff > 0 ? '#e53935' : '#888' }}
      >
        {label}
      </Text>
    </View>
  );
}
