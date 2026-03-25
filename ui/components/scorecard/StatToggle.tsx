import React from 'react';
import { View, Text, Pressable } from 'react-native';

type Props = { options: string[]; value: string; onChange: (v: string) => void; label?: string };

export function StatToggle({ options, value, onChange, label }: Props) {
  return (
    <View className="items-center">
      {label && <Text className="text-xs font-semibold text-[#888] mb-2 uppercase tracking-wide">{label}</Text>}
      <View className="flex-row rounded-xl overflow-hidden border border-[#e5e5e5] dark:border-[#2a2a2a]">
        {options.map((opt) => (
          <Pressable
            key={opt}
            onPress={() => onChange(opt)}
            className={`px-4 py-2 ${opt === value ? 'bg-[#111] dark:bg-white' : 'bg-white dark:bg-[#1c1c1e]'}`}
          >
            <Text
              className={`text-sm font-semibold ${opt === value ? 'text-white dark:text-[#111]' : 'text-[#111] dark:text-white'}`}
            >
              {opt}
            </Text>
          </Pressable>
        ))}
      </View>
    </View>
  );
}
