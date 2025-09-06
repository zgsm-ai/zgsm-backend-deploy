\c chatgpt;

CREATE TABLE IF NOT EXISTS "public"."api_rule" (
    "id" SERIAL PRIMARY KEY,
    "deleted" CHAR(1) NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "update_at" TIMESTAMP NOT NULL,
    "rule_type" VARCHAR(50) NOT NULL,
    "rule_info" VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS "public"."configuration" (
    "id" SERIAL PRIMARY KEY,
    "deleted" CHAR(1) NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "update_at" TIMESTAMP NOT NULL,
    "belong_type" VARCHAR(50) NOT NULL,
    "attribute_key" VARCHAR(50) NOT NULL,
    "attribute_value" TEXT NOT NULL,
    "attribute_type" VARCHAR(50),
    "desc" TEXT
);

-- api_rule 规则
INSERT INTO "public"."api_rule"("id", "deleted", "created_at", "update_at", "rule_type", "rule_info") VALUES (1, 'f', '2023-05-09 19:09:36', '2023-05-09 19:09:36', 'dept', '研发体系');

INSERT INTO "public"."configuration"("id", "deleted", "created_at", "update_at", "belong_type", "attribute_key", "attribute_type", "attribute_value", "desc") VALUES (1, 'f', '2023-04-25 11:00:28', '2023-04-25 11:00:28', 'banner', 'text', 'string', '【通知】千流 Copilot 全面开放使用，欢迎大家安装使用！ 使用文档：http://docs.sangfor.org/x/rNnHDw', '1.由于每次提问都有费用支出，请勿用于工作无关的问题 ; 2. API已提供申请入口(广场->应用广场->申请)，请勿私自爬取API使用，一经发现，将封号处理！');

--组件库映射配置
--INSERT INTO "public"."components_map"("id", "deleted", "created_at", "update_at", "team", "git_repos", "inline_chat_components", "fauxpilot_components") VALUES (2, 'f', '2023-10-23 20:22:11', '2023-10-24 10:38:02.358202', 'other', 'just_test', 'test', '');
--INSERT INTO "public"."components_map"("id", "deleted", "created_at", "update_at", "team", "git_repos", "inline_chat_components", "fauxpilot_components") VALUES (3, 'f', '2023-10-24 10:47:21', '2023-10-26 17:44:30.912257', 'mss', 'git@mq.code.sangfor.org:SS/SOC/soc_workflow_webui.git', 'ss-business,ss-components', 'ss-components');
--INSERT INTO "public"."components_map"("id", "deleted", "created_at", "update_at", "team", "git_repos", "inline_chat_components", "fauxpilot_components") VALUES (1, 'f', '2023-10-23 20:12:45', '2023-10-26 19:00:32.772076', 'sase', 'git@mq.code.sangfor.org:UED/SAAS/sase-platform.git', 'sase,idux', 'sf-vue;;<sf-[a-z]+,idux');


--设置更新 开始自增id
SELECT setval('api_rule_id_seq', (SELECT MAX(id) FROM api_rule));
SELECT setval('configuration_id_seq', (SELECT MAX(id) FROM configuration));
--SELECT setval('components_map_id_seq', (SELECT MAX(id) FROM components_map));

