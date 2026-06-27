"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/",          label: "Home"      },
  { href: "/translate", label: "Translate" },
  { href: "/validate",  label: "Validate"  },
  { href: "/vocab",     label: "Vocab"     },
];


export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/90 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-6xl items-center gap-8 px-6">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-violet-400 font-bold text-lg tracking-widest sigan">◈</span>
          <span className="font-semibold tracking-wide text-slate-100">SIGAN</span>
        </Link>

        <div className="flex items-center gap-1 ml-4">
          {links.map(({ href, label }) => {
            const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  active
                    ? "bg-violet-500/15 text-violet-300"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                }`}
              >
                {label}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
