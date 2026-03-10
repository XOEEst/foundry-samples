import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
AGENT_FILE = REPO_ROOT / ".github" / "agents" / "foundry-repo-auditor.agent.md"
SKILL_FILE = REPO_ROOT / ".github" / "skills" / "foundry-repo-audit" / "SKILL.md"
ISSUE_TEMPLATE = REPO_ROOT / ".github" / "skills" / "foundry-repo-audit" / "issue-template.md"
WORKFLOW_FILE = REPO_ROOT / ".github" / "workflows" / "foundry-repo-audit.yml"
PROMPT_FILE = REPO_ROOT / ".github" / "scripts" / "foundry-repo-audit-prompt.md"
SETUP_WORKFLOW_FILE = REPO_ROOT / ".github" / "workflows" / "copilot-setup-steps.yml"
MCP_CONFIG_FILE = REPO_ROOT / ".github" / "copilot" / "azure-foundry-mcp.json"


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    content = path.read_text(encoding="utf-8")
    assert content.startswith("---\n"), f"{path} is missing YAML frontmatter"

    _, frontmatter, body = content.split("---\n", 2)
    metadata: dict[str, str] = {}

    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        if line[:1].isspace():
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata, body


def test_custom_agent_profile_has_required_metadata_and_instructions() -> None:
    metadata, body = parse_frontmatter(AGENT_FILE)

    assert metadata["name"] == "Foundry Repo Auditor"
    assert metadata["target"] == "github-copilot"
    assert "Azure/*" in metadata["tools"]
    assert "mcp-servers" in metadata
    assert "Azure AI Foundry agents" in metadata["description"]
    assert "foundry-repo-audit" in body
    assert "Azure MCP Server Foundry tools" in body
    assert "foundry-agent-audit::<relative-path>" in body


def test_repo_skill_matches_directory_and_mentions_core_workflow_steps() -> None:
    metadata, body = parse_frontmatter(SKILL_FILE)

    assert metadata["name"] == "foundry-repo-audit"
    assert metadata["argument-hint"] == "[optional path scope or sample family]"
    assert metadata["user-invocable"] == "true"
    assert "`agent.yaml`" in body
    assert "`sample.yaml`" in body
    assert "`AZURE_AI_PROJECT_ENDPOINT`" in body
    assert "Azure MCP Server Foundry tools" in body
    assert "`./issue-template.md`" in body


def test_issue_template_contains_dedupe_token_and_placeholders() -> None:
    content = ISSUE_TEMPLATE.read_text(encoding="utf-8")

    assert "foundry-agent-audit::{{ relative_path }}" in content
    assert "{{ classification }}" in content
    assert "{{ deployment_state }}" in content
    assert "{{ next_action_1 }}" in content


def test_workflow_runs_on_main_and_uses_custom_agent() -> None:
    content = WORKFLOW_FILE.read_text(encoding="utf-8")

    assert "push:" in content
    assert "branches:" in content
    assert "- main" in content
    assert "workflow_dispatch:" in content
    assert "COPILOT_PAT" in content
    assert "--agent foundry-repo-auditor" in content
    assert ".github/scripts/foundry-repo-audit-prompt.md" in content
    assert "actions/upload-artifact@v4" in content


def test_prompt_file_mentions_skill_and_dedupe_token() -> None:
    content = PROMPT_FILE.read_text(encoding="utf-8")

    assert "`foundry-repo-audit` skill" in content
    assert "`AZURE_AI_PROJECT_ENDPOINT`" in content
    assert "`AZURE_AI_AGENT_NAME`" in content
    assert "foundry-agent-audit::<relative-path>" in content


def test_setup_workflow_and_mcp_config_exist_for_coding_agent() -> None:
    workflow = SETUP_WORKFLOW_FILE.read_text(encoding="utf-8")
    config = json.loads(MCP_CONFIG_FILE.read_text(encoding="utf-8"))

    assert "workflow_dispatch:" in workflow
    assert "environment: copilot" in workflow
    assert "azure/login@" in workflow
    assert "AZURE_CLIENT_ID" in workflow
    assert "AZURE_TENANT_ID" in workflow
    assert "AZURE_SUBSCRIPTION_ID" in workflow
    assert "${{ vars.AZURE_CLIENT_ID }}" in workflow
    assert "${{ vars.AZURE_TENANT_ID }}" in workflow
    assert "${{ vars.AZURE_SUBSCRIPTION_ID }}" in workflow

    assert config["mcpServers"]["Azure"]["command"] == "npx"
    assert config["mcpServers"]["Azure"]["args"] == ["-y", "@azure/mcp@latest", "server", "start"]
    assert config["mcpServers"]["Azure"]["tools"] == ["*"]
