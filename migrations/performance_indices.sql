-- Performance optimization indices for AUDITORIA360
-- Phase 3: Database query optimization

-- Employee table indices for frequent queries
CREATE INDEX IF NOT EXISTS idx_employees_active_department ON employees(is_active, department);
CREATE INDEX IF NOT EXISTS idx_employees_employee_id ON employees(employee_id);
CREATE INDEX IF NOT EXISTS idx_employees_cpf ON employees(cpf);
CREATE INDEX IF NOT EXISTS idx_employees_hire_date ON employees(hire_date);

-- PayrollCompetency table indices
CREATE INDEX IF NOT EXISTS idx_payroll_competencies_year_month ON payroll_competencies(year, month);
CREATE INDEX IF NOT EXISTS idx_payroll_competencies_status ON payroll_competencies(status);
CREATE INDEX IF NOT EXISTS idx_payroll_competencies_type ON payroll_competencies(type);
CREATE INDEX IF NOT EXISTS idx_payroll_competencies_created_at ON payroll_competencies(created_at);

-- PayrollItem table indices for complex queries
CREATE INDEX IF NOT EXISTS idx_payroll_items_competency_employee ON payroll_items(competency_id, employee_id);
CREATE INDEX IF NOT EXISTS idx_payroll_items_employee_id ON payroll_items(employee_id);
CREATE INDEX IF NOT EXISTS idx_payroll_items_competency_id ON payroll_items(competency_id);
CREATE INDEX IF NOT EXISTS idx_payroll_items_validation ON payroll_items(is_validated, has_divergences);
CREATE INDEX IF NOT EXISTS idx_payroll_items_gross_salary ON payroll_items(gross_salary);

-- Composite indices for common filter combinations
CREATE INDEX IF NOT EXISTS idx_employees_active_department_position ON employees(is_active, department, position) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_payroll_competencies_year_month_type ON payroll_competencies(year, month, type);

-- Audit and performance tracking indices
CREATE INDEX IF NOT EXISTS idx_employees_created_at ON employees(created_at);
CREATE INDEX IF NOT EXISTS idx_employees_updated_at ON employees(updated_at);
CREATE INDEX IF NOT EXISTS idx_payroll_items_calculated_at ON payroll_items(calculated_at);
CREATE INDEX IF NOT EXISTS idx_payroll_items_validated_at ON payroll_items(validated_at);

-- Partial indices for better performance on common queries
CREATE INDEX IF NOT EXISTS idx_active_employees_only ON employees(id, full_name, department, position) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_draft_competencies ON payroll_competencies(id, year, month) WHERE status = 'draft';
CREATE INDEX IF NOT EXISTS idx_unvalidated_payroll_items ON payroll_items(id, competency_id, employee_id) WHERE is_validated = false;

-- Text search optimization (for future full-text search)
CREATE INDEX IF NOT EXISTS idx_employees_full_name_gin ON employees USING gin(to_tsvector('portuguese', full_name));

-- Performance statistics views
CREATE OR REPLACE VIEW payroll_performance_stats AS
SELECT 
    pc.id as competency_id,
    pc.year,
    pc.month,
    pc.type,
    pc.status,
    COUNT(pi.id) as total_items,
    COUNT(CASE WHEN pi.is_validated = true THEN 1 END) as validated_items,
    COUNT(CASE WHEN pi.has_divergences = true THEN 1 END) as items_with_divergences,
    SUM(pi.gross_salary) as total_gross_salary,
    SUM(pi.net_salary) as total_net_salary,
    SUM(pi.total_deductions) as total_deductions,
    AVG(pi.gross_salary) as avg_gross_salary,
    MAX(pi.updated_at) as last_update
FROM payroll_competencies pc
LEFT JOIN payroll_items pi ON pc.id = pi.competency_id
GROUP BY pc.id, pc.year, pc.month, pc.type, pc.status;

-- Index for the performance stats view
CREATE INDEX IF NOT EXISTS idx_payroll_performance_stats ON payroll_competencies(id, year, month, type, status);

-- Query optimization hints for common patterns
COMMENT ON INDEX idx_employees_active_department IS 'Optimizes employee filtering by active status and department';
COMMENT ON INDEX idx_payroll_items_competency_employee IS 'Eliminates N+1 queries when loading employee payroll items';
COMMENT ON INDEX idx_payroll_competencies_year_month IS 'Optimizes competency lookup by period';