import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "WildSense | Look closer. Then look away.",
  description: "Offline-first AI nature exploration companion that gets you off the screen.",
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark h-full">
      <body className="min-h-full flex flex-col bg-[#0b110d] text-[#f2f5f1]">
        {children}
      </body>
    </html>
  );
}
