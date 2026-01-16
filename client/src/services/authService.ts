import { jwtDecode } from 'jwt-decode';
import type { RegisterData, AuthResponse, DecodedToken } from '../types';
import apiClient from '../api/api';

const authService = {
  async login(email: string, password: string): Promise<AuthResponse & { user?: DecodedToken }> {
    try {
      const response = await apiClient.post<AuthResponse>('/auth/login', {
        email,
        password,
      });

      if (response.data.success && response.data.token) {
        const token = response.data.token;
        const decoded = jwtDecode<DecodedToken>(token);
        
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify({
          id: decoded.id,
          email: decoded.email,
          uloga: decoded.uloga,
        }));

        return { success: true, token, user: decoded };
      }
      
      return { success: false, message: response.data.message };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || 'Greška pri prijavljivanju',
      };
    }
  },

  async register(userData: RegisterData): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>('/auth/register', userData);
      return {
        success: response.data.success,
        message: response.data.success ? 'Uspešna registracija!' : response.data.message,
        user_id: response.data.user_id,
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || 'Greška pri registraciji',
      };
    }
  },

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getCurrentUser(): DecodedToken | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  },

  isAuthenticated(): boolean {
    const token = localStorage.getItem('token');
    if (!token) return false;

    try {
      const decoded = jwtDecode<DecodedToken>(token);
      if (decoded.exp * 1000 < Date.now()) {
        this.logout();
        return false;
      }
      return true;
    } catch {
      return false;
    }
  },

  getToken(): string | null {
    return localStorage.getItem('token');
  },
};

export default authService;