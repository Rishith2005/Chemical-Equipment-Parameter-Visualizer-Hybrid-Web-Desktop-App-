import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import PreviewTable from "@/components/PreviewTable";
import SummaryCards from "@/components/SummaryCards";
import TopBar from "@/components/TopBar";
import EquipmentMetricsLineChart from "@/components/EquipmentMetricsLineChart";
import TypeDistributionChart from "@/components/TypeDistributionChart";
import TypeDistributionBarChart from "@/components/TypeDistributionBarChart";
import type { PreviewResponse, SummaryAnalytics, SummaryResponse } from "@/types/api";
import { apiDownload, apiFetch } from "@/utils/api";

export default function DatasetDetail() {
  const { id } = useParams();
  const datasetId = id ?? "";

  const [summary, setSummary] = useState<SummaryAnalytics | null>(null);
  const [preview, setPreview] = useState<PreviewResponse["preview"] | null>(null);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      if (!datasetId) return;
      setLoading(true);
      setError(null);
      try {
        const s = await apiFetch<SummaryResponse>(`/datasets/${datasetId}/summary/`);
        setSummary(s.summary);
        const p = await apiFetch<PreviewResponse>(`/datasets/${datasetId}/preview/?limit=100`);
        setPreview(p.preview);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load dataset");
      } finally {
        setLoading(false);
      }
    }

    void load();
  }, [datasetId]);

  async function downloadPdf() {
    setDownloading(true);
    setError(null);
    try {
      const blob = await apiDownload(`/datasets/${datasetId}/report.pdf`);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `dataset_${datasetId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(e instanceof Error ? e.message : "PDF download failed");
    } finally {
      setDownloading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950">
      <TopBar />
      <main className="mx-auto max-w-6xl px-4 py-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="text-xs text-slate-400">
              <Link to="/dashboard" className="hover:text-slate-200">
                Dashboard
              </Link>
              <span className="px-2">/</span>
              <span className="text-slate-300">Dataset</span>
            </div>
            <div className="mt-1 text-lg font-semibold text-slate-100">Dataset details</div>
          </div>
          <button
            type="button"
            onClick={() => void downloadPdf()}
            disabled={downloading || !datasetId}
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:opacity-60"
          >
            {downloading ? "Generating…" : "Download PDF report"}
          </button>
        </div>

        {error ? <div className="mt-4 rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-200">{error}</div> : null}
        {loading ? <div className="mt-4 text-sm text-slate-400">Loading…</div> : null}

        {summary ? (
          <div className="mt-6 space-y-4">
            <SummaryCards summary={summary} />
            <div className="grid gap-4 lg:grid-cols-2">
              <TypeDistributionChart summary={summary} />
              <TypeDistributionBarChart summary={summary} />
            </div>
            <EquipmentMetricsLineChart preview={preview} />
            {preview ? <PreviewTable preview={preview} /> : <div className="rounded-xl border border-white/10 bg-white/5 p-4" />}
          </div>
        ) : null}
      </main>
    </div>
  );
}
