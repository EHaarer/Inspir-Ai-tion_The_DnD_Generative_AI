import { Inter } from "next/font/google";
import "./globals.css";
import Nav from "./components/nav";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout(
  {children}: Readonly<{children: React.ReactNode;}>
  ) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {/* Nav Bar */}
        <Nav>
          {children}
        </Nav>
      </body>
    </html>
  );
}
