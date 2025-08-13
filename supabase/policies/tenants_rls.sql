-- Row Level Security Policies for AUDITORIA360 Multi-Tenant Architecture
-- Ensures proper data isolation between contabilidades and clients

-- Enable RLS on main tenant-based tables
-- Note: These policies assume JWT claims contain tenant identification

-- Clientes table - isolate by contabilidade_id
ALTER TABLE public.clientes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation_select" ON public.clientes
  FOR SELECT USING (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

CREATE POLICY "tenant_isolation_insert" ON public.clientes
  FOR INSERT WITH CHECK (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

CREATE POLICY "tenant_isolation_update" ON public.clientes
  FOR UPDATE USING (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

CREATE POLICY "tenant_isolation_delete" ON public.clientes
  FOR DELETE USING (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

-- Auditorias table - isolate by contabilidade_id
ALTER TABLE public.auditorias ENABLE ROW LEVEL SECURITY;

CREATE POLICY "audit_tenant_isolation_select" ON public.auditorias
  FOR SELECT USING (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

CREATE POLICY "audit_tenant_isolation_insert" ON public.auditorias
  FOR INSERT WITH CHECK (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

CREATE POLICY "audit_tenant_isolation_update" ON public.auditorias
  FOR UPDATE USING (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

-- Folhas de pagamento - isolate by contabilidade_id
ALTER TABLE public.folhas_pagamento ENABLE ROW LEVEL SECURITY;

CREATE POLICY "payroll_tenant_isolation_select" ON public.folhas_pagamento
  FOR SELECT USING (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

CREATE POLICY "payroll_tenant_isolation_insert" ON public.folhas_pagamento
  FOR INSERT WITH CHECK (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

-- Documentos - isolate by contabilidade_id
ALTER TABLE public.documentos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "documents_tenant_isolation_select" ON public.documentos
  FOR SELECT USING (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

CREATE POLICY "documents_tenant_isolation_insert" ON public.documentos
  FOR INSERT WITH CHECK (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

-- CCT (Convenções Coletivas) - isolate by contabilidade_id
ALTER TABLE public.cct ENABLE ROW LEVEL SECURITY;

CREATE POLICY "cct_tenant_isolation_select" ON public.cct
  FOR SELECT USING (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

-- Logs de auditoria - isolate by contabilidade_id for LGPD compliance
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "audit_logs_tenant_isolation" ON public.audit_logs
  FOR SELECT USING (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

-- User access control - users can only see their own data
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_self_access" ON public.users
  FOR SELECT USING (id = current_setting('jwt.claims.user_id')::uuid);

CREATE POLICY "users_same_tenant" ON public.users
  FOR SELECT USING (contabilidade_id = current_setting('jwt.claims.contabilidade_id')::uuid);

-- Function to set tenant context (to be called by application)
CREATE OR REPLACE FUNCTION set_tenant_context(tenant_id UUID, user_id UUID DEFAULT NULL)
RETURNS VOID AS $$
BEGIN
  PERFORM set_config('jwt.claims.contabilidade_id', tenant_id::text, true);
  IF user_id IS NOT NULL THEN
    PERFORM set_config('jwt.claims.user_id', user_id::text, true);
  END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to verify tenant isolation (for testing)
CREATE OR REPLACE FUNCTION verify_tenant_isolation()
RETURNS TABLE (
  table_name TEXT,
  has_rls BOOLEAN,
  policy_count INTEGER
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    t.table_name::TEXT,
    t.row_security::BOOLEAN,
    COUNT(p.policyname)::INTEGER
  FROM information_schema.tables t
  LEFT JOIN pg_policies p ON p.tablename = t.table_name
  WHERE t.table_schema = 'public'
    AND t.table_type = 'BASE TABLE'
    AND t.table_name IN ('clientes', 'auditorias', 'folhas_pagamento', 'documentos', 'cct', 'audit_logs', 'users')
  GROUP BY t.table_name, t.row_security;
END;
$$ LANGUAGE plpgsql;