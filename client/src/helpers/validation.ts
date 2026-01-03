/**
 * Validacione funkcije
 */

export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePassword = (password: string): boolean => {
  // Minimum 6 karaktera
  return !!(password && password.length >= 6);
};

export const validateRequired = (value: string): boolean => {
  return !!(value && value.trim() !== '');
};

export const validateDate = (dateString: string): boolean => {
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date.getTime());
};

export const validateFileType = (file: File, allowedTypes: string[]): boolean => {
  if (!file) return false;
  const fileType = file.type;
  return allowedTypes.some((type) => fileType.includes(type));
};

export const validateFileSize = (file: File, maxSizeInMB: number): boolean => {
  if (!file) return false;
  const fileSizeInMB = file.size / (1024 * 1024);
  return fileSizeInMB <= maxSizeInMB;
};

/**
 * Helper funkcije za forme
 */

export const getErrorMessage = (field: string, value: string): string => {
  if (!validateRequired(value)) {
    return `${field} je obavezno polje`;
  }
  
  if (field === 'Email' && !validateEmail(value)) {
    return 'Unesite ispravan email';
  }
  
  if (field === 'Lozinka' && !validatePassword(value)) {
    return 'Lozinka mora imati najmanje 6 karaktera';
  }
  
  return '';
};