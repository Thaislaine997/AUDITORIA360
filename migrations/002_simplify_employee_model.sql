-- Migration: Simplify Employee Model to 7 Essential Fields
-- Genesis Final PR: Simplification of Employee/Funcionarios module

-- First, create the new simplified structure
ALTER TABLE employees RENAME TO employees_backup;

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,                    -- nome (full_name)
    codigo VARCHAR(50) UNIQUE NOT NULL,            -- código (employee_id)
    admissao TIMESTAMP WITH TIME ZONE NOT NULL,    -- admissão (hire_date)
    salario DECIMAL(10,2) NOT NULL,                -- salário (salary)
    dependentes INTEGER DEFAULT 0,                 -- dependentes (number of dependents)
    cpf VARCHAR(14) UNIQUE NOT NULL,               -- cpf
    cargo VARCHAR(100) NOT NULL,                   -- cargo (position)
    cbo VARCHAR(10),                               -- cbo (Brazilian Occupation Classification)
    
    -- Essential audit fields
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    created_by_id INTEGER REFERENCES users(id)
);

-- Create indexes for performance
CREATE INDEX idx_employees_codigo ON employees(codigo);
CREATE INDEX idx_employees_cpf ON employees(cpf);
CREATE INDEX idx_employees_is_active ON employees(is_active);

-- Migrate essential data from backup table
INSERT INTO employees (
    id, nome, codigo, admissao, salario, dependentes, cpf, cargo, cbo,
    is_active, created_at, updated_at, created_by_id
)
SELECT 
    id, 
    full_name, 
    employee_id, 
    hire_date, 
    salary, 
    0 as dependentes,  -- Default since this field didn't exist
    cpf, 
    COALESCE(position, 'Não informado'), 
    NULL as cbo,       -- Default since this field didn't exist
    is_active, 
    created_at, 
    updated_at, 
    created_by_id
FROM employees_backup
WHERE full_name IS NOT NULL 
  AND employee_id IS NOT NULL 
  AND hire_date IS NOT NULL 
  AND salary IS NOT NULL 
  AND cpf IS NOT NULL;

-- Reset sequence to match migrated data
SELECT setval('employees_id_seq', COALESCE((SELECT MAX(id) FROM employees), 1));

-- Update any foreign key references in payroll_items table
-- No structural change needed as it references employees.id which remains the same

-- Clean up after successful migration
-- DROP TABLE employees_backup;  -- Uncomment after verifying migration success

-- Add comment for documentation
COMMENT ON TABLE employees IS 'Simplified employee model with 7 essential fields as per Genesis Final requirements';
COMMENT ON COLUMN employees.nome IS 'Employee full name';
COMMENT ON COLUMN employees.codigo IS 'Employee identification code';
COMMENT ON COLUMN employees.admissao IS 'Hire date';
COMMENT ON COLUMN employees.salario IS 'Current salary';
COMMENT ON COLUMN employees.dependentes IS 'Number of dependents';
COMMENT ON COLUMN employees.cpf IS 'Brazilian tax ID (CPF)';
COMMENT ON COLUMN employees.cargo IS 'Job position/role';
COMMENT ON COLUMN employees.cbo IS 'Brazilian Occupation Classification code';