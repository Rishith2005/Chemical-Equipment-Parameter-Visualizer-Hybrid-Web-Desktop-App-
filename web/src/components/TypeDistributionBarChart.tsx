import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Tooltip } from "chart.js";
import { Bar } from "react-chartjs-2";

import type { SummaryAnalytics } from "@/types/api";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const COLORS = [
  "#3B82F6",
  "#22C55E",
  "#F59E0B",
  "#EF4444",
  "#A855F7",
  "#06B6D4",
  "#F97316",
  "#84CC16",
];

export default function TypeDistributionBarChart({ summary }: { summary: SummaryAnalytics }) {
  const dist = summary.type_distribution ?? {};
  const labels = Object.keys(dist);
  const values = labels.map((k) => dist[k] ?? 0);

  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-4">
      <div className="mb-3 text-sm font-semibold text-slate-100">Equipment Type Distribution (Bar)</div>
      {labels.length === 0 ? (
        <div className="text-sm text-slate-400">No distribution data available.</div>
      ) : (
        <Bar
          data={{
            labels,
            datasets: [
              {
                label: "Count",
                data: values,
                backgroundColor: labels.map((_, i) => COLORS[i % COLORS.length]),
                borderColor: "rgba(255,255,255,0.15)",
                borderWidth: 1,
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
              y: {
                ticks: { color: "#94A3B8", precision: 0 },
                grid: { color: "rgba(148,163,184,0.1)" },
                beginAtZero: true,
              },
            },
          }}
        />
      )}
    </div>
  );
}

