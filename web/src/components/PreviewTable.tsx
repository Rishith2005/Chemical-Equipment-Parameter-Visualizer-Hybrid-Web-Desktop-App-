import type { PreviewResponse } from "@/types/api";

export default function PreviewTable({ preview }: { preview: PreviewResponse["preview"] }) {
  const columns = preview.columns;
  const rows = preview.rows;

  return (
    <div className="overflow-hidden rounded-xl border border-white/10 bg-white/5">
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
        <div className="text-sm font-semibold text-slate-100">Preview</div>
        <div className="text-xs text-slate-400">
          Showing {preview.returned} of {preview.limit}
        </div>
      </div>
      <div className="max-h-80 overflow-auto">
        <table className="w-full border-collapse text-left text-sm">
          <thead className="sticky top-0 bg-slate-950/80 backdrop-blur">
            <tr>
              {columns.map((c) => (
                <th key={c} className="whitespace-nowrap border-b border-white/10 px-4 py-2 text-xs font-semibold text-slate-300">
                  {c}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, idx) => (
              <tr key={idx} className={idx % 2 === 0 ? "bg-white/0" : "bg-white/5"}>
                {columns.map((c) => (
                  <td key={c} className="whitespace-nowrap border-b border-white/5 px-4 py-2 text-slate-200">
                    {String((r as Record<string, unknown>)[c] ?? "")}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
