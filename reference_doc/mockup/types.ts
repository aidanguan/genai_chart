export interface Stage {
  name: string;
  description: string;
  value: string; // Descriptive value, e.g. "Market Share 15%"
  color: string; // Hex code
}

export interface InfographicData {
  title: string;
  subtitle: string;
  stages: Stage[];
}

export interface HistoryItem {
  id: string;
  title: string;
  preview: string;
  timestamp: number;
}
