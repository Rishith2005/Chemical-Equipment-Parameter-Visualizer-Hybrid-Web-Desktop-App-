import type { SummaryAnalytics } from "@/types/api";

function Card({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-4">
      <div className="text-xs uppercase tracking-wide text-slate-400">{label}</div>
      <div className="mt-1 text-lg font-semibold text-slate-100">{value}</div>
    </div>
  );
}

export default function SummaryCards({ summary }: { summary: SummaryAnalytics }) {
  const avg = summary.averages ?? {};
  const format = (v: unknown) => (typeof v === "number" && Number.isFinite(v) ? v.toFixed(2) : "-");

  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
      <Card label="Total Count" value={`${summary.total_count ?? 0}`} />
      <Card label="Avg Flowrate" value={format(avg.Flowrate)} />
      <Card label="Avg Pressure" value={format(avg.Pressure)} />
      <Card label="Avg Temperature" value={format(avg.Temperature)} />
    </div>
  );
}
