/// <reference path="../.astro/types.d.ts" />

// Global type declarations for the project

declare global {
  // Google Analytics gtag function
  function gtag(command: string, targetId: string, config?: Record<string, any>): void;

  // Window extensions
  interface Window {
    gtag?: typeof gtag;
    ticking?: boolean;
    currentAnalysis?: any;
  }

  // Element extensions for common properties
  interface Element {
    dataset: DOMStringMap;
  }

  // Event extensions
  interface Event {
    key?: string;
  }

  // HTMLElement extensions
  interface HTMLElement {
    click(): void;
  }
}

export {};