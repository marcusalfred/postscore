import React from 'react';
import { View, Text } from 'react-native';

type Props = { name: string; size?: number };

export function Avatar({ name, size = 40 }: Props) {
  const initials = name.trim()
    ? name
        .trim()
        .split(/\s+/)
        .slice(0, 2)
        .map((w) => w[0]?.toUpperCase() ?? '')
        .join('')
    : '?';

  return (
    <View
      className="bg-[#e5e5e5] dark:bg-[#2a2a2a]"
      style={{
        width: size,
        height: size,
        borderRadius: size / 2,
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Text
        className="text-[#111] dark:text-white"
        style={{ fontWeight: 'bold', fontSize: size * 0.35 }}
      >
        {initials}
      </Text>
    </View>
  );
}
