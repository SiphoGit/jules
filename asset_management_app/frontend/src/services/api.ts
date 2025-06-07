// Defines the base URL for the API.
// Adjust this if your backend runs on a different port or host.
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// --- Reusable utility for fetching data ---
async function fetchAPI<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultHeaders = {
        'Content-Type': 'application/json',
        // Add other default headers here if needed, like Authorization
    };
    options.headers = { ...defaultHeaders, ...options.headers };

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            // Attempt to parse error details from the backend
            const errorData = await response.json().catch(() => ({ detail: 'Unknown error structure' }));
            console.error(`API Error (${response.status}): ${errorData.detail || response.statusText}`, errorData);
            throw new Error(`API request failed: ${errorData.detail || response.statusText}`);
        }
        // Handle cases where the response might be empty (e.g., 204 No Content)
        if (response.status === 204) {
            return null as T;
        }
        return response.json() as T;
    } catch (error) {
        console.error('Network or other error:', error);
        throw error; // Re-throw the error to be caught by the caller
    }
}

// --- Pydantic Models mirrored in TypeScript ---
// These should ideally be kept in sync with your backend models.py
// Consider using tools like openapi-typescript-codegen in a real project.

export enum RiskProfile {
    LOW = "low",
    MEDIUM = "medium",
    HIGH = "high",
}

export enum MarketTrend {
    BULLISH = "bullish",
    BEARISH = "bearish",
    NEUTRAL = "neutral",
}

export interface Asset {
    id: number;
    name: string;
    ticker_symbol: string;
    asset_type: string;
    current_price: number;
}

export interface AssetCreate extends Omit<Asset, 'id'> {}

export interface PortfolioAsset {
    asset_id: number;
    quantity: number;
}

export interface Portfolio {
    id: number;
    name: string;
    client_id: number;
    assets: PortfolioAsset[]; // List of asset IDs and quantities
    total_value?: number;
}

export interface PortfolioCreate {
    name:string;
    assets: PortfolioAsset[];
}

export interface Client {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    risk_profile: RiskProfile;
    portfolios: Portfolio[]; // Full portfolio objects
}

export interface ClientCreate extends Omit<Client, 'id' | 'portfolios'> {
    // Portfolios are typically created/managed separately or as part of client creation if API supports
}

export interface RecommendedAsset extends Asset {
    suitability_score?: number;
    rationale?: string;
}

export interface RecommendationRequest {
    // client_id is part of the path, not body for this specific endpoint
    market_trend: MarketTrend;
}

// For the detailed portfolio response from GET /clients/{client_id}/portfolio
// Corresponds to PortfolioDetailsResponse in main.py
export interface PortfolioDetailsResponse {
    id: number;
    name: string;
    client_id: number;
    assets_details: RecommendedAsset[]; // Uses RecommendedAsset structure for assets
    total_value: number;
}


// --- Client Endpoints ---
export const createClient = (clientData: ClientCreate): Promise<Client> => {
    return fetchAPI<Client>('/clients/', {
        method: 'POST',
        body: JSON.stringify(clientData),
    });
};

export const getClients = (): Promise<Client[]> => {
    return fetchAPI<Client[]>('/clients/');
};

export const getClientById = (clientId: number): Promise<Client> => {
    return fetchAPI<Client>(`/clients/${clientId}`);
};

export const updateClient = (clientId: number, clientData: ClientCreate): Promise<Client> => {
    return fetchAPI<Client>(`/clients/${clientId}`, {
        method: 'PUT',
        body: JSON.stringify(clientData),
    });
};

export const deleteClient = (clientId: number): Promise<Client> => {
    return fetchAPI<Client>(`/clients/${clientId}`, {
        method: 'DELETE',
    });
};

// --- Asset Endpoints ---
export const createAsset = (assetData: AssetCreate): Promise<Asset> => {
    return fetchAPI<Asset>('/assets/', {
        method: 'POST',
        body: JSON.stringify(assetData),
    });
};

export const getAssets = (): Promise<Asset[]> => {
    return fetchAPI<Asset[]>('/assets/');
};

export const getAssetById = (assetId: number): Promise<Asset> => {
    return fetchAPI<Asset>(`/assets/${assetId}`);
};

// --- Portfolio Endpoints ---
export const createOrUpdateClientPortfolio = (clientId: number, portfolioData: PortfolioCreate): Promise<Portfolio> => {
    return fetchAPI<Portfolio>(`/clients/${clientId}/portfolio`, {
        method: 'POST',
        body: JSON.stringify(portfolioData),
    });
};

export const getClientPortfolio = (clientId: number): Promise<PortfolioDetailsResponse> => {
    return fetchAPI<PortfolioDetailsResponse>(`/clients/${clientId}/portfolio`);
};

// --- AI Recommendation Endpoints ---
export const getRecommendations = (clientId: number, requestData: RecommendationRequest): Promise<RecommendedAsset[]> => {
    return fetchAPI<RecommendedAsset[]>(`/clients/${clientId}/recommendations`, {
        method: 'POST',
        body: JSON.stringify(requestData),
    });
};
