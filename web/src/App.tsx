import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import RequireAuth from "@/components/RequireAuth";
import Dashboard from "@/pages/Dashboard";
import DatasetDetail from "@/pages/DatasetDetail";
import Home from "@/pages/Home";
import Login from "@/pages/Login";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <RequireAuth>
              <Dashboard />
            </RequireAuth>
          }
        />
        <Route
          path="/datasets/:id"
          element={
            <RequireAuth>
              <DatasetDetail />
            </RequireAuth>
          }
        />
      </Routes>
    </Router>
  );
}
