import React from 'react'
import { BrandLogo } from './brandLogo'
import { BrandText } from './brandText'

interface BrandProps {
    className?: string;      
}

export default function Brand({className} : BrandProps) {
  return (
    <div className={"flex justify-center items-center " + className}>
        <BrandLogo />
        <BrandText />
    </div>
  )
}
