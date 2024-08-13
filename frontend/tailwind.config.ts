import {nextui} from '@nextui-org/theme';
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
    "./node_modules/@nextui-org/react/dist/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
    },
  },
  darkMode: "class",
  plugins: [nextui(
    {
      addCommonColors: true,
      themes: {
        light: {
          colors: {
            background: "#F7FAFC",
            foreground: "#1A202C",
            primary: "#FF0000",
          },
        },
        dark: {
          colors: {
            background: "#1A202C",
            foreground: "#E2E8F0",
            primary: "#FF00FF",
          },
        },
      },
    }
  )],
};
export default config;
