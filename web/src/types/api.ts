export type DatasetStatus = "uploaded" | "processing" | "ready" | "error";

export type Dataset = {
  id: string;
  filename: string;
  status: DatasetStatus;
  row_count: number | null;
  column_count: number | null;
  uploaded_at: string;
};

export type SummaryAnalytics = {
  total_count: number;
  averages: Record<string, number | null>;
  type_distribution: Record<string, number>;
};

export type DatasetListResponse = { items: Dataset[] };

export type UploadResponse = {
  dataset: Dataset;
  summary: SummaryAnalytics;
};

export type SummaryResponse = {
  dataset: Dataset;
  summary: SummaryAnalytics;
};

export type PreviewResponse = {
  dataset: Dataset;
  preview: {
    columns: string[];
    rows: Record<string, unknown>[];
    limit: number;
    returned: number;
  };
};
