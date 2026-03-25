import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { PuttsStepper } from '../../../components/scorecard/PuttsStepper';

describe('PuttsStepper', () => {
  it('displays the current putts value', () => {
    const { getByText } = render(<PuttsStepper value={2} onChange={() => {}} />);
    expect(getByText('2')).toBeTruthy();
  });

  it('increments up to 6', () => {
    const onChange = jest.fn();
    const { getAllByText } = render(<PuttsStepper value={2} onChange={onChange} />);
    fireEvent.press(getAllByText('+')[0]);
    expect(onChange).toHaveBeenCalledWith(3);
  });

  it('does not go above 6', () => {
    const onChange = jest.fn();
    const { getAllByText } = render(<PuttsStepper value={6} onChange={onChange} />);
    fireEvent.press(getAllByText('+')[0]);
    expect(onChange).not.toHaveBeenCalled();
  });

  it('does not go below 0', () => {
    const onChange = jest.fn();
    const { getAllByText } = render(<PuttsStepper value={0} onChange={onChange} />);
    fireEvent.press(getAllByText('\u2212')[0]);
    expect(onChange).not.toHaveBeenCalled();
  });
});
