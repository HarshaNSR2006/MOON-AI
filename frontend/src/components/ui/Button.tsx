import React from 'react'

export type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'ghost' }

const Button: React.FC<ButtonProps> = ({ children, variant = 'primary', className = '', ...rest }) => {
  const base = 'px-4 py-2 rounded-md font-semibold transition'
  const style = variant === 'primary' ? 'bg-indigo-600 text-white hover:bg-indigo-500' : 'bg-transparent border'
  return (
    <button className={`${base} ${style} ${className}`} {...rest}>
      {children}
    </button>
  )
}

export default Button
