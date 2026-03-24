import React from 'react';
import { Text } from 'react-native';

type Props = { toPar: number; size?: 'sm' | 'md' | 'lg' };

export function ScoreLabel({ toPar, size = 'md' }: Props) {
  const label = toPar === 0 ? 'E' : toPar > 0 ? `+${toPar}` : `${toPar}`;
  const color =
    toPar < 0 ? '#43a047' : toPar > 0 ? '#e53935' : '#888888';
  const fontSize = size === 'lg' ? 24 : size === 'sm' ? 12 : 16;
  const fontWeight: '600' | '700' = size === 'lg' ? '700' : '600';

  return (
    <Text style={{ color, fontSize, fontWeight }}>
      {label}
    </Text>
  );
}
