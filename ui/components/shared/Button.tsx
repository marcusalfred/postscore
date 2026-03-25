import React from 'react';
import { Pressable, Text, ActivityIndicator, useColorScheme } from 'react-native';

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
  const isDark = useColorScheme() === 'dark';

  return (
    <Pressable
      onPress={isDisabled ? undefined : onPress}
      disabled={isDisabled}
      className={
        isPrimary
          ? 'bg-[#111] dark:bg-white'
          : 'border border-[#111] dark:border-white'
      }
      style={{
        borderRadius: 12,
        paddingHorizontal: 24,
        paddingVertical: 16,
        alignItems: 'center',
        justifyContent: 'center',
        opacity: isDisabled ? 0.4 : 1,
      }}
    >
      {loading && (
        <ActivityIndicator color={isPrimary ? (isDark ? '#111' : '#fff') : (isDark ? '#fff' : '#111')} />
      )}
      <Text
        className={
          isPrimary
            ? 'text-white dark:text-[#111]'
            : 'text-[#111] dark:text-white'
        }
        style={{
          fontWeight: '600',
          fontSize: 16,
          opacity: loading ? 0 : 1,
        }}
      >
        {label}
      </Text>
    </Pressable>
  );
}
