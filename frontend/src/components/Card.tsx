import React from 'react'

export default function Card({ children, className = '' }: React.PropsWithChildren<{ className?: string }>) {
  return (
    <div className={`bg-white dark:bg-gray-800 shadow-sm rounded-2xl p-4 ${className}`}>
      {children}
    </div>
  )
}
