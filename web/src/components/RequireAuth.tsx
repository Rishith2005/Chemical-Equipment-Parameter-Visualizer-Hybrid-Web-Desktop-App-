import type React from "react";
import { useAuthStore } from "@/stores/authStore";
import { Navigate, useLocation } from "react-router-dom";

export default function RequireAuth({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((s) => s.basicToken);
  const location = useLocation();

  if (!token) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <>{children}</>;
}
