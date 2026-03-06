{
  "$schema": "https://opencode.ai/config.json",
  "lsp": false,
  "small_model": "openrouter/{{REVIEW_MODEL_MODEL}}",
  "provider": {
    "openrouter": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "openrouter",
      "options": {
        "baseURL": "{{REVIEW_MODEL_BASEURL}}",
        "apiKey": "{{REVIEW_MODEL_APIKEY}}"
      },
      "models": {
        "{{REVIEW_MODEL_MODEL}}": {
          "name": "{{REVIEW_MODEL_MODEL}}"
        }
      }
    }
  },

  "agent": {
    "CodeReviewer": {
      "description": "综合代码审查专家，专注于静态缺陷、安全漏洞、逻辑缺陷和内存问题的全面检测",
      "mode": "primary",
      "model": "{{REVIEW_MODEL_MODEL}}",
      "prompt": "{file:prompts/CodeReviewerPrompt.md}",
      "steps": 50,
      "permission": {
        "edit": "deny",
        "read": "allow",
        "glob": "allow",
        "grep": "allow",
        "list": "allow",
        "todowrite": "allow",
        "todoread": "allow",
        "file-outline": "allow",
        "mcp__cclsp__find_definition": "allow",
        "mcp__cclsp__find_references": "allow",
        "mcp__cclsp__restart_server": "allow",
        "bash": {
          "*": "deny",
          "git *": "allow" 
        },
        "task": {
          "*": "deny",
          "explore": "allow",
          "ReflectionAgent": "allow"
        }
      }
    },
    "ReflectionAgent": {
      "description": "代码审查反思验证专家，负责对已发现的代码缺陷进行深度二审、上下文取证与误报过滤，确保报告的准确性",
      "mode": "subagent",
      "model": "{{REVIEW_MODEL_MODEL}}",
      "prompt": "{file:prompts/ReflectionAgentPrompt.md}",
      "steps": 50,
      "permission": {
        "edit": "deny",
        "read": "allow",
        "glob": "allow",
        "grep": "allow",
        "list": "allow",
        "todowrite": "allow",
        "todoread": "allow",
        "file-outline": "allow",
        "mcp__cclsp__find_definition": "allow",
        "mcp__cclsp__find_references": "allow",
        "mcp__cclsp__restart_server": "allow",
        "bash": {
          "*": "deny",
          "git *": "allow" 
        },
        "task": {
          "*": "deny",
          "explore": "allow"
        }
      }
    }
  },

  "mcp": {
    "cclsp": {
      "type": "local",
      "command": ["cclsp"],
      "environment": {
        "CCLSP_CONFIG_PATH": "/app/base/cclsp.json"
      },
      "timeout": 30000
    },
    "issue": {
      "type": "local",
      "command": ["python", "/app/mcp/server.py"],
      "environment": {
        "ISSUE_MANAGER_API_URL": "{env:ISSUE_MANAGER_URL}"
      },
      "timeout": 30000
    }
  }
}
