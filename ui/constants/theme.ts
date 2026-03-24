export const Colors = {
  light: {
    background: '#f5f5f5',
    surface: '#ffffff',
    surfaceElevated: '#f0f0f0',
    textPrimary: '#111111',
    textSecondary: '#888888',
    textMuted: '#bbbbbb',
    border: '#e5e5e5',
    actionBg: '#111111',
    actionText: '#ffffff',
  },
  dark: {
    background: '#111111',
    surface: '#1c1c1e',
    surfaceElevated: '#2a2a2a',
    textPrimary: '#ffffff',
    textSecondary: '#666666',
    textMuted: '#444444',
    border: '#2a2a2a',
    actionBg: '#ffffff',
    actionText: '#111111',
  },
  // Scoring accents — same in both modes
  birdie: '#43a047',
  bogey: '#e53935',
} as const;

export type ColorScheme = 'light' | 'dark';
