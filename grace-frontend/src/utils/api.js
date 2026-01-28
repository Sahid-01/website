import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // Django backend URL
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ============================================
// COMMON APIs
// ============================================

// Get site configuration (country, branch info)
export const getSiteConfig = () => api.get("/site-config/");

// ============================================
// LOCATION APIs
// ============================================

// Get all active countries
export const getCountries = () => api.get("/countries/");

// Get branches (optionally filter by country code)
export const getBranches = (countryCode = null) => {
  const params = countryCode ? { country: countryCode } : {};
  return api.get("/branches/", { params });
};

// ============================================
// PAGE APIs
// ============================================

// Get page metadata by slug
export const getPage = (slug) => api.get(`/${slug}/`);

// Admin: Create new page (requires authentication)
export const createPage = (pageData) => api.post("/admin/create/", pageData);

// Admin: Update page (requires authentication)
export const updatePage = (pageId, pageData) =>
  api.put(`/admin/update/${pageId}/`, pageData);

// Admin: Delete page (requires authentication)
export const deletePage = (pageId) => api.delete(`/admin/delete/${pageId}/`);

// ============================================
// CONTENT APIs
// ============================================

// Get page content with sections and items
export const getPageContent = (slug) => api.get(`/${slug}/`);

// ============================================
// AUTH APIs
// ============================================

// Login user
export const login = (username, password) =>
  api.post("/login/", { username, password });

// Register new user (Admin only)
export const registerUser = (userData) => api.post("/register/", userData);

// Get list of users (Admin only)
export const getUsers = () => api.get("/list/");

// ============================================
// HELPER FUNCTIONS
// ============================================

// Save auth token
export const setAuthToken = (token) => {
  localStorage.setItem("token", token);
};

// Remove auth token
export const removeAuthToken = () => {
  localStorage.removeItem("token");
};

// Get current auth token
export const getAuthToken = () => {
  return localStorage.getItem("token");
};

export default api;
