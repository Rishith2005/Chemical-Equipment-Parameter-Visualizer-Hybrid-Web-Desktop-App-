import type React from "react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { buildBasicToken, useAuthStore } from "@/stores/authStore";
import { getApiBaseUrl } from "@/utils/api";

export default function Login() {
  const navigate = useNavigate();
  const setAuth = useAuthStore((s) => s.setAuth);
  const existingToken = useAuthStore((s) => s.basicToken);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (existingToken) navigate("/dashboard", { replace: true });
  }, [existingToken, navigate]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const token = buildBasicToken(username, password);
      const baseUrl = getApiBaseUrl();
      const res = await fetch(`${baseUrl}/me/`, {
        headers: {
          Authorization: `Basic ${token}`,
        },
      });

      if (!res.ok) {
        throw new Error("Invalid credentials");
      }

      setAuth(username, token);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="mx-auto flex min-h-screen max-w-6xl items-center justify-center px-4">
        <div className="w-full max-w-md rounded-2xl border border-white/10 bg-white/5 p-6">
          <div className="text-lg font-semibold text-slate-100">Sign in</div>
          <div className="mt-1 text-sm text-slate-400">Use your Django Basic Auth username/password.</div>

          <form onSubmit={onSubmit} className="mt-6 space-y-4">
            <div>
              <label htmlFor="username" className="text-xs font-medium text-slate-300">
                Username
              </label>
              <input
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="mt-1 w-full rounded-md border border-white/10 bg-slate-950/50 px-3 py-2 text-slate-100 outline-none ring-0 focus:border-blue-500"
                autoComplete="username"
                placeholder="Enter username"
                required
              />
            </div>
            <div>
              <label htmlFor="password" className="text-xs font-medium text-slate-300">
                Password
              </label>
              <input
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                className="mt-1 w-full rounded-md border border-white/10 bg-slate-950/50 px-3 py-2 text-slate-100 outline-none ring-0 focus:border-blue-500"
                autoComplete="current-password"
                placeholder="Enter password"
                required
              />
            </div>

            {error ? <div className="rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-200">{error}</div> : null}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-md bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-500 disabled:opacity-60"
            >
              {loading ? "Signing in…" : "Sign in"}
            </button>
          </form>

          <div className="mt-6 text-xs text-slate-400">
            Default demo: <span className="text-slate-200">demo</span> / <span className="text-slate-200">demo1234</span>
          </div>
        </div>
      </div>
    </div>
  );
}
