import React from 'react';
import { render } from '@testing-library/react-native';
import { ScoreLabel } from '../../../components/shared/ScoreLabel';

describe('ScoreLabel', () => {
  it('shows E for even par', () => {
    const { getByText } = render(<ScoreLabel toPar={0} />);
    expect(getByText('E')).toBeTruthy();
  });

  it('shows +2 for over par', () => {
    const { getByText } = render(<ScoreLabel toPar={2} />);
    expect(getByText('+2')).toBeTruthy();
  });

  it('shows -1 for under par', () => {
    const { getByText } = render(<ScoreLabel toPar={-1} />);
    expect(getByText('-1')).toBeTruthy();
  });
});
