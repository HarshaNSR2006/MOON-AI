import React from 'react'

const Input = (props: React.InputHTMLAttributes<HTMLInputElement>) => {
  return <input className="w-full border rounded px-3 py-2" {...props} />
}

export default Input
