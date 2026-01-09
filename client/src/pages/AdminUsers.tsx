import { useState, useEffect } from 'react';
import userService from '../services/userService';
import type { User, UserRole } from '../types';

const AdminUsers = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string }>({ type: 'success', text: '' });
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [showRoleModal, setShowRoleModal] = useState(false);
  const [newRole, setNewRole] = useState<UserRole>('IGRAC');

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    setLoading(true);
    const result = await userService.getAllUsers();
    
    if (result.success) {
      setUsers(result.users);
    } else {
      setMessage({ type: 'error', text: result.message || 'Greška' });
    }
    setLoading(false);
  };

  const handleDeleteUser = async (userId: number) => {
    if (!window.confirm('Da li ste sigurni da želite da obrišete ovog korisnika?')) {
      return;
    }

    const result = await userService.deleteUser(userId);
    
    if (result.success) {
      setMessage({ type: 'success', text: result.message });
      loadUsers();
    } else {
      setMessage({ type: 'error', text: result.message });
    }
  };

  const handleOpenRoleModal = (user: User) => {
    setSelectedUser(user);
    setNewRole(user.uloga);
    setShowRoleModal(true);
  };

  const handleUpdateRole = async () => {
    if (!selectedUser || !newRole) return;

    const result = await userService.updateUserRole(selectedUser.id, newRole);
    
    if (result.success) {
      setMessage({ type: 'success', text: result.message });
      setShowRoleModal(false);
      loadUsers();
    } else {
      setMessage({ type: 'error', text: result.message });
    }
  };

  const getRoleBadgeColor = (role: UserRole): string => {
    switch (role) {
      case 'ADMINISTRATOR':
        return 'bg-red-100 text-red-800';
      case 'MODERATOR':
        return 'bg-blue-100 text-blue-800';
      case 'IGRAC':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white shadow-xl rounded-lg overflow-hidden">
          <div className="bg-gradient-to-r from-purple-500 to-purple-600 px-6 py-8">
            <h1 className="text-3xl font-bold text-white">Upravljanje Korisnicima</h1>
            <p className="text-purple-100 mt-2">Administracija svih korisnika platforme</p>
          </div>

          <div className="p-6">
            {message.text && (
              <div
                className={`mb-4 p-4 rounded ${
                  message.type === 'success'
                    ? 'bg-green-50 border border-green-400 text-green-700'
                    : 'bg-red-50 border border-red-400 text-red-700'
                }`}
              >
                {message.text}
              </div>
            )}

            <div className="mb-4">
              <p className="text-gray-600">
                Ukupno korisnika: <span className="font-bold">{users.length}</span>
              </p>
            </div>

            {/* Users Table */}
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Ime i Prezime
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Email
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Uloga
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Akcije
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {users.map((user) => (
                    <tr key={user.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {user.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {(user as any).ime_prezime}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {user.email}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getRoleBadgeColor(
                            user.uloga
                          )}`}
                        >
                          {user.uloga}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                        <button
                          onClick={() => handleOpenRoleModal(user)}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          Promeni ulogu
                        </button>
                        <button
                          onClick={() => handleDeleteUser(user.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Obriši
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {/* Role Change Modal */}
      {showRoleModal && selectedUser && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Promena uloge korisnika
            </h3>
            
            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-2">
                Korisnik: <span className="font-medium">{selectedUser.imePrezime}</span>
              </p>
              <p className="text-sm text-gray-600 mb-4">
                Email: <span className="font-medium">{selectedUser.email}</span>
              </p>
              
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nova uloga
              </label>
              <select
                value={newRole}
                onChange={(e) => setNewRole(e.target.value as UserRole)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="IGRAC">IGRAČ</option>
                <option value="MODERATOR">MODERATOR</option>
                <option value="ADMINISTRATOR">ADMINISTRATOR</option>
              </select>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={handleUpdateRole}
                className="flex-1 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
              >
                Potvrdi
              </button>
              <button
                onClick={() => setShowRoleModal(false)}
                className="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400"
              >
                Otkaži
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminUsers;