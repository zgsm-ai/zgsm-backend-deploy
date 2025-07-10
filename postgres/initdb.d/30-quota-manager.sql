-- -- Create databases
-- CREATE DATABASE quota_manager;

-- -- Connect to quota_manager database for quota-related tables
\c quota_manager;

-- Quota strategy table
CREATE TABLE IF NOT EXISTS quota_strategy (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    amount INTEGER NOT NULL,
    model VARCHAR(255),
    periodic_expr VARCHAR(255),
    condition TEXT,
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

-- Add index for strategy status field to improve query performance
CREATE INDEX IF NOT EXISTS idx_quota_strategy_status ON quota_strategy(status);

-- User quota table
CREATE TABLE IF NOT EXISTS quota (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    amount INTEGER NOT NULL,
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
    amount INTEGER NOT NULL,
    operation VARCHAR(50) NOT NULL,
    voucher_code VARCHAR(1000),
    related_user VARCHAR(255),
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
