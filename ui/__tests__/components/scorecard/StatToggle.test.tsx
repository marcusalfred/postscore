import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { StatToggle } from '../../../components/scorecard/StatToggle';

describe('StatToggle', () => {
  const options = ['YES', 'NO'];

  it('renders all options', () => {
    const { getByText } = render(
      <StatToggle options={options} value="YES" onChange={() => {}} />
    );
    expect(getByText('YES')).toBeTruthy();
    expect(getByText('NO')).toBeTruthy();
  });

  it('calls onChange when an option is pressed', () => {
    const onChange = jest.fn();
    const { getByText } = render(
      <StatToggle options={options} value="YES" onChange={onChange} />
    );
    fireEvent.press(getByText('NO'));
    expect(onChange).toHaveBeenCalledWith('NO');
  });
});
