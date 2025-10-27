/// <reference types="vite/client" />

// Chrome extension API types (for extension communication from webapp)
declare global {
  interface Window {
    chrome?: typeof chrome;
  }

  const chrome: {
    runtime: {
      sendMessage: (
        extensionId: string,
        message: unknown,
        callback: (response: unknown) => void
      ) => void;
      lastError?: { message: string };
    };
  };
}

export {};
