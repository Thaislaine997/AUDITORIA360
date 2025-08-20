import js from "@eslint/js";
import tseslint from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";

export default [
  // Base JS config
  {
    ...js.configs.recommended,
    ignores: [
      "docs/assets/**",
      "out/**",
      ".next/**",
      "dist/**",
      "node_modules/**",
    ],
    languageOptions: {
      ...js.configs.recommended.languageOptions,
        document: "readonly",
        console: "readonly",
        process: "readonly",
        module: "writable",
        setTimeout: "readonly",
        clearTimeout: "readonly",
        setInterval: "readonly",
        clearInterval: "readonly",
        fetch: "readonly",
        sessionStorage: "readonly",
        localStorage: "readonly",
        FormData: "readonly",
        Blob: "readonly",
        URL: "readonly",
        navigator: "readonly",
        require: "readonly",
        exports: "readonly",
        HTMLElement: "readonly",
        HTMLButtonElement: "readonly",
        HTMLInputElement: "readonly",
        HTMLTextAreaElement: "readonly",
        HTMLSelectElement: "readonly",
        NodeJS: "readonly",
        File: "readonly",
        Event: "readonly",
        CustomEvent: "readonly",
        KeyboardEvent: "readonly",
        Element: "readonly",
        Response: "readonly",
        Deno: "readonly",
        MessageChannel: "readonly",
        AbortController: "readonly",
        ReadableStream: "readonly",
        TextEncoder: "readonly",
        Request: "readonly",
        WorkerGlobalScope: "readonly",
        MutationObserver: "readonly",
        IntersectionObserver: "readonly",
        ResizeObserver: "readonly",
        Buffer: "readonly",
        URLSearchParams: "readonly",
        btoa: "readonly",
        atob: "readonly",
        alert: "readonly",
      },
  }
  },
  // TypeScript + React config
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaFeatures: { jsx: true },
        ecmaVersion: 2020,
        sourceType: "module",
        // project: "./tsconfig.json", // Removido para evitar erro em arquivos fora do escopo
      },
      globals: {
        window: "readonly",
        document: "readonly",
        console: "readonly",
        process: "readonly",
        module: "writable",
        setTimeout: "readonly",
        clearTimeout: "readonly",
        setInterval: "readonly",
        clearInterval: "readonly",
        fetch: "readonly",
        sessionStorage: "readonly",
        localStorage: "readonly",
        FormData: "readonly",
        Blob: "readonly",
        URL: "readonly",
        navigator: "readonly",
        require: "readonly",
        exports: "readonly",
      },
    },
    plugins: {
      "@typescript-eslint": tseslint,
      react,
      "react-hooks": reactHooks,
    },
    rules: {
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": "warn",
      "no-console": "off",
      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  },
];
