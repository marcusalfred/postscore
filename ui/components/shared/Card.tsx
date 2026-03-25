import React from 'react';
import { View, ViewProps } from 'react-native';

export function Card({ children, style, ...props }: ViewProps) {
  return (
    <View
      className="bg-white dark:bg-[#1c1c1e] border border-[#e5e5e5] dark:border-[#2a2a2a]"
      style={[
        {
          borderRadius: 16,
          padding: 16,
          shadowColor: '#000',
          shadowOpacity: 0.05,
          shadowRadius: 4,
          shadowOffset: { width: 0, height: 2 },
          elevation: 2,
        },
        style,
      ]}
      {...props}
    >
      {children}
    </View>
  );
}
