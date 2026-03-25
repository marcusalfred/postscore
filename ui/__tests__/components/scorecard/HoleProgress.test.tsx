import React from 'react';
import { render } from '@testing-library/react-native';
import { HoleProgress } from '../../../components/scorecard/HoleProgress';

it('renders the correct number of dots', () => {
  const { getAllByTestId } = render(
    <HoleProgress total={9} currentHole={3} scoredHoles={[{ holeNumber: 1, toPar: 0 }, { holeNumber: 2, toPar: -1 }]} />
  );
  expect(getAllByTestId('hole-dot')).toHaveLength(9);
});
