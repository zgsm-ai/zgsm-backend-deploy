-- Create databases
CREATE DATABASE quota_manager;
CREATE DATABASE auth;

-- Connect to auth database for auth_users table
\c auth;

-- Auth users table
-- ----------------------------
-- Table structure for auth_users
-- ----------------------------
CREATE TABLE IF NOT EXISTS "public"."auth_users" (
  "id" uuid NOT NULL,
  "created_at" timestamptz(0),
  "updated_at" timestamptz(0),
  "access_time" timestamptz(0),
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "github_id" varchar(100) COLLATE "pg_catalog"."default",
  "github_name" varchar(100) COLLATE "pg_catalog"."default",
  "vip" int8 DEFAULT 0,
  "phone" varchar(20) COLLATE "pg_catalog"."default",
  "email" varchar(100) COLLATE "pg_catalog"."default",
  "password" varchar(100) COLLATE "pg_catalog"."default",
  "company" varchar(100) COLLATE "pg_catalog"."default",
  "location" varchar(100) COLLATE "pg_catalog"."default",
  "user_code" varchar(100) COLLATE "pg_catalog"."default",
  "external_accounts" varchar(100) COLLATE "pg_catalog"."default",
  "employee_number" varchar(100) COLLATE "pg_catalog"."default",
  "github_star" text COLLATE "pg_catalog"."default",
  "devices" jsonb
);

-- ----------------------------
-- Indexes structure for table auth_users
-- ----------------------------
CREATE INDEX "idx_auth_users_email" ON "public"."auth_users" USING btree (
  "email" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
-- CREATE UNIQUE INDEX "idx_auth_users_github_id" ON "public"."auth_users" USING btree (
--   "github_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
-- );
CREATE INDEX "idx_auth_users_name" ON "public"."auth_users" USING btree (
  "name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table auth_users
-- ----------------------------
ALTER TABLE "public"."auth_users" ADD CONSTRAINT "auth_users_pkey" PRIMARY KEY ("id");

-- Connect to quota_manager database for quota-related tables
\c quota_manager;

-- Quota strategy table
CREATE TABLE IF NOT EXISTS quota_strategy (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    model VARCHAR(255),
    periodic_expr VARCHAR(255),
    condition TEXT,
    max_exec_per_user INTEGER NOT NULL DEFAULT 0,
    status BOOLEAN DEFAULT true NOT NULL,  -- Status field: true=enabled, false=disabled
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP
);

-- Quota execution status table
CREATE TABLE IF NOT EXISTS quota_execute (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    batch_number VARCHAR(20) NOT NULL,
    status VARCHAR(50) NOT NULL,
    expiry_date TIMESTAMPTZ(0) NOT NULL,
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (strategy_id) REFERENCES quota_strategy(id)
);

-- Create indexes for quota_execute table
CREATE INDEX IF NOT EXISTS idx_quota_execute_strategy_id ON quota_execute(strategy_id);
CREATE INDEX IF NOT EXISTS idx_quota_execute_user_id ON quota_execute(user_id);
CREATE INDEX IF NOT EXISTS idx_quota_execute_batch_number ON quota_execute(batch_number);
CREATE INDEX IF NOT EXISTS idx_quota_execute_sid_uid_status ON quota_execute(strategy_id, user_id, status);

-- Add index for strategy status field to improve query performance
CREATE INDEX IF NOT EXISTS idx_quota_strategy_status ON quota_strategy(status);

-- User quota table
CREATE TABLE IF NOT EXISTS quota (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    expiry_date TIMESTAMPTZ(0) NOT NULL,
    status VARCHAR(20) DEFAULT 'VALID' NOT NULL,
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_quota_user_id ON quota(user_id);
CREATE INDEX IF NOT EXISTS idx_quota_expiry_date ON quota(expiry_date);
CREATE INDEX IF NOT EXISTS idx_quota_status ON quota(status);

-- Quota audit table
CREATE TABLE IF NOT EXISTS quota_audit (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    operation VARCHAR(50) NOT NULL,
    voucher_code VARCHAR(1000),
    related_user VARCHAR(255),
    strategy_id INTEGER,
    strategy_name VARCHAR(100),
    expiry_date TIMESTAMPTZ(0) NOT NULL,
    details TEXT,
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_quota_audit_user_id ON quota_audit(user_id);
CREATE INDEX IF NOT EXISTS idx_quota_audit_operation ON quota_audit(operation);
CREATE INDEX IF NOT EXISTS idx_quota_audit_strategy_name ON quota_audit(strategy_name);
CREATE INDEX IF NOT EXISTS idx_quota_audit_create_time ON quota_audit(create_time);

-- Voucher redemption table
CREATE TABLE IF NOT EXISTS voucher_redemption (
    id SERIAL PRIMARY KEY,
    voucher_code VARCHAR(1000) UNIQUE NOT NULL,
    receiver_id VARCHAR(255) NOT NULL,
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP
);

-- Create unique index to enforce one record per user per expiry date per status
CREATE UNIQUE INDEX IF NOT EXISTS idx_quota_user_expiry_status ON quota(user_id, expiry_date, status);

-- Employee department mapping table
CREATE TABLE IF NOT EXISTS employee_department (
    id SERIAL PRIMARY KEY,
    employee_number VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    dept_full_level_names TEXT NOT NULL,
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for employee_department table
CREATE INDEX IF NOT EXISTS idx_employee_department_employee_number ON employee_department(employee_number);
CREATE INDEX IF NOT EXISTS idx_employee_department_username ON employee_department(username);
CREATE INDEX IF NOT EXISTS idx_employee_department_dept_full_level_names ON employee_department(dept_full_level_names);

-- Model whitelist table
CREATE TABLE IF NOT EXISTS model_whitelist (
    id SERIAL PRIMARY KEY,
    target_type VARCHAR(20) NOT NULL,  -- 'user' or 'department'
    target_identifier VARCHAR(500) NOT NULL,  -- employee_number for user, department name for department
    allowed_models TEXT NOT NULL,
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for model_whitelist table
CREATE INDEX IF NOT EXISTS idx_model_whitelist_target_type ON model_whitelist(target_type);
CREATE INDEX IF NOT EXISTS idx_model_whitelist_target_identifier ON model_whitelist(target_identifier);
CREATE INDEX IF NOT EXISTS idx_model_whitelist_allowed_models ON model_whitelist(allowed_models);

-- Create unique index to prevent duplicate whitelists
CREATE UNIQUE INDEX IF NOT EXISTS idx_model_whitelist_unique ON model_whitelist(target_type, target_identifier);

-- Effective permissions table
CREATE TABLE IF NOT EXISTS effective_permissions (
    id SERIAL PRIMARY KEY,
    employee_number VARCHAR(100) UNIQUE NOT NULL,
    effective_models TEXT NOT NULL,
    whitelist_id INTEGER,
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (whitelist_id) REFERENCES model_whitelist(id) ON DELETE SET NULL
);

-- Create indexes for effective_permissions table
CREATE INDEX IF NOT EXISTS idx_effective_permissions_employee ON effective_permissions(employee_number);
CREATE INDEX IF NOT EXISTS idx_effective_permissions_whitelist ON effective_permissions(whitelist_id);
CREATE INDEX IF NOT EXISTS idx_effective_permissions_effective_models ON effective_permissions(effective_models);

-- Audit log table for permission operations
CREATE TABLE IF NOT EXISTS permission_audit (
    id SERIAL PRIMARY KEY,
    operation VARCHAR(50) NOT NULL,  -- 'employee_sync', 'whitelist_set', 'permission_updated', etc.
    target_type VARCHAR(20),  -- 'user' or 'department'
    target_identifier VARCHAR(500),
    details TEXT,  -- JSON string with operation details
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for permission_audit table
CREATE INDEX IF NOT EXISTS idx_permission_audit_operation ON permission_audit(operation);
CREATE INDEX IF NOT EXISTS idx_permission_audit_target_type ON permission_audit(target_type);
CREATE INDEX IF NOT EXISTS idx_permission_audit_target_identifier ON permission_audit(target_identifier);
CREATE INDEX IF NOT EXISTS idx_permission_audit_create_time ON permission_audit(create_time);

-- Star check settings table
CREATE TABLE IF NOT EXISTS star_check_settings (
    id SERIAL PRIMARY KEY,
    target_type VARCHAR(20) NOT NULL,  -- 'user' or 'department'
    target_identifier VARCHAR(500) NOT NULL,  -- employee_number for user, department name for department
    enabled BOOLEAN NOT NULL DEFAULT false,  -- star check enabled or disabled
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for star_check_settings table
CREATE INDEX IF NOT EXISTS idx_star_check_settings_target_type ON star_check_settings(target_type);
CREATE INDEX IF NOT EXISTS idx_star_check_settings_target_identifier ON star_check_settings(target_identifier);

-- Create unique index to prevent duplicate settings
CREATE UNIQUE INDEX IF NOT EXISTS idx_star_check_settings_unique ON star_check_settings(target_type, target_identifier);

-- Effective star check settings table
CREATE TABLE IF NOT EXISTS effective_star_check_settings (
    id SERIAL PRIMARY KEY,
    employee_number VARCHAR(100) UNIQUE NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT false,  -- effective star check setting
    setting_id INTEGER,
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (setting_id) REFERENCES star_check_settings(id) ON DELETE SET NULL
);

-- Create indexes for effective_star_check_settings table
CREATE INDEX IF NOT EXISTS idx_effective_star_check_settings_employee ON effective_star_check_settings(employee_number);
CREATE INDEX IF NOT EXISTS idx_effective_star_check_settings_setting ON effective_star_check_settings(setting_id);

-- Quota check settings table
CREATE TABLE IF NOT EXISTS quota_check_settings (
    id SERIAL PRIMARY KEY,
    target_type VARCHAR(20) NOT NULL,  -- 'user' or 'department'
    target_identifier VARCHAR(500) NOT NULL,  -- employee_number for user, department name for department
    enabled BOOLEAN NOT NULL DEFAULT false,  -- quota check enabled or disabled
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for quota_check_settings table
CREATE INDEX IF NOT EXISTS idx_quota_check_settings_target_type ON quota_check_settings(target_type);
CREATE INDEX IF NOT EXISTS idx_quota_check_settings_target_identifier ON quota_check_settings(target_identifier);

-- Create unique index to prevent duplicate settings
CREATE UNIQUE INDEX IF NOT EXISTS idx_quota_check_settings_unique ON quota_check_settings(target_type, target_identifier);

-- Effective quota check settings table
CREATE TABLE IF NOT EXISTS effective_quota_check_settings (
    id SERIAL PRIMARY KEY,
    employee_number VARCHAR(100) UNIQUE NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT false,  -- effective quota check setting
    setting_id INTEGER,
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (setting_id) REFERENCES quota_check_settings(id) ON DELETE SET NULL
);

-- Create indexes for effective_quota_check_settings table
CREATE INDEX IF NOT EXISTS idx_effective_quota_check_settings_employee ON effective_quota_check_settings(employee_number);
CREATE INDEX IF NOT EXISTS idx_effective_quota_check_settings_setting ON effective_quota_check_settings(setting_id);

-- Monthly quota usage record table
CREATE TABLE IF NOT EXISTS monthly_quota_usage (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    year_month VARCHAR(7) NOT NULL,  -- Format: YYYY-MM
    used_quota DECIMAL(10,2) NOT NULL,
    record_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    create_time TIMESTAMPTZ(0) DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, year_month)
);

-- Create indexes to improve query performance
CREATE INDEX IF NOT EXISTS idx_monthly_quota_usage_user_id ON monthly_quota_usage(user_id);
CREATE INDEX IF NOT EXISTS idx_monthly_quota_usage_year_month ON monthly_quota_usage(year_month);
CREATE INDEX IF NOT EXISTS idx_monthly_quota_usage_user_month ON monthly_quota_usage(user_id, year_month);

-- Add comments
COMMENT ON TABLE monthly_quota_usage IS 'Monthly quota usage record table';
COMMENT ON COLUMN monthly_quota_usage.user_id IS 'User ID';
COMMENT ON COLUMN monthly_quota_usage.year_month IS 'Year and month identifier, format: YYYY-MM';
COMMENT ON COLUMN monthly_quota_usage.used_quota IS 'Used quota amount';
COMMENT ON COLUMN monthly_quota_usage.record_time IS 'Record time';
COMMENT ON COLUMN monthly_quota_usage.create_time IS 'Create time';
