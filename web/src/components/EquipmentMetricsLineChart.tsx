import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";

import type { PreviewResponse } from "@/types/api";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

function toNumber(v: unknown): number | null {
  if (typeof v === "number" && Number.isFinite(v)) return v;
  if (typeof v === "string") {
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  }
  return null;
}

export default function EquipmentMetricsLineChart({
  preview,
}: {
  preview: PreviewResponse["preview"] | null;
}) {
  const rows = preview?.rows ?? [];
  const labels = rows.map((r, i) => {
    const name = r["Equipment Name"];
    if (typeof name === "string" && name.trim()) return name;
    return `Row ${i + 1}`;
  });

  const flow = rows.map((r) => toNumber(r.Flowrate));
  const pressure = rows.map((r) => toNumber(r.Pressure));
  const temperature = rows.map((r) => toNumber(r.Temperature));

  const hasAny = [...flow, ...pressure, ...temperature].some((v) => v !== null);

  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-4">
      <div className="mb-3 text-sm font-semibold text-slate-100">Flowrate / Pressure / Temperature (Line)</div>
      {!preview ? (
        <div className="text-sm text-slate-400">Upload and select a dataset to view this chart.</div>
      ) : !hasAny ? (
        <div className="text-sm text-slate-400">No numeric Flowrate/Pressure/Temperature values found in preview.</div>
      ) : (
        <Line
          data={{
            labels,
            datasets: [
              {
                label: "Flowrate",
                data: flow,
                borderColor: "#3B82F6",
                backgroundColor: "rgba(59,130,246,0.25)",
                pointRadius: 2,
                tension: 0.25,
                spanGaps: true,
              },
              {
                label: "Pressure",
                data: pressure,
                borderColor: "#22C55E",
                backgroundColor: "rgba(34,197,94,0.25)",
                pointRadius: 2,
                tension: 0.25,
                spanGaps: true,
              },
              {
                label: "Temperature",
                data: temperature,
                borderColor: "#F59E0B",
                backgroundColor: "rgba(245,158,11,0.25)",
                pointRadius: 2,
                tension: 0.25,
                spanGaps: true,
              },
            ],
          }}
          options={{
            responsive: true,
            plugins: {
              legend: { labels: { color: "#CBD5E1" } },
              tooltip: { enabled: true },
            },
            scales: {
              x: { ticks: { color: "#94A3B8" }, grid: { color: "rgba(148,163,184,0.1)" } },
              y: { ticks: { color: "#94A3B8" }, grid: { color: "rgba(148,163,184,0.1)" } },
            },
          }}
        />
      )}
    </div>
  );
}

