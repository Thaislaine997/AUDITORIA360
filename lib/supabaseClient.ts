// src/frontend/src/lib/supabaseClient.ts

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL as string;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY as string;

// For development/demo purposes, use placeholder values if env vars are missing
// In production, these should be properly configured in .env.local
const defaultUrl = 'https://demo.supabase.co'; // Placeholder URL
const defaultKey = 'demo-key'; // Placeholder key

const finalUrl = supabaseUrl || defaultUrl;
const finalKey = supabaseAnonKey || defaultKey;

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn("Supabase URL or Anon Key are missing from .env.local - using placeholder values for development");
}

export const supabase = createClient(finalUrl, finalKey);