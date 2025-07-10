\c casdoor;
-- ----------------------------
-- Table structure for application
-- ----------------------------
DROP TABLE IF EXISTS "public"."application";
CREATE TABLE "public"."application" (
  "owner" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "created_time" varchar(100) COLLATE "pg_catalog"."default",
  "display_name" varchar(100) COLLATE "pg_catalog"."default",
  "logo" varchar(200) COLLATE "pg_catalog"."default",
  "homepage_url" varchar(100) COLLATE "pg_catalog"."default",
  "description" varchar(100) COLLATE "pg_catalog"."default",
  "organization" varchar(100) COLLATE "pg_catalog"."default",
  "cert" varchar(100) COLLATE "pg_catalog"."default",
  "default_group" varchar(100) COLLATE "pg_catalog"."default",
  "header_html" text COLLATE "pg_catalog"."default",
  "enable_password" bool,
  "enable_sign_up" bool,
  "enable_signin_session" bool,
  "enable_auto_signin" bool,
  "enable_code_signin" bool,
  "enable_saml_compress" bool,
  "enable_saml_c14n10" bool,
  "enable_saml_post_binding" bool,
  "use_email_as_saml_name_id" bool,
  "enable_web_authn" bool,
  "enable_link_with_email" bool,
  "org_choice_mode" varchar(255) COLLATE "pg_catalog"."default",
  "saml_reply_url" varchar(500) COLLATE "pg_catalog"."default",
  "providers" text COLLATE "pg_catalog"."default",
  "signin_methods" varchar(2000) COLLATE "pg_catalog"."default",
  "signup_items" varchar(3000) COLLATE "pg_catalog"."default",
  "signin_items" text COLLATE "pg_catalog"."default",
  "grant_types" varchar(1000) COLLATE "pg_catalog"."default",
  "tags" text COLLATE "pg_catalog"."default",
  "saml_attributes" varchar(1000) COLLATE "pg_catalog"."default",
  "is_shared" bool,
  "ip_restriction" varchar(255) COLLATE "pg_catalog"."default",
  "client_id" varchar(100) COLLATE "pg_catalog"."default",
  "client_secret" varchar(100) COLLATE "pg_catalog"."default",
  "redirect_uris" varchar(1000) COLLATE "pg_catalog"."default",
  "forced_redirect_origin" varchar(100) COLLATE "pg_catalog"."default",
  "token_format" varchar(100) COLLATE "pg_catalog"."default",
  "token_signing_method" varchar(100) COLLATE "pg_catalog"."default",
  "token_fields" varchar(1000) COLLATE "pg_catalog"."default",
  "expire_in_hours" int4,
  "refresh_expire_in_hours" int4,
  "signup_url" varchar(200) COLLATE "pg_catalog"."default",
  "signin_url" varchar(200) COLLATE "pg_catalog"."default",
  "forget_url" varchar(200) COLLATE "pg_catalog"."default",
  "affiliation_url" varchar(100) COLLATE "pg_catalog"."default",
  "ip_whitelist" varchar(200) COLLATE "pg_catalog"."default",
  "terms_of_use" varchar(100) COLLATE "pg_catalog"."default",
  "signup_html" text COLLATE "pg_catalog"."default",
  "signin_html" text COLLATE "pg_catalog"."default",
  "theme_data" json,
  "footer_html" text COLLATE "pg_catalog"."default",
  "form_css" text COLLATE "pg_catalog"."default",
  "form_css_mobile" text COLLATE "pg_catalog"."default",
  "form_offset" int4,
  "form_side_html" text COLLATE "pg_catalog"."default",
  "form_background_url" varchar(200) COLLATE "pg_catalog"."default",
  "form_background_url_mobile" varchar(200) COLLATE "pg_catalog"."default",
  "failed_signin_limit" int4,
  "failed_signin_frozen_time" int4
)
;

-- ----------------------------
-- Records of application
-- ----------------------------
INSERT INTO "public"."application" VALUES ('admin', 'app-built-in', '2025-07-02T16:20:48Z', 'Casdoor', 'https://cdn.casbin.org/img/casdoor-logo_1185x256.png', 'https://casdoor.org', '', 'built-in', 'cert-built-in', '', '', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', '', '', '[{"owner":"","name":"provider_captcha_default","canSignUp":false,"canSignIn":false,"canUnlink":false,"countryCodes":null,"prompted":false,"signupGroup":"","rule":"None","provider":null}]', '[{"name":"Password","displayName":"Password","rule":"All"},{"name":"Verification code","displayName":"Verification code","rule":"All"},{"name":"WebAuthn","displayName":"WebAuthn","rule":"None"},{"name":"Face ID","displayName":"Face ID","rule":"None"}]', '[{"name":"ID","visible":false,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"Random"},{"name":"Username","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Display name","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Password","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Confirm password","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Email","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"Normal"},{"name":"Phone","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Agreement","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"}]', 'null', 'null', '[]', 'null', 'f', '', '33b6fa19be033e3b60ca', 'cd4b0174b0e30a340437058856be3cbba3e40ad7', '[]', '', 'JWT', '', '[]', 168, 0, '', '', '', '', '', '', '', '', NULL, '', '', '', 2, '', '', '', 0, 0);
INSERT INTO "public"."application" VALUES ('admin', 'login', '2025-07-03T00:22:30+08:00', 'login', 'https://cdn.casbin.org/img/casdoor-logo_1185x256.png', '', '', 'user-group', 'cert-built-in', '', '', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', '', '', '[{"owner":"","name":"Github","canSignUp":false,"canSignIn":true,"canUnlink":true,"countryCodes":null,"prompted":false,"signupGroup":"","rule":"","provider":null},{"owner":"","name":"SMS","canSignUp":true,"canSignIn":true,"canUnlink":true,"countryCodes":["CN"],"prompted":false,"signupGroup":"","rule":"All","provider":null}]', '[{"name":"Verification code","displayName":"Verification code","rule":"Phone only"}]', '[{"name":"ID","visible":false,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"Random"},{"name":"Username","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Display name","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Password","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Confirm password","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Email","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"Normal"},{"name":"Phone","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Agreement","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Signup button","visible":true,"required":true,"prompted":false,"type":"","customCss":"","label":"","placeholder":"","options":null,"regex":"","rule":"None"},{"name":"Providers","visible":true,"required":true,"prompted":false,"type":"","customCss":".provider-img {\n width: 30px;\n margin: 5px;\n }\n .provider-big-img {\n margin-bottom: 10px;\n }\n ","label":"","placeholder":"","options":null,"regex":"","rule":"small"}]', '[{"name":"Back button","visible":false,"label":"","customCss":".back-button {\n      top: 65px;\n      left: 15px;\n      position: absolute;\n}\n.back-inner-button{}","placeholder":"","rule":"None","isCustom":false},{"name":"Languages","visible":true,"label":"","customCss":".login-languages {\n    top: 55px;\n    right: 5px;\n    position: absolute;\n}","placeholder":"","rule":"None","isCustom":false},{"name":"Logo","visible":true,"label":"","customCss":".login-logo-box {}","placeholder":"","rule":"None","isCustom":false},{"name":"Signin methods","visible":true,"label":"","customCss":".signin-methods {}","placeholder":"","rule":"None","isCustom":false},{"name":"Username","visible":true,"label":"","customCss":".login-username {}\n.login-username-input{}","placeholder":"","rule":"None","isCustom":false},{"name":"Password","visible":true,"label":"","customCss":".login-password {}\n.login-password-input{}","placeholder":"","rule":"None","isCustom":false},{"name":"Agreement","visible":true,"label":"","customCss":".login-agreement {}","placeholder":"","rule":"None","isCustom":false},{"name":"Forgot password?","visible":false,"label":"","customCss":".login-forget-password {\n    display: inline-flex;\n    justify-content: space-between;\n    width: 320px;\n    margin-bottom: 25px;\n}","placeholder":"","rule":"None","isCustom":false},{"name":"Login button","visible":true,"label":"","customCss":".login-button-box {\n    margin-bottom: 5px;\n}\n.login-button {\n    width: 100%;\n}","placeholder":"","rule":"None","isCustom":false},{"name":"Signup link","visible":false,"label":"","customCss":".login-signup-link {\n    margin-bottom: 24px;\n    display: flex;\n    justify-content: end;\n}","placeholder":"","rule":"None","isCustom":false},{"name":"Providers","visible":true,"label":"","customCss":".provider-img {\n      width: 30px;\n      margin: 5px;\n}\n.provider-big-img {\n      margin-bottom: 10px;\n}","placeholder":"","rule":"small","isCustom":false}]', '["authorization_code","password","client_credentials","token","id_token","refresh_token"]', '[]', 'null', 'f', '', 'c95ffe7f1060f95a3f2a', 'a043ae9fa2e8d1ab1764e991b11a4281733c37b7', '["https://zgsm.sangfor.com/oidc-auth/api/v1/manager/bind/account/callback","https://zgsm.sangfor.com/oidc-auth/api/v1/plugin/login/callback"]', '', 'JWT', '', '[]', 1024, 1024, '', '', '', '', '', '', '', '', NULL, '', '', '', 2, '', '', '', 5, 15);

-- ----------------------------
-- Primary Key structure for table application
-- ----------------------------
ALTER TABLE "public"."application" ADD CONSTRAINT "application_pkey" PRIMARY KEY ("owner", "name");
