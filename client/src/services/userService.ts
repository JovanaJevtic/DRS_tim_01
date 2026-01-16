import apiClient from '../api/api';
import type { User, ProfileUpdateData, ApiResponse } from '../types';

interface UserListResponse {
  success: boolean;
  users: User[];
  message?: string;
}

interface UserActionResponse {
  success: boolean;
  message: string;
}

interface UploadAvatarResponse {
  success: boolean;
  profileImage?: string;
  message: string;
}

const userService = {
  async getAllUsers(): Promise<UserListResponse> {
    try {
      const response = await apiClient.get<User[]>('/users');
      return {
        success: true,
        users: response.data,
      };
    } catch (error: any) {
      return {
        success: false,
        users: [],
        message: error.response?.data?.message || 'Greška pri učitavanju korisnika',
      };
    }
  },

  async updateUserRole(userId: number, uloga: string): Promise<UserActionResponse> {
    try {
      const response = await apiClient.patch<ApiResponse>(`/users/${userId}/role`, { uloga });
      return {
        success: response.data.success,
        message: 'Uloga uspešno promenjena',
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || 'Greška pri promeni uloge',
      };
    }
  },

  async deleteUser(userId: number): Promise<UserActionResponse> {
    try {
      const response = await apiClient.delete<ApiResponse>(`/users/${userId}`);
      return {
        success: response.data.success,
        message: 'Korisnik uspešno obrisan',
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || 'Greška pri brisanju korisnika',
      };
    }
  },

  async updateMyProfile(profileData: ProfileUpdateData): Promise<UserActionResponse> {
    try {
      const response = await apiClient.put<ApiResponse>('/users/me', profileData);
      return {
        success: response.data.success,
        message: response.data.message || 'Profil uspešno ažuriran',
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || 'Greška pri ažuriranju profila',
      };
    }
  },

  async uploadAvatar(file: File): Promise<UploadAvatarResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await apiClient.post<{ success: boolean; profile_image: string }>('/users/me/avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return {
        success: response.data.success,
        profileImage: response.data.profile_image,
        message: 'Slika uspešno postavljena',
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || 'Greška pri postavljanju slike',
      };
    }
  },

  async getMyProfile(): Promise<{ success: boolean; user?: User; message?: string }> {
    try {
      const response = await apiClient.get<{ success: boolean; user: User }>('/users/me');
      return {
        success: response.data.success,
        user: response.data.user,
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || 'Greška pri učitavanju profila',
      };
    }
  },
};

export default userService;