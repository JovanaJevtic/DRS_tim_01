/**
 * Validacione funkcije
 */

// dopusteni mejlovi
const ALLOWED_EMAIL_DOMAINS = [
  "gmail.com",
  "hotmail.com",
  "outlook.com",
  "live.com",
  "yahoo.com",
  "icloud.com",
  "proton.me",
  "protonmail.com",
  "uns.ac.rs"
];


export const validateEmail = (email: string): boolean => {
  if (!email) return false;

  const trimmed = email.trim().toLowerCase();

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(trimmed)) {
    return false;
  }

  const domain = trimmed.split('@')[1];
  return ALLOWED_EMAIL_DOMAINS.includes(domain);
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