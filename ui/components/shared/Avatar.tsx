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
      style={{
        width: size,
        height: size,
        borderRadius: size / 2,
        backgroundColor: '#e5e5e5',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Text style={{ fontWeight: 'bold', color: '#111111', fontSize: size * 0.35 }}>
        {initials}
      </Text>
    </View>
  );
}
