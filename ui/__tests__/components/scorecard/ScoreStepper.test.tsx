import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { ScoreStepper } from '../../../components/scorecard/ScoreStepper';

describe('ScoreStepper', () => {
  it('displays the current score', () => {
    const { getByText } = render(
      <ScoreStepper value={4} par={4} onChange={() => {}} />
    );
    expect(getByText('4')).toBeTruthy();
  });

  it('increments on + press', () => {
    const onChange = jest.fn();
    const { getByText } = render(<ScoreStepper value={4} par={4} onChange={onChange} />);
    fireEvent.press(getByText('+'));
    expect(onChange).toHaveBeenCalledWith(5);
  });

  it('decrements on \u2212 press', () => {
    const onChange = jest.fn();
    const { getByText } = render(<ScoreStepper value={4} par={4} onChange={onChange} />);
    fireEvent.press(getByText('\u2212'));
    expect(onChange).toHaveBeenCalledWith(3);
  });

  it('does not go below 1', () => {
    const onChange = jest.fn();
    const { getByText } = render(<ScoreStepper value={1} par={4} onChange={onChange} />);
    fireEvent.press(getByText('\u2212'));
    expect(onChange).not.toHaveBeenCalled();
  });

  it('shows PAR label when score equals par', () => {
    const { getByText } = render(<ScoreStepper value={4} par={4} onChange={() => {}} />);
    expect(getByText('PAR')).toBeTruthy();
  });

  it('shows BIRDIE label when score is par - 1', () => {
    const { getByText } = render(<ScoreStepper value={3} par={4} onChange={() => {}} />);
    expect(getByText('BIRDIE')).toBeTruthy();
  });
});
