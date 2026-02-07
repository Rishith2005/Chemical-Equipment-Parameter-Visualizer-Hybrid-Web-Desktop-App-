import { LogOut } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { useAuthStore } from "@/stores/authStore";

export default function TopBar() {
  const username = useAuthStore((s) => s.username);
  const clearAuth = useAuthStore((s) => s.clearAuth);
  const navigate = useNavigate();

  return (
    <header className="border-b border-white/10 bg-slate-950/50">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/dashboard" className="font-semibold tracking-tight text-slate-100">
          Chemical Equipment Visualizer
        </Link>
        <div className="flex items-center gap-3">
          <div className="text-sm text-slate-300">{username ? `Signed in as ${username}` : ""}</div>
          <button
            type="button"
            onClick={() => {
              clearAuth();
              navigate("/login", { replace: true });
            }}
            className="inline-flex items-center gap-2 rounded-md border border-white/10 bg-white/5 px-3 py-2 text-sm text-slate-100 transition hover:bg-white/10"
          >
            <LogOut className="h-4 w-4" />
            Sign out
          </button>
        </div>
      </div>
    </header>
  );
}
