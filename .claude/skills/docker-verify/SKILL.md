---
name: docker-verify
description: Clone a GitHub repository and automatically build a Docker environment for local verification. Creates a verification workspace in WS/, sets up Docker files, launches the environment, and performs health checks.
argument-hint: <github-url> [--cleanup] [--no-keep-repo]
context: fork
agent: general-purpose
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion, Task, mcp__web_reader__webReader
---

# Docker Auto-Verify

Automatically clone a GitHub repository and set up a Docker Compose environment for local verification.

## Usage

```
/docker-verify <github-url> [--cleanup] [--no-keep-repo]
```

## Arguments

- `$0` - GitHub repository URL (required)
- `--cleanup` - Clean up the environment after verification (optional)
- `--no-keep-repo` - Don't keep the verification repository (optional)

## Workflow

This skill orchestrates multiple specialized agents to:

1. **Reconnaissance** (`repo-scout`): Analyze the GitHub repository
   - Detect programming language and framework
   - Check for existing Docker files
   - Identify dependencies and startup commands
   - Determine port numbers

2. **Repository Creation** (`repo-creator`): Set up verification workspace
   - Create workspace in `/prj/RECAPTOR/WS/<project-name>/`
   - Clone the repository
   - Configure Git settings

3. **Docker Design** (`docker-architect`): Design Docker environment
   - Generate Dockerfile (multi-stage build when applicable)
   - Create docker-compose.yml
   - Set up .env.example
   - Configure volumes and ports

4. **Launch Control** (`launch-controller`): Start the environment
   - Check port availability
   - Execute `docker-compose up`
   - Monitor container status
   - Watch logs

5. **Health Check** (`health-checker`): Verify the application
   - Test HTTP connectivity
   - Check status codes
   - Validate health endpoints
   - Generate health report

6. **Cleanup** (`clean-up-crew`): Clean up (optional)
   - Stop containers
   - Remove images and volumes
   - Clean workspace (if `--no-keep-repo`)

## Workspace

Verification repositories are created in:
```
/prj/RECAPTOR/WS/
└── <project-name>/
    ├── .git/
    ├── Dockerfile
    ├── docker-compose.yml
    └── ...
```

## Output

- `repo-scout-report.json` - Repository analysis
- `health-check-report.md` - Health check results
- `verify-summary.md` - Final summary

## Example

```
/docker-verify https://github.com/vercel/next.js
```

This will clone Next.js, create Docker files, launch the environment, and verify it's working.
