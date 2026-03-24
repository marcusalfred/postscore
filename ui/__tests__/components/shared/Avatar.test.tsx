import React from 'react';
import { render } from '@testing-library/react-native';
import { Avatar } from '../../../components/shared/Avatar';

it('renders initials from name', () => {
  const { getByText } = render(<Avatar name="Alex Golfer" />);
  expect(getByText('AG')).toBeTruthy();
});
