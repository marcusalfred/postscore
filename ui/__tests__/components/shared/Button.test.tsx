import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { Button } from '../../../components/shared/Button';

describe('Button', () => {
  it('renders label', () => {
    const { getByText } = render(<Button label="Log in" onPress={() => {}} />);
    expect(getByText('Log in')).toBeTruthy();
  });

  it('calls onPress when tapped', () => {
    const onPress = jest.fn();
    const { getByText } = render(<Button label="Go" onPress={onPress} />);
    fireEvent.press(getByText('Go'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });

  it('does not call onPress when loading', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <Button label="Go" onPress={onPress} loading />
    );
    fireEvent.press(getByText('Go'));
    expect(onPress).not.toHaveBeenCalled();
  });
});
