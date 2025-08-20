import { createClient } from '@supabase/supabase-js';

// Configure suas variáveis de ambiente no .env.local
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Exemplo de helper para autenticação (ajuste conforme sua lógica real)
export const authHelpers = {
  signIn: (email: string, password: string) => supabase.auth.signInWithPassword({ email, password }),
  signOut: () => supabase.auth.signOut(),
  getUser: () => supabase.auth.getUser(),
};
