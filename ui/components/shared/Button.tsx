import React from 'react';
import { Pressable, Text, ActivityIndicator } from 'react-native';

type Props = {
  label: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary';
  loading?: boolean;
  disabled?: boolean;
};

export function Button({
  label,
  onPress,
  variant = 'primary',
  loading = false,
  disabled = false,
}: Props) {
  const isPrimary = variant === 'primary';
  const isDisabled = disabled || loading;

  return (
    <Pressable
      onPress={isDisabled ? undefined : onPress}
      disabled={isDisabled}
      style={{
        borderRadius: 12,
        paddingHorizontal: 24,
        paddingVertical: 16,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: isPrimary ? '#111111' : 'transparent',
        borderWidth: isPrimary ? 0 : 1,
        borderColor: '#e5e5e5',
        opacity: isDisabled ? 0.4 : 1,
      }}
    >
      {loading && <ActivityIndicator color={isPrimary ? '#fff' : '#111'} />}
      <Text
        style={{
          fontWeight: '600',
          fontSize: 16,
          color: isPrimary ? '#ffffff' : '#111111',
          opacity: loading ? 0 : 1,
        }}
      >
        {label}
      </Text>
    </Pressable>
  );
}
