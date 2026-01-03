import type { UserRole, Gender } from '../types';

/**
 * Konstante korišćene širom aplikacije
 */

export const USER_ROLES: Record<string, UserRole> = {
  IGRAC: 'IGRAC',
  MODERATOR: 'MODERATOR',
  ADMINISTRATOR: 'ADMINISTRATOR',
};

export const USER_ROLES_DISPLAY: Record<UserRole, string> = {
  IGRAC: 'Igrač',
  MODERATOR: 'Moderator',
  ADMINISTRATOR: 'Administrator',
};

export const GENDERS: Record<Gender, string> = {
  M: 'Muški',
  Z: 'Ženski',
  O: 'Drugo',
};

export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  
  // Users
  USERS: '/users',
  MY_PROFILE: '/users/me',
  MY_AVATAR: '/users/me/avatar',
  USER_ROLE: (id: number) => `/users/${id}/role`,
  USER_DELETE: (id: number) => `/users/${id}`,
};

export const STORAGE_KEYS = {
  TOKEN: 'token',
  USER: 'user',
};

export const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
export const MAX_IMAGE_SIZE_MB = 5;

export const TOAST_DURATION = 3000;

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  PROFILE: '/profile',
  ADMIN_USERS: '/admin/users',
  KVIZOVI: '/kvizovi',
  DOSTUPNI_KVIZOVI: '/kvizovi/dostupni',
  REZULTATI: '/rezultati',
};