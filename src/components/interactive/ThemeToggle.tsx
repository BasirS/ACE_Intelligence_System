import { useState, useEffect } from 'react';

export default function ThemeToggle() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [mounted, setMounted] = useState(false);

  // Handle hydration
  useEffect(() => {
    setMounted(true);

    // Get initial theme from localStorage or system preference
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.classList.toggle('dark', savedTheme === 'dark');
      document.documentElement.setAttribute('data-theme', savedTheme);
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setTheme('dark');
      document.documentElement.classList.add('dark');
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  // Don't render anything until mounted to avoid hydration mismatch
  if (!mounted) {
    return (
      <div className="w-16 h-10 bg-gray-200 rounded-full opacity-50 animate-pulse" />
    );
  }

  return (
    <label className="relative inline-flex cursor-pointer items-center">
      <input
        type="checkbox"
        checked={theme === 'dark'}
        onChange={toggleTheme}
        className="peer sr-only"
        aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      />

      <div className="peer h-10 w-16 rounded-full bg-gray-200 shadow-inner transition-all duration-300 ease-in-out after:absolute after:left-[4px] after:top-[4px] after:h-8 after:w-8 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:duration-300 after:ease-in-out after:content-[''] peer-checked:bg-blue-600 peer-checked:after:translate-x-6 peer-checked:after:border-white peer-focus:ring-4 peer-focus:ring-blue-300 dark:border-gray-600 dark:bg-gray-700 dark:peer-focus:ring-blue-800"></div>

      {/* Sun Icon */}
      <div className="absolute left-3 top-[10px] text-yellow-500 transition-all duration-300 peer-checked:scale-0 peer-checked:opacity-0">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="4"/>
          <path d="M12 2v2"/>
          <path d="M12 20v2"/>
          <path d="m4.93 4.93 1.41 1.41"/>
          <path d="m17.66 17.66 1.41 1.41"/>
          <path d="M2 12h2"/>
          <path d="M20 12h2"/>
          <path d="m6.34 17.66-1.41 1.41"/>
          <path d="m19.07 4.93-1.41 1.41"/>
        </svg>
      </div>

      {/* Moon Icon */}
      <div className="absolute right-3 top-[10px] text-blue-100 scale-0 opacity-0 transition-all duration-300 peer-checked:scale-100 peer-checked:opacity-100">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
        </svg>
      </div>
    </label>
  );
}