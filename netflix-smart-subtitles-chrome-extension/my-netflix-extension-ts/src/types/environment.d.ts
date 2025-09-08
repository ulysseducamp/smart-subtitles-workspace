/*
 * Environment variables type definitions
 * These variables are injected at build time by webpack
 */

declare namespace NodeJS {
  interface ProcessEnv {
    readonly RAILWAY_API_URL: string;
    readonly RAILWAY_API_KEY: string;
    readonly FUSE_SUBTITLES_ENDPOINT: string;
    readonly NODE_ENV: 'development' | 'production';
  }
}

// Global environment variables (injected by webpack)
declare const process: {
  env: NodeJS.ProcessEnv;
};
