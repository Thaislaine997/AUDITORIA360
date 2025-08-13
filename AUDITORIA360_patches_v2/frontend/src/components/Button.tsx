import React from 'react'

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost'
}

export default function Button({ variant = 'primary', children, ...rest }: Props) {
  const base = 'px-4 py-2 rounded-xl font-medium transition-shadow focus:outline-none'
  const variants = {
    primary: 'bg-primary-500 text-white hover:bg-primary-700',
    secondary: 'bg-white border border-gray-200 text-gray-800',
    ghost: 'bg-transparent text-primary-500'
  } as const
  const cls = `${base} ${variants[variant]}`
  return (
    <button className={cls} {...rest}>
      {children}
    </button>
  )
}
