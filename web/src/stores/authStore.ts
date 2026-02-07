import { create } from "zustand";

type AuthState = {
  username: string | null;
  basicToken: string | null;
  setAuth: (username: string, basicToken: string) => void;
  clearAuth: () => void;
};

const STORAGE_KEY = "chemviz_auth";

function loadInitial(): { username: string | null; basicToken: string | null } {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { username: null, basicToken: null };
    const parsed = JSON.parse(raw) as { username?: unknown; basicToken?: unknown };
    if (typeof parsed.username !== "string" || typeof parsed.basicToken !== "string") {
      return { username: null, basicToken: null };
    }
    return { username: parsed.username, basicToken: parsed.basicToken };
  } catch {
    return { username: null, basicToken: null };
  }
}

const initial = loadInitial();

export const useAuthStore = create<AuthState>((set) => ({
  username: initial.username,
  basicToken: initial.basicToken,
  setAuth: (username, basicToken) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ username, basicToken }));
    set({ username, basicToken });
  },
  clearAuth: () => {
    localStorage.removeItem(STORAGE_KEY);
    set({ username: null, basicToken: null });
  },
}));

export function buildBasicToken(username: string, password: string): string {
  return btoa(`${username}:${password}`);
}

export function authHeaderFromToken(token: string | null): Record<string, string> {
  if (!token) return {};
  return { Authorization: `Basic ${token}` };
}
