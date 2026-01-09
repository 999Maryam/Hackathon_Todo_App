import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

const Card: React.FC<CardProps> = ({ className, ...props }) => {
  return (
    <div
      className={`bg-white rounded-lg shadow-md overflow-hidden ${className || ''}`}
      {...props}
    />
  );
};

const CardContent: React.FC<CardContentProps> = ({ className, ...props }) => {
  return (
    <div className={`p-6 ${className || ''}`} {...props} />
  );
};

Card.displayName = "Card";
CardContent.displayName = "CardContent";

export { Card, CardContent };