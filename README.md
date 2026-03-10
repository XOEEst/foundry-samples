# Azure AI Foundry Documentation Samples

This repository acts as the top-level directory for official Azure AI Foundry documentation sample code and examples. It includes notebooks and sample code that contain end-to-end examples as well as smaller code snippets for common developer tasks.

This repository is entirely open source, guidance on how to contribute and links to additional repositories are provided below.

Use the samples in this repository to try out Azure AI Foundry scenarios on your local machine!

## Foundry repo audit automation

This repo includes a GitHub Copilot custom agent and a GitHub Actions workflow for auditing folders that can become Azure AI Foundry agents.

### What was added

- Custom agent: `.github/agents/foundry-repo-auditor.agent.md`
- Repo skill: `.github/skills/foundry-repo-audit/SKILL.md`
- Workflow: `.github/workflows/foundry-repo-audit.yml`
- Azure MCP reference config: `.github/copilot/azure-foundry-mcp.json`
- Copilot coding agent setup workflow: `.github/workflows/copilot-setup-steps.yml`

### Default behavior

- The workflow runs automatically on every push to `main`.
- The workflow can also be started manually from the **Actions** tab by running **Foundry Repo Audit**.
- Automatic runs are report-only and upload an audit artifact instead of creating issues.

### Required secret

Create a repository secret named `COPILOT_PAT` before using the workflow.

Recommended token setup:
- token type: fine-grained personal access token
- GitHub permission: **Copilot Requests**
- repository access: this repository
- repository permissions: enough access to read contents and create issues

To add the secret on GitHub.com:
1. Open the repository.
2. Go to **Settings** > **Secrets and variables** > **Actions**.
3. Select **New repository secret**.
4. Name it `COPILOT_PAT`.
5. Paste the token value and save.

### Azure MCP / Foundry setup for GitHub coding agent

To let the GitHub website coding agent or custom agent verify Foundry deployments in the cloud, finish the Azure MCP setup in GitHub:

1. Open **Settings** > **Copilot** > **Coding agent**.
2. In **MCP configuration**, paste the JSON from `.github/copilot/azure-foundry-mcp.json`.
3. Open **Settings** > **Environments** and create an environment named `copilot`.
4. Add environment variables named `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_SUBSCRIPTION_ID`.
5. Run the **copilot-setup-steps** workflow once from the **Actions** tab to validate Azure login for Copilot coding agent sessions.

This repo now includes agent-level Azure MCP configuration in `.github/agents/foundry-repo-auditor.agent.md`, but the GitHub website experience still depends on the repository Copilot environment being configured correctly.

### How to run it from the GitHub website

1. Open the repository on GitHub.
2. Select the **Actions** tab.
3. Choose **Foundry Repo Audit** from the workflow list.
4. Select **Run workflow**.
5. If you want the run to create GitHub issues, enable the `create_issues` option.
6. Start the workflow and then open the run summary to review logs and download the `foundry-repo-audit-report` artifact.

## Contributing

Found a bug or have a suggestion? [Open an issue](https://github.com/microsoft-foundry/foundry-samples/issues/new) — we welcome feedback from everyone!

Sample contributions are submitted through a private staging repository. If you're a Microsoft employee or contractor, see the [contributing guidelines](CONTRIBUTING.md) for how to get started.

