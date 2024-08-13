"use client";
import { BrandLogo } from "./components/brand/brandLogo";
import { BrandText } from "./components/brand/brandText";

import RequestExample from "./components/requestExample";

import { Tooltip, useDisclosure } from "@nextui-org/react";
import { motion } from "framer-motion";


export default function Home() {
  const {isOpen, onOpen, onOpenChange} = useDisclosure();
  

  return (
    <div className="flex flex-col items-center justify-center py-2">
      <Tooltip content="Click me to see how HTML requests work" offset={-60} closeDelay={40}>
        <motion.div
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={onOpen}
        >
          <BrandLogo size={400} className="text-primary"/>
        </motion.div>
      </Tooltip>
      
      <h1 className="text-6xl font-bold">
        DB_Name: {process.env.DB_NAME}{" "}
        <BrandText />
      </h1>
      <RequestExample modalOpen={isOpen} onModalChange={onOpenChange}/>
    </div>
  );
}
