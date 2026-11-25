export type Role = "Admin" | "Annotator" | "Reviewer";

export interface Dataset {
  id: number;
  name: string;
  format: string;
  created_at: string;
}

export interface EvaluationTask {
  id: number;
  status: string;
  task_type: string;
  item?: {
    prompt: string;
    context?: string;
    response_a: string;
    response_b: string;
    category: string;
  };
}

export interface DashboardStats {
  datasets: number;
  tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  annotations: number;
  reviewed_tasks: number;
}
