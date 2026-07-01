---
name: run-project
description: Runs projects locally or with Docker containers. Use when starting a development server, running the project, launching containers, or when the user asks to "run", "start", or "serve" the application.
---

# Run Project

Runs the project locally or with Docker by detecting configuration files.

## Detection Order

Check for these files in the workspace root to determine run method:

1. **Docker Compose**: `docker-compose.yml`, `docker-compose.yaml`, `compose.yml`, `compose.yaml`
2. **Dockerfile**: `Dockerfile`, `Dockerfile.*`
3. **Package Manager Files**: `package.json`, `requirements.txt`, `Gemfile`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `mix.exs`, etc.
4. **Scripts**: `Makefile`, `start.sh`, `run.sh`

## Workflow

```
Task Progress:
- [ ] Step 1: Detect configuration files
- [ ] Step 2: Ask user: local or Docker?
- [ ] Step 3: Check prerequisites
- [ ] Step 4: Execute run command
- [ ] Step 5: Monitor output
```

### Step 1: Detect Configuration Files

Use Glob to find configuration files:

```
Glob patterns to check:
- **/docker-compose*.yml
- **/compose*.yml
- **/Dockerfile*
- package.json
- requirements.txt
- Makefile
```

Report findings to user before proceeding.

### Step 2: Ask User Preference

If both local and Docker options exist, ask user:

- **Local**: Run directly on the machine
- **Docker**: Run in container(s)

If only one option exists, proceed with that option (confirm with user if needed).

### Step 3: Check Prerequisites

**For Docker:**
- Verify Docker is installed: `docker --version`
- Verify Docker daemon is running: `docker info`

**For Local:**
- Check if dependency files exist
- Verify runtime/package manager is available

### Step 4: Execute Run Command

#### Docker Compose

```bash
# Default
docker compose up

# Build and run
docker compose up --build

# Run in background
docker compose up -d
```

#### Dockerfile Only

```bash
# Build image
docker build -t <project-name> .

# Run container
docker run -p <port>:<port> <project-name>
```

Read the Dockerfile to determine exposed ports.

#### Local Execution

Detect the appropriate command by reading configuration files:

| File Found | Read For | Common Commands |
|------------|----------|-----------------|
| `package.json` | `scripts` section | `npm run dev`, `npm start`, `yarn dev` |
| `requirements.txt` | - | `python app.py`, `python main.py` |
| `Makefile` | targets | `make run`, `make dev` |
| `Cargo.toml` | - | `cargo run` |
| `go.mod` | - | `go run .` |
| Custom scripts | - | `./start.sh`, `./run.sh` |

**Important**: Read the actual config file to find the correct command. Do not guess.

### Step 5: Monitor Output

After starting the process:

1. Set `block_until_ms: 0` for long-running servers
2. Read terminal file to check startup status
3. Look for:
   - Port binding messages
   - "Server started" or similar
   - Error messages
4. Report the URL/port to user when ready

## Error Handling

### Docker Issues

| Error | Solution |
|-------|----------|
| "Cannot connect to Docker daemon" | Ask user to start Docker Desktop/daemon |
| "port is already in use" | Find process using port or suggest alternate port |
| Build fails | Show error, suggest fixes based on output |

### Local Issues

| Error | Solution |
|-------|----------|
| Dependencies not installed | Run install command first |
| Missing runtime | Guide user to install required runtime |
| Port in use | Suggest different port or kill existing process |

## Common Patterns

### Install Dependencies First

If project hasn't been set up:

```bash
# Node.js
npm install
# or
yarn install

# Python
pip install -r requirements.txt
# or
python -m venv venv && pip install -r requirements.txt

# Others - detect from lock files
```

### Environment Setup

Check for `.env.example` or `.env.sample`:
- If `.env` missing but example exists, copy and inform user to configure

### Multiple Services

For projects with multiple components (frontend + backend):
- Check for workspace/monorepo structure
- Ask user which service to run
- Or suggest running all with Docker Compose

## Scripts Folder

Store reusable project scripts in `scripts/` within this skill directory:

```
run-project/
├── SKILL.md
└── scripts/
    └── (store project run scripts here)
```

**Usage:**
- Save commonly used run configurations as shell scripts
- Store helper scripts for port detection, process management, etc.
- Keep environment setup scripts for different scenarios

**Example scripts to create:**
- `check-port.sh` - Check if a port is in use
- `kill-port.sh` - Kill process on a specific port
- `wait-for-service.sh` - Wait for a service to be ready

## Tips

- **Prefer Docker Compose** when available - it handles multi-service setups cleanly
- **Check README.md** for project-specific instructions
- **Watch for environment variables** - some projects require specific env vars
- **Use `-d` flag** for Docker when user wants to run in background