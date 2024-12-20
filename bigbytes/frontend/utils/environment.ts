export function isProduction() {
  return typeof process !== 'undefined' && process.env.NODE_ENV === 'production';
}

export function isSecureProtocol() {
  if (typeof window !== 'undefined') {
    return window.location.protocol === 'https:';
  }
  return false;
}

export function logRender(uuid) {
  if (!isProduction()) {
    console.log(uuid);
  }
}

export function isDebug() {
  return !!process.env.NEXT_PUBLIC_DEBUG && String(process.env.NEXT_PUBLIC_DEBUG) !== '0';
}

export const DEBUG = (func?: () => any): boolean => {
  const val = isDebug();

  if (func && val) {
    func?.();
  }

  return val;
};

export function isDemo() {
  return typeof window !== 'undefined' && window.location.hostname === 'demo.bigbytes.ai';
}

export function isPro() {
  return !!process.env.NEXT_PUBLIC_PRO;
}
