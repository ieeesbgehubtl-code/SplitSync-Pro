import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";
import { Plane, Users, Receipt, Bell, BarChart3, Settings } from "lucide-react";
const links = [
  ["/dashboard", "Dashboard", BarChart3],
  ["/trips", "Trips", Plane],
  ["/friends", "Friends", Users],
  ["/expenses", "Expenses", Receipt],
  ["/notifications", "Notifications", Bell],
  ["/settings", "Settings", Settings],
] as const;
export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-indigo-50 to-cyan-50 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950">
      <aside className="fixed inset-y-0 hidden w-64 p-4 md:block">
        <div className="glass h-full rounded-3xl p-4">
          <h1 className="mb-8 text-2xl font-black">TripSplit</h1>
          <nav className="space-y-2">
            {links.map(([to, label, Icon]) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-2xl px-4 py-3 ${isActive ? "bg-indigo-600 text-white" : "hover:bg-white/60 dark:hover:bg-slate-800"}`
                }
              >
                <Icon size={18} />
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      </aside>
      <main className="p-4 md:ml-64">
        <div className="mx-auto max-w-7xl">{children}</div>
      </main>
    </div>
  );
}
