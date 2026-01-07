/**
 * API utilities for connecting to the Space Entropy Generator backend
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export interface RandomBytesResponse {
  bytes: string;
  length: number;
  format: string;
  entropy_score?: number;
  timestamp?: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  redis: Record<string, any>;
}

export interface StatsResponse {
  pool_bytes?: number;
  available_bytes?: number;
  entropy_blocks?: number;
  avg_shannon?: number;
  avg_quality_score?: number;
  last_validation?: string;
  last_refresh?: string;
}

export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string
  ) {
    super(`API Error ${status}: ${detail}`);
  }
}

/**
 * Fetch random bytes from the API
 */
export async function fetchRandomBytes(
  n: number,
  options?: RequestInit
): Promise<RandomBytesResponse> {
  if (n < 1 || n > 10240) {
    throw new ApiError(400, 'Number of bytes must be between 1 and 10240');
  }

  try {
    const response = await fetch(`${API_BASE}/random/${n}`, {
      method: 'GET',
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new ApiError(
        response.status,
        error.detail || response.statusText
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError(
      500,
      error instanceof Error ? error.message : 'Failed to fetch random bytes'
    );
  }
}

/**
 * Check service health
 */
export async function checkHealth(
  options?: RequestInit
): Promise<HealthResponse> {
  try {
    const response = await fetch(`${API_BASE}/health`, {
      method: 'GET',
      ...options,
    });

    if (!response.ok) {
      throw new ApiError(response.status, response.statusText);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError(
      500,
      error instanceof Error ? error.message : 'Failed to check health'
    );
  }
}

/**
 * Get pool statistics
 */
export async function fetchStats(
  options?: RequestInit
): Promise<StatsResponse> {
  try {
    const response = await fetch(`${API_BASE}/stats`, {
      method: 'GET',
      ...options,
    });

    if (!response.ok) {
      throw new ApiError(response.status, response.statusText);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError(
      500,
      error instanceof Error ? error.message : 'Failed to fetch stats'
    );
  }
}

/**
 * Get the API base URL (for debugging/display)
 */
export function getApiBaseUrl(): string {
  return API_BASE;
}
