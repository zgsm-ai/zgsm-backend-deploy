\c casdoor;
-- ----------------------------
-- Table structure for provider
-- ----------------------------
DROP TABLE IF EXISTS "public"."provider";
CREATE TABLE "public"."provider" (
  "owner" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "created_time" varchar(100) COLLATE "pg_catalog"."default",
  "display_name" varchar(100) COLLATE "pg_catalog"."default",
  "category" varchar(100) COLLATE "pg_catalog"."default",
  "type" varchar(100) COLLATE "pg_catalog"."default",
  "sub_type" varchar(100) COLLATE "pg_catalog"."default",
  "method" varchar(100) COLLATE "pg_catalog"."default",
  "client_id" varchar(200) COLLATE "pg_catalog"."default",
  "client_secret" varchar(3000) COLLATE "pg_catalog"."default",
  "client_id2" varchar(100) COLLATE "pg_catalog"."default",
  "client_secret2" varchar(500) COLLATE "pg_catalog"."default",
  "cert" varchar(100) COLLATE "pg_catalog"."default",
  "custom_auth_url" varchar(200) COLLATE "pg_catalog"."default",
  "custom_token_url" varchar(200) COLLATE "pg_catalog"."default",
  "custom_user_info_url" varchar(200) COLLATE "pg_catalog"."default",
  "custom_logo" varchar(200) COLLATE "pg_catalog"."default",
  "scopes" varchar(100) COLLATE "pg_catalog"."default",
  "user_mapping" varchar(500) COLLATE "pg_catalog"."default",
  "http_headers" varchar(500) COLLATE "pg_catalog"."default",
  "host" varchar(100) COLLATE "pg_catalog"."default",
  "port" int4,
  "disable_ssl" bool,
  "title" varchar(100) COLLATE "pg_catalog"."default",
  "content" varchar(2000) COLLATE "pg_catalog"."default",
  "receiver" varchar(100) COLLATE "pg_catalog"."default",
  "region_id" varchar(100) COLLATE "pg_catalog"."default",
  "sign_name" varchar(100) COLLATE "pg_catalog"."default",
  "template_code" varchar(100) COLLATE "pg_catalog"."default",
  "app_id" varchar(100) COLLATE "pg_catalog"."default",
  "endpoint" varchar(1000) COLLATE "pg_catalog"."default",
  "intranet_endpoint" varchar(100) COLLATE "pg_catalog"."default",
  "domain" varchar(100) COLLATE "pg_catalog"."default",
  "bucket" varchar(100) COLLATE "pg_catalog"."default",
  "path_prefix" varchar(100) COLLATE "pg_catalog"."default",
  "metadata" text COLLATE "pg_catalog"."default",
  "id_p" text COLLATE "pg_catalog"."default",
  "issuer_url" varchar(100) COLLATE "pg_catalog"."default",
  "enable_sign_authn_request" bool,
  "email_regex" varchar(200) COLLATE "pg_catalog"."default",
  "provider_url" varchar(200) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of provider
-- ----------------------------
INSERT INTO "public"."provider" VALUES ('user-group', 'Oauth', '2025-08-04T10:35:22+08:00', 'Oauth', 'OAuth', 'Custom', '', 'Normal', '1239280978', '49a2e85e8fbe81ce5bf768889c8e2a9b', '', '', '', 'https://test.com/oauth2/authorize', 'https://test.com/oauth2/token', 'https://test.com/oauth2/get_user_info', '', 'openid profile email', '{"avatarUrl":"","displayName":"username","email":"phone_number","id":"employee_number","username":"username"}', 'null', '', 0, 'f', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'f', '', '');
INSERT INTO "public"."provider" VALUES ('user-group', 'SMS', '2025-08-01T02:40:43+08:00', 'SMS', 'SMS', 'Custom HTTP SMS', '', 'POST', '', '', '', '', '', '', '', '', '', '', '{"avatarUrl":"avatarUrl","displayName":"displayName","email":"email","id":"id","username":"username"}', 'null', '', 0, 'f', 'code', '', '', '', '', '', '', 'http://oidc-auth:9006/oidc-auth/api/v1/send/sms', '', '', '', '', '', '', '', 'f', '', '');

-- ----------------------------
-- Indexes structure for table provider
-- ----------------------------
CREATE UNIQUE INDEX "UQE_provider_name" ON "public"."provider" USING btree (
  "name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table provider
-- ----------------------------
ALTER TABLE "public"."provider" ADD CONSTRAINT "provider_pkey" PRIMARY KEY ("owner", "name");
