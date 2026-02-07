import { ArcElement, Legend, Tooltip, Chart as ChartJS } from "chart.js";
import { Pie } from "react-chartjs-2";

import type { SummaryAnalytics } from "@/types/api";

ChartJS.register(ArcElement, Tooltip, Legend);

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

export default function TypeDistributionChart({ summary }: { summary: SummaryAnalytics }) {
  const dist = summary.type_distribution ?? {};
  const labels = Object.keys(dist);
  const values = labels.map((k) => dist[k] ?? 0);

  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-4">
      <div className="mb-3 text-sm font-semibold text-slate-100">Equipment Type Distribution</div>
      {labels.length === 0 ? (
        <div className="text-sm text-slate-400">No distribution data available.</div>
      ) : (
        <Pie
          data={{
            labels,
            datasets: [
              {
                data: values,
                backgroundColor: labels.map((_, i) => COLORS[i % COLORS.length]),
                borderColor: "rgba(255,255,255,0.15)",
                borderWidth: 1,
              },
            ],
          }}
          options={{
            plugins: {
              legend: {
                position: "right",
                labels: { color: "#CBD5E1" },
              },
            },
          }}
        />
      )}
    </div>
  );
}
