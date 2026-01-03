import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import userService from '../services/userService';
import type { ProfileUpdateData } from '../types';

const Profile = () => {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [profileImage, setProfileImage] = useState<string | null>(null);  // DODAJ OVO
  const [formData, setFormData] = useState<ProfileUpdateData>({
    ime: '',
    prezime: '',
    datum_rodjenja: '',
    pol: undefined,
    drzava: '',
    ulica: '',
    broj: '',
  });
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string }>({ type: 'success', text: '' });

  useEffect(() => {
    const loadProfile = async () => {
      const result = await userService.getMyProfile();
      if (result.success && result.user) {
        if (result.user.profile_image) {
         const baseUrl = import.meta.env.VITE_API_URL.split('/api/v1')[0];
          const fullImageUrl = `${baseUrl}${result.user.profile_image}`;
          console.log('🌐 Full image URL:', fullImageUrl);
          setProfileImage(fullImageUrl);
        }
        
        setFormData({
          ime: result.user.ime || '',
          prezime: result.user.prezime || '',
          datum_rodjenja: result.user.datum_rodjenja || '',
          pol: result.user.pol,
          drzava: result.user.drzava || '',
          ulica: result.user.ulica || '',
          broj: result.user.broj || '',
        });
      }
    };
    
    loadProfile();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      
      // VALIDACIJA NA FRONTEND-U
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        setMessage({ type: 'error', text: 'Fajl je prevelik. Maksimalna veličina: 5MB' });
        return;
      }
      
      const allowedTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif'];
      if (!allowedTypes.includes(file.type)) {
        setMessage({ type: 'error', text: 'Nepodržan tip fajla. Dozvoljeni: PNG, JPG, JPEG, GIF' });
        return;
      }
      
      setSelectedFile(file);
    }
  };

  const handleUploadAvatar = async () => {
    if (!selectedFile) {
      setMessage({ type: 'error', text: 'Izaberite sliku' });
      return;
    }

    setLoading(true);
    const result = await userService.uploadAvatar(selectedFile);
    setLoading(false);

    if (result.success) {
      setMessage({ type: 'success', text: result.message });
      setSelectedFile(null);
      
      // AŽURIRAJ SLIKU
      if (result.profileImage) {
        const baseUrl = import.meta.env.VITE_API_URL.split('/api/v1')[0];
        const fullImageUrl = `${baseUrl}${result.profileImage}`;
        setProfileImage(fullImageUrl);
      }
    } else {
      setMessage({ type: 'error', text: result.message });
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: 'success', text: '' });

    const result = await userService.updateMyProfile(formData);
    setLoading(false);

    if (result.success) {
      setMessage({ type: 'success', text: result.message });
      setIsEditing(false);
    } else {
      setMessage({ type: 'error', text: result.message });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow-xl rounded-lg overflow-hidden">
          <div className="bg-gradient-to-r from-primary-500 to-primary-600 px-6 py-8">
            <h1 className="text-3xl font-bold text-white">Moj Profil</h1>
            <p className="text-primary-100 mt-2">Upravljajte svojim nalogom</p>
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

            {/* Avatar Upload Section */}
            <div className="mb-8 pb-8 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Profilna slika</h3>
              <div className="flex items-center space-x-4">
                <div className="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center overflow-hidden">
                  {profileImage ? (
                    <img src={profileImage} alt="Profile" className="w-full h-full object-cover" />
                  ) : (
                    <svg
                      className="w-12 h-12 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                      />
                    </svg>
                  )}
                </div>
                <div className="flex-1">
                  <input
                    type="file"
                    accept="image/png,image/jpg,image/jpeg,image/gif"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
                  />
                  <p className="text-xs text-gray-500 mt-1">PNG, JPG, JPEG ili GIF. Maksimalno 5MB.</p>
                  {selectedFile && (
                    <button
                      onClick={handleUploadAvatar}
                      disabled={loading}
                      className="mt-2 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50"
                    >
                      {loading ? 'Postavljanje...' : 'Postavi sliku'}
                    </button>
                  )}
                </div>
              </div>
            </div>

            {/* User Info Section */}
            <div className="mb-8">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900">Osnovne informacije</h3>
                {!isEditing && (
                  <button
                    onClick={() => setIsEditing(true)}
                    className="text-primary-600 hover:text-primary-700 font-medium"
                  >
                    Izmeni
                  </button>
                )}
              </div>

              {isEditing ? (
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Ime
                      </label>
                      <input
                        type="text"
                        name="ime"
                        value={formData.ime}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Prezime
                      </label>
                      <input
                        type="text"
                        name="prezime"
                        value={formData.prezime}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Datum rođenja
                      </label>
                      <input
                        type="date"
                        name="datum_rodjenja"
                        value={formData.datum_rodjenja}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Pol
                      </label>
                      <select
                        name="pol"
                        value={formData.pol || ''}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      >
                        <option value="">Izaberite</option>
                        <option value="M">Muški</option>
                        <option value="Z">Ženski</option>
                        <option value="O">Drugo</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Država
                      </label>
                      <input
                        type="text"
                        name="drzava"
                        value={formData.drzava}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Ulica
                      </label>
                      <input
                        type="text"
                        name="ulica"
                        value={formData.ulica}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Broj
                      </label>
                      <input
                        type="text"
                        name="broj"
                        value={formData.broj}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      />
                    </div>
                  </div>

                  <div className="flex space-x-4">
                    <button
                      type="submit"
                      disabled={loading}
                      className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50"
                    >
                      {loading ? 'Čuvanje...' : 'Sačuvaj izmene'}
                    </button>
                    <button
                      type="button"
                      onClick={() => setIsEditing(false)}
                      className="bg-gray-300 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-400"
                    >
                      Otkaži
                    </button>
                  </div>
                </form>
              ) : (
                <div className="space-y-3">
                  <div className="flex items-center">
                    <span className="text-gray-600 w-32">Email:</span>
                    <span className="font-medium">{user?.email}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="text-gray-600 w-32">Uloga:</span>
                    <span className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm font-medium">
                      {user?.uloga}
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;