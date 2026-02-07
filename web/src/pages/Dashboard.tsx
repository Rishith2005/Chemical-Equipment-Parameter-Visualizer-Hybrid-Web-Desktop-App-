import { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import PreviewTable from "@/components/PreviewTable";
import SummaryCards from "@/components/SummaryCards";
import TopBar from "@/components/TopBar";
import EquipmentMetricsLineChart from "@/components/EquipmentMetricsLineChart";
import TypeDistributionChart from "@/components/TypeDistributionChart";
import TypeDistributionBarChart from "@/components/TypeDistributionBarChart";
import type { Dataset, DatasetListResponse, PreviewResponse, SummaryAnalytics, SummaryResponse, UploadResponse } from "@/types/api";
import { apiFetch } from "@/utils/api";

export default function Dashboard() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const [summary, setSummary] = useState<SummaryAnalytics | null>(null);
  const [preview, setPreview] = useState<PreviewResponse["preview"] | null>(null);

  const [loadingList, setLoadingList] = useState(false);
  const [loadingDataset, setLoadingDataset] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selected = useMemo(() => datasets.find((d) => d.id === selectedId) ?? null, [datasets, selectedId]);

  const loadDatasets = useCallback(async (preserveSelection = true) => {
    setLoadingList(true);
    setError(null);
    try {
      const res = await apiFetch<DatasetListResponse>("/datasets/?limit=5");
      setDatasets(res.items);
      if (!preserveSelection) {
        setSelectedId(res.items[0]?.id ?? null);
      } else {
        const stillExists = res.items.some((d) => d.id === selectedId);
        if (!stillExists) setSelectedId(res.items[0]?.id ?? null);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load datasets");
    } finally {
      setLoadingList(false);
    }
  }, [selectedId]);

  async function loadSelected(id: string) {
    setLoadingDataset(true);
    setError(null);
    setSummary(null);
    setPreview(null);
    try {
      const s = await apiFetch<SummaryResponse>(`/datasets/${id}/summary/`);
      setSummary(s.summary);
      const p = await apiFetch<PreviewResponse>(`/datasets/${id}/preview/?limit=50`);
      setPreview(p.preview);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load dataset");
    } finally {
      setLoadingDataset(false);
    }
  }

  useEffect(() => {
    void loadDatasets(false);
  }, [loadDatasets]);

  useEffect(() => {
    if (selectedId) loadSelected(selectedId);
  }, [selectedId]);

  async function onUpload(file: File) {
    setUploading(true);
    setError(null);
    try {
      const form = new FormData();
      form.append("file", file);

      const res = await apiFetch<UploadResponse>("/datasets/upload/", {
        method: "POST",
        body: form,
      });

      await loadDatasets(false);
      setSelectedId(res.dataset.id);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950">
      <TopBar />
      <main className="mx-auto max-w-6xl px-4 py-6">
        <div className="grid gap-6 lg:grid-cols-[420px_1fr]">
          <section className="space-y-6">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="text-sm font-semibold text-slate-100">Upload CSV</div>
              <div className="mt-1 text-xs text-slate-400">CSV must include: Equipment Name, Type, Flowrate, Pressure, Temperature</div>

              <div className="mt-4 flex items-center gap-3">
                <label htmlFor="csv-upload" className="sr-only">
                  Upload CSV file
                </label>
                <input
                  id="csv-upload"
                  type="file"
                  accept=".csv,text/csv"
                  title="Upload CSV"
                  disabled={uploading}
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    if (f) void onUpload(f);
                    e.currentTarget.value = "";
                  }}
                  className="block w-full text-sm text-slate-200 file:mr-4 file:rounded-md file:border-0 file:bg-blue-600 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-blue-500"
                />
              </div>
              {uploading ? <div className="mt-3 text-sm text-slate-300">Uploading and processing…</div> : null}
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="flex items-center justify-between">
                <div className="text-sm font-semibold text-slate-100">Recent datasets (last 5)</div>
                <button
                  type="button"
                  onClick={() => loadDatasets(true)}
                  disabled={loadingList}
                  className="rounded-md border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-slate-200 hover:bg-white/10 disabled:opacity-60"
                >
                  Refresh
                </button>
              </div>

              <div className="mt-3 space-y-2">
                {loadingList ? <div className="text-sm text-slate-400">Loading…</div> : null}
                {!loadingList && datasets.length === 0 ? (
                  <div className="text-sm text-slate-400">No datasets yet. Upload a CSV to begin.</div>
                ) : null}
                {datasets.map((d) => (
                  <button
                    key={d.id}
                    type="button"
                    onClick={() => setSelectedId(d.id)}
                    className={
                      d.id === selectedId
                        ? "w-full rounded-xl border border-blue-500/40 bg-blue-500/10 px-3 py-2 text-left"
                        : "w-full rounded-xl border border-white/10 bg-white/0 px-3 py-2 text-left hover:bg-white/5"
                    }
                  >
                    <div className="flex items-center justify-between gap-3">
                      <div className="min-w-0">
                        <div className="truncate text-sm font-medium text-slate-100">{d.filename}</div>
                        <div className="mt-0.5 text-xs text-slate-400">{new Date(d.uploaded_at).toLocaleString()}</div>
                      </div>
                      <div className="shrink-0 rounded-full border border-white/10 bg-white/5 px-2 py-1 text-xs text-slate-200">
                        {d.status}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </section>

          <section className="space-y-6">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-semibold text-slate-100">Summary analytics</div>
                  <div className="mt-1 text-xs text-slate-400">Select a dataset to view charts and a preview table.</div>
                </div>
                {selected ? (
                  <Link
                    to={`/datasets/${selected.id}`}
                    className="rounded-md border border-white/10 bg-white/5 px-3 py-2 text-xs font-medium text-slate-100 hover:bg-white/10"
                  >
                    Open details
                  </Link>
                ) : null}
              </div>

              {error ? <div className="mt-4 rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-200">{error}</div> : null}

              {!selected ? <div className="mt-4 text-sm text-slate-400">No dataset selected.</div> : null}

              {selected && selected.status !== "ready" ? (
                <div className="mt-4 text-sm text-slate-300">Status: {selected.status}</div>
              ) : null}

              {loadingDataset ? <div className="mt-4 text-sm text-slate-400">Loading analytics…</div> : null}

              {summary && selected?.status === "ready" ? (
                <div className="mt-4 space-y-4">
                  <SummaryCards summary={summary} />
                  <div className="grid gap-4 lg:grid-cols-2">
                    <TypeDistributionChart summary={summary} />
                    <TypeDistributionBarChart summary={summary} />
                  </div>
                  <EquipmentMetricsLineChart preview={preview} />
                  {preview ? <PreviewTable preview={preview} /> : <div className="rounded-xl border border-white/10 bg-white/5 p-4" />}
                </div>
              ) : null}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
