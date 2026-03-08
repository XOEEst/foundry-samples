Audit this repository with the `foundry-repo-audit` skill.

Focus on candidate folders that can become Azure AI Foundry agents and classify them as either:
- `ready-hosted-agent`
- `convertible-sample`

For each candidate:
- record the relative path
- record concrete evidence used for classification
- resolve any available `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_AGENT_NAME`, `AGENT_NAME`, or `agentName` metadata and note the source
- verify deployment status when both project endpoint and agent name are available
- otherwise mark deployment state as `unknown` and list the missing metadata

Produce a concise final report that summarizes:
- candidates reviewed
- classifications
- deployment states
- issue actions taken

If issue creation is enabled by the workflow, use the dedupe token format `foundry-agent-audit::<relative-path>`.
