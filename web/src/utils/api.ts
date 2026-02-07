import { authHeaderFromToken, useAuthStore } from "@/stores/authStore";

const DEFAULT_BASE_URL = "http://127.0.0.1:8000/api";

export function getApiBaseUrl(): string {
  const fromEnv = import.meta.env.VITE_API_BASE_URL;
  if (typeof fromEnv === "string" && fromEnv.trim().length > 0) return fromEnv.trim();
  return DEFAULT_BASE_URL;
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const { basicToken, clearAuth } = useAuthStore.getState();
  const baseUrl = getApiBaseUrl();

  const res = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: {
      ...(init?.headers ?? {}),
      ...authHeaderFromToken(basicToken),
    },
  });

  if (res.status === 401) {
    clearAuth();
    throw new Error("Unauthorized");
  }

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `Request failed (${res.status})`);
  }

  return (await res.json()) as T;
}

export async function apiDownload(path: string): Promise<Blob> {
  const { basicToken, clearAuth } = useAuthStore.getState();
  const baseUrl = getApiBaseUrl();

  const res = await fetch(`${baseUrl}${path}`, {
    headers: {
      ...authHeaderFromToken(basicToken),
    },
  });

  if (res.status === 401) {
    clearAuth();
    throw new Error("Unauthorized");
  }

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `Request failed (${res.status})`);
  }

  return await res.blob();
}
