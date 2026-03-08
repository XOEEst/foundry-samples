---
name: foundry-repo-audit
description: Repository-specific workflow for discovering Azure AI Foundry agent candidates, resolving local deployment metadata, verifying deployment with microsoft-foundry, and preparing deduplicated GitHub issues.
argument-hint: "[optional path scope or sample family]"
user-invocable: true
---

# Foundry Repo Audit

Use this skill when working in `xoeest-foundry-samples` and the task is to find folders that can become Azure AI Foundry agents, determine whether those folders already map to deployed Foundry agents, or open audit issues for follow-up.

## Repository-specific guidance

- Hosted-agent candidates in this repo are primarily signaled by `agent.yaml`.
- Convertible samples often have a `Dockerfile`, a language manifest (`requirements.txt`, `pyproject.toml`, `package.json`, `*.csproj`, `go.mod`, or `pom.xml`), an entrypoint, and a `README.md`.
- Quickstart samples with `sample.yaml` are useful secondary candidates, but they should normally be classified as `convertible` instead of `ready` unless they also have hosted-agent signals.
- Existing GitHub issues can fan out to Azure DevOps through `.github/workflows/ado-automation.yml`, so GitHub issues are the preferred write target.
- Docs-owned files listed in `.github/CODEOWNERS` must not be renamed or moved.

## Candidate discovery workflow

1. Search for `**/agent.yaml` and classify each parent folder as a `ready-hosted-agent` candidate.
2. Search for `**/sample.yaml` and classify each parent folder as a `convertible-sample` candidate unless stronger hosted-agent evidence is present.
3. For folders without `agent.yaml`, look for the following combination before treating them as convertible:
   - `Dockerfile`
   - one language manifest
   - an obvious entrypoint such as `main.py`, `Program.cs`, `index.ts`, `app.py`, or another runnable source file
   - a `README.md`
4. Exclude `.github`, `.infra`, `infrastructure`, `migration`, test folders, and docs-only folders unless the user explicitly asks for a broader audit.
5. Record concrete evidence for every candidate instead of using generic labels like "looks deployable."

## Metadata resolution workflow

For each candidate, resolve deployment metadata in this order:

1. Search the candidate folder and its nearby config files for:
   - `AZURE_AI_PROJECT_ENDPOINT`
   - `AZURE_AI_AGENT_NAME`
   - `AGENT_NAME`
   - `agentName`
2. Prefer local runtime/config sources over documentation examples:
   - `.env*`
   - `azure.yaml`
   - `launchSettings.json`
   - PowerShell or shell deployment scripts
3. Use `agent.yaml` as a fallback source:
   - top-level `name`
   - `template.name`
   - `environment_variables`
4. Use README snippets only as low-confidence hints when no stronger config exists.
5. Track both the resolved value and its source. If a value is not present, leave it unset instead of inventing one.

## Foundry deployment verification

When both a project endpoint and agent name are available:

1. Invoke the `microsoft-foundry` skill before using Foundry tools.
2. Use Foundry agent lookup tooling to check whether the agent exists for the resolved project endpoint and agent name.
3. Classify the result as:
   - `verified` when the agent lookup succeeds
   - `not deployed` when the lookup definitively reports the agent does not exist
   - `unknown` when credentials, connectivity, or incomplete metadata prevent verification

When either the project endpoint or agent name is missing, set deployment state to `unknown` and list the missing fields.

## GitHub issue workflow

Before creating an issue:

1. Search existing issues for the dedupe token `foundry-agent-audit::<relative-path>`.
2. Reuse `./issue-template.md` for the issue structure.
3. Default to one issue per candidate path unless the user explicitly asks for one issue per problem type.
4. Recommended labels:
   - `foundry-agent-audit`
   - readiness label such as `ready-hosted-agent` or `convertible-sample`
   - an optional language label if it can be inferred safely

## Expected audit output

For each candidate, report:
- relative path
- classification
- evidence
- resolved project endpoint and agent name with sources
- deployment state
- issue action taken (`planned`, `created`, or `duplicate`)

## Useful repo references

- `.github/workflows/ado-automation.yml`
- `samples/python/hosted-agents/agent-framework/echo-agent/agent.yaml`
- `samples/csharp/FoundryA365/azure.yaml`
- `.github/CODEOWNERS`
