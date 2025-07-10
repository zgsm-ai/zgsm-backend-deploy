\c casdoor;
-- ----------------------------
-- Table structure for organization
-- ----------------------------
DROP TABLE IF EXISTS "public"."organization";
CREATE TABLE "public"."organization" (
  "owner" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "created_time" varchar(100) COLLATE "pg_catalog"."default",
  "display_name" varchar(100) COLLATE "pg_catalog"."default",
  "website_url" varchar(100) COLLATE "pg_catalog"."default",
  "logo" varchar(200) COLLATE "pg_catalog"."default",
  "logo_dark" varchar(200) COLLATE "pg_catalog"."default",
  "favicon" varchar(200) COLLATE "pg_catalog"."default",
  "has_privilege_consent" bool,
  "password_type" varchar(100) COLLATE "pg_catalog"."default",
  "password_salt" varchar(100) COLLATE "pg_catalog"."default",
  "password_options" varchar(100) COLLATE "pg_catalog"."default",
  "password_obfuscator_type" varchar(100) COLLATE "pg_catalog"."default",
  "password_obfuscator_key" varchar(100) COLLATE "pg_catalog"."default",
  "password_expire_days" int4,
  "country_codes" text COLLATE "pg_catalog"."default",
  "default_avatar" varchar(200) COLLATE "pg_catalog"."default",
  "default_application" varchar(100) COLLATE "pg_catalog"."default",
  "user_types" text COLLATE "pg_catalog"."default",
  "tags" text COLLATE "pg_catalog"."default",
  "languages" varchar(255) COLLATE "pg_catalog"."default",
  "theme_data" json,
  "master_password" varchar(200) COLLATE "pg_catalog"."default",
  "default_password" varchar(200) COLLATE "pg_catalog"."default",
  "master_verification_code" varchar(100) COLLATE "pg_catalog"."default",
  "ip_whitelist" varchar(200) COLLATE "pg_catalog"."default",
  "init_score" int4,
  "enable_soft_deletion" bool,
  "is_profile_public" bool,
  "use_email_as_username" bool,
  "enable_tour" bool,
  "ip_restriction" varchar(255) COLLATE "pg_catalog"."default",
  "nav_items" varchar(1000) COLLATE "pg_catalog"."default",
  "widget_items" varchar(1000) COLLATE "pg_catalog"."default",
  "mfa_items" varchar(300) COLLATE "pg_catalog"."default",
  "account_items" varchar(5000) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of organization
-- ----------------------------
INSERT INTO "public"."organization" VALUES ('admin', 'built-in', '2025-07-02T08:28:07Z', 'Built-in Organization', 'https://example.com', '', '', 'https://cdn.casbin.org/img/casbin/favicon.ico', 'f', 'plain', '', '["AtLeast6"]', '', '', 0, '["US","ES","FR","DE","GB","CN","JP","KR","VN","ID","SG","IN"]', 'https://cdn.casbin.org/img/casbin.svg', '', '[]', '[]', '["en","zh","es","fr","de","id","ja","ko","ru","vi","pt"]', NULL, '', '', '', '', 2000, 'f', 'f', 'f', 'f', '', 'null', 'null', 'null', '[{"name":"Organization","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"ID","visible":true,"viewRule":"Public","modifyRule":"Immutable","regex":""},{"name":"Name","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Display name","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Avatar","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"User type","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Password","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""},{"name":"Email","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Phone","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Country code","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Country/Region","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Location","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Affiliation","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Title","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Homepage","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Bio","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Tag","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Signup application","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Roles","visible":true,"viewRule":"Public","modifyRule":"Immutable","regex":""},{"name":"Permissions","visible":true,"viewRule":"Public","modifyRule":"Immutable","regex":""},{"name":"Groups","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"3rd-party logins","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""},{"name":"Properties","visible":true,"viewRule":"Admin","modifyRule":"Admin","regex":""},{"name":"Is admin","visible":true,"viewRule":"Admin","modifyRule":"Admin","regex":""},{"name":"Is forbidden","visible":true,"viewRule":"Admin","modifyRule":"Admin","regex":""},{"name":"Is deleted","visible":true,"viewRule":"Admin","modifyRule":"Admin","regex":""},{"name":"Multi-factor authentication","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""},{"name":"WebAuthn credentials","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""},{"name":"Managed accounts","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""},{"name":"MFA accounts","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""}]');
INSERT INTO "public"."organization" VALUES ('admin', 'user-group', '2025-07-02T17:58:52+08:00', 'user-group', 'https://door.casdoor.com', '', '', 'https://cdn.casbin.org/img/favicon.png', 'f', 'plain', '', '["AtLeast6"]', 'Plain', '', 0, '["CN"]', 'https://cdn.casbin.org/img/casbin.svg', '', 'null', '[]', '["en","es","fr","de","zh","id","ja","ko","ru","vi","pt","it","ms","tr","ar","he","nl","pl","fi","sv","uk","kk","fa","cs","sk"]', NULL, '', '', '', '', 0, 'f', 'f', 'f', 'f', '', 'null', 'null', 'null', '[{"name":"Organization","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"ID","visible":true,"viewRule":"Public","modifyRule":"Immutable","regex":""},{"name":"Name","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Display name","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Avatar","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"User type","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Password","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""},{"name":"Email","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Phone","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Country code","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Country/Region","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Location","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Address","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Affiliation","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Title","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"ID card type","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"ID card","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"ID card info","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Homepage","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Bio","visible":true,"viewRule":"Public","modifyRule":"Self","regex":""},{"name":"Tag","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Language","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Gender","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Birthday","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Education","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Score","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Karma","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Ranking","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Signup application","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"API key","visible":false,"viewRule":"","modifyRule":"Self","regex":""},{"name":"Groups","visible":true,"viewRule":"Public","modifyRule":"Admin","regex":""},{"name":"Roles","visible":true,"viewRule":"Public","modifyRule":"Immutable","regex":""},{"name":"Permissions","visible":true,"viewRule":"Public","modifyRule":"Immutable","regex":""},{"name":"3rd-party logins","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""},{"name":"Properties","visible":false,"viewRule":"Admin","modifyRule":"Admin","regex":""},{"name":"Is online","visible":true,"viewRule":"Admin","modifyRule":"Admin","regex":""},{"name":"Is admin","visible":true,"viewRule":"Admin","modifyRule":"Admin","regex":""},{"name":"Is forbidden","visible":true,"viewRule":"Admin","modifyRule":"Admin","regex":""},{"name":"Is deleted","visible":true,"viewRule":"Admin","modifyRule":"Admin","regex":""},{"name":"Multi-factor authentication","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""},{"name":"WebAuthn credentials","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""},{"name":"Managed accounts","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""},{"name":"MFA accounts","visible":true,"viewRule":"Self","modifyRule":"Self","regex":""}]');

-- ----------------------------
-- Primary Key structure for table organization
-- ----------------------------
ALTER TABLE "public"."organization" ADD CONSTRAINT "organization_pkey" PRIMARY KEY ("owner", "name");
