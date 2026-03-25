import React from 'react';
import { View, Text, Pressable } from 'react-native';

type Props = { value: number; onChange: (v: number) => void };

export function PuttsStepper({ value, onChange }: Props) {
  return (
    <View className="items-center">
      <Text className="text-xs font-semibold text-[#888] mb-2 uppercase tracking-wide">Putts</Text>
      <View className="flex-row items-center gap-4">
        <Pressable onPress={() => value > 0 && onChange(value - 1)} hitSlop={12}>
          <Text className="text-2xl text-[#111] dark:text-white">{'\u2212'}</Text>
        </Pressable>
        <Text className="text-2xl font-bold text-[#111] dark:text-white w-8 text-center">{value}</Text>
        <Pressable onPress={() => value < 6 && onChange(value + 1)} hitSlop={12}>
          <Text className="text-2xl text-[#111] dark:text-white">+</Text>
        </Pressable>
      </View>
    </View>
  );
}
