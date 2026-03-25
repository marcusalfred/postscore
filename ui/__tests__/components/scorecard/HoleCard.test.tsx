import React from 'react';
import { render } from '@testing-library/react-native';
import { HoleCard, HoleCardState } from '../../../components/scorecard/HoleCard';

const baseState: HoleCardState = { score: 4, gir: false, fairway: 'o', putts: 2 };

describe('HoleCard', () => {
  it('displays hole number and par', () => {
    const { getByText } = render(
      <HoleCard holeNumber={5} par={4} yards={420} state={baseState} onChange={() => {}} />
    );
    expect(getByText('Hole 5')).toBeTruthy();
    expect(getByText('Par 4 \u00b7 420 yds')).toBeTruthy();
  });

  it('hides fairway toggle on par-3', () => {
    const par3State: HoleCardState = { score: 3, gir: true, fairway: null, putts: 1 };
    const { queryByText } = render(
      <HoleCard holeNumber={3} par={3} yards={155} state={par3State} onChange={() => {}} />
    );
    expect(queryByText('Fairway')).toBeNull();
  });

  it('shows fairway toggle on par-4', () => {
    const { getByText } = render(
      <HoleCard holeNumber={1} par={4} yards={400} state={baseState} onChange={() => {}} />
    );
    expect(getByText('Fairway')).toBeTruthy();
  });
});
