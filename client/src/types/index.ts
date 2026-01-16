// User types
export interface User {
  id: number;
  email: string;
  uloga: UserRole;
  ime?: string;
  prezime?: string;
  imePrezime?: string;
  datum_rodjenja?: string;
  pol?: Gender;
  drzava?: string;
  ulica?: string;
  broj?: string;
  profile_image?: string;
}

export type UserRole = 'IGRAC' | 'MODERATOR' | 'ADMINISTRATOR';
export type Gender = 'M' | 'Z' | 'O';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  ime: string;
  prezime: string;
  email: string;
  password: string;
  datum_rodjenja?: string;
  pol?: Gender;
  drzava?: string;
  ulica?: string;
  broj?: string;
}

export interface AuthResponse {
  success: boolean;
  token?: string;
  message?: string;
  user_id?: number;
}

export interface DecodedToken {
  id: number;
  email: string;
  uloga: UserRole;
  exp: number;
}

export interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
}

export interface ProfileUpdateData {
  ime?: string;
  prezime?: string;
  datum_rodjenja?: string;
  pol?: Gender;
  drzava?: string;
  ulica?: string;
  broj?: string;
}

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface ToastMessage {
  id: number;
  message: string;
  type: ToastType;
  duration: number;
}