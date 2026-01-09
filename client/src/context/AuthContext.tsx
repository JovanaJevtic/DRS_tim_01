import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import authService from '../services/authService';
import websocketService from '../services/websocketService'; 
import type { DecodedToken, RegisterData } from '../types';

interface AuthContextType {
  user: DecodedToken | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; message?: string }>;
  register: (userData: RegisterData) => Promise<{ success: boolean; message?: string; userId?: number }>;
  logout: () => void;
  updateUser: (updatedUserData: Partial<DecodedToken>) => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<DecodedToken | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

 useEffect(() => {
    // Provera da li je korisnik već prijavljen
    const initAuth = () => {
      if (authService.isAuthenticated()) {
        const currentUser = authService.getCurrentUser();
        setUser(currentUser);
        setIsAuthenticated(true);
        
        // Konektuj WebSocket ako je korisnik već prijavljen - DODAJ OVO
        if (currentUser) {
          websocketService.connect(currentUser.id);
          
          websocketService.onRoleChanged((data) => {
            console.log('🔔 Uloga promenjena:', data);
            const updatedUser = { ...currentUser, uloga: data.new_role as any };
            setUser(updatedUser);
            localStorage.setItem('user', JSON.stringify(updatedUser));
            alert(data.message);
          });
        }
      }
      setLoading(false);
    };

    initAuth();
    
    return () => {
      websocketService.off('role_changed');
    };
  }, []);

  const login = async (email: string, password: string) => {
    const result = await authService.login(email, password);

    if (result.success && result.user) {
      setUser(result.user);
      setIsAuthenticated(true);

      websocketService.connect(result.user.id);

      websocketService.onRoleChanged((data) => {
        console.log('🔔 Uloga promenjena:', data);
        const updatedUser = { ...result.user!, uloga: data.new_role as any };
        setUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));
        alert(data.message);
      });
    }

    return result;
  
};


  const register = async (userData: RegisterData) => {
    return await authService.register(userData);
  };

  const logout = () => {
    authService.logout();
    websocketService.disconnect();
    setUser(null);
    setIsAuthenticated(false);
  };

  const updateUser = (updatedUserData: Partial<DecodedToken>) => {
    const updatedUser = { ...user, ...updatedUserData } as DecodedToken;
    setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify(updatedUser));
  };

  const value: AuthContextType = {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth mora biti korišćen unutar AuthProvider');
  }
  return context;
};

export default AuthContext;