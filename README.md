# 🐳 Docker Hands-On Workshop

Welcome! This repo contains everything you need to get hands-on with Docker.
Follow each section in order each one builds on the previous.

---

## 🚀 Getting Started

### Clone the Repo
```bash
git clone https://github.com/peroute/docker-workshop.git
cd docker-workshop
```


## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- A terminal (Terminal on Mac/Linux, PowerShell on Windows)
- A text editor (VS Code recommended)

Verify Docker is installed:

```bash
docker --version
docker compose version
```

---

## 📂 Repo Structure

```
docker-workshop/
├── 01-hello-docker/        # Your first container
├── 02-build-image/         # Build a custom image
├── 03-volumes/             # Persistent data & live reloading
├── 04-docker-compose/      # Multi-container apps
├── 05-networking/          # Container communication
├── 06-challenge/           # Test your skills!
└── README.md               # You are here
```

---

## 01 Hello Docker

**Goal:** Run your first container and explore what's inside.

### Step 1: Run Hello World

```bash
docker run hello-world
```

You should see a message saying "Hello from Docker!". This confirms Docker is working.

### Step 2: Explore a Container

```bash
docker run -it ubuntu bash
```

You're now INSIDE a container. Try these commands:

```bash
cat /etc/os-release    # What OS are you running?
whoami                 # Who are you?
ls /                   # What's in here?
pwd                    # Where are you?
exit                   # Leave the container
```

### Step 3: See Your Containers

```bash
docker ps              # Shows running containers (should be empty)
docker ps -a           # Shows ALL containers (including stopped ones)
```

### Step 4: Clean Up

```bash
docker rm $(docker ps -a -q)   # Remove all stopped containers
```

### 💡 What just happened?

- `docker run` downloaded an image and created a container from it
- `-it` gave you an interactive terminal
- The container has its own filesystem, separate from your machine
- When you exited, the container stopped but still exists until you remove it

---

## 02 Build Your Own Image

**Goal:** Create a Docker image for a Python Flask app.

### Step 1: Look at the App

```bash
cd 02-build-image/app
```

Check out `app.py` it's a simple web server. Check `requirements.txt` it lists the dependencies.

### Step 2: Understand the Dockerfile

Open `Dockerfile` and read each line:

```dockerfile
# Start from a Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Tell Docker this app uses port 5000
EXPOSE 5000

# Command to run when the container starts
CMD ["python", "app.py"]
```

### Step 3: Build the Image

```bash
docker build -t myapp .
```

- `-t myapp` gives the image a name (tag)
- `.` tells Docker to look for the Dockerfile in the current directory

### Step 4: Run It

```bash
docker run -d -p 5000:5000 --name my-flask-app myapp
```

- `-d` runs in the background (detached)
- `-p 5000:5000` maps port 5000 on your machine to port 5000 in the container
- `--name my-flask-app` gives the container a friendly name

### Step 5: Test It

Open your browser: [http://localhost:5000](http://localhost:5000)

You should see: **"Hello from Docker! 🐳"**

Try the other endpoints:
- [http://localhost:5000/info](http://localhost:5000/info) shows container info
- [http://localhost:5000/health](http://localhost:5000/health) health check

### Step 6: Useful Commands

```bash
docker ps                           # See running containers
docker logs my-flask-app            # See app logs
docker exec -it my-flask-app sh     # Open a shell inside the container
docker stop my-flask-app            # Stop the container
docker rm my-flask-app              # Remove the container
docker images                       # List all images
```

### 💡 What just happened?

- You wrote a recipe (Dockerfile) that tells Docker how to build your app
- `docker build` created an image a snapshot of your app + all its dependencies
- `docker run` created a running container from that image
- Anyone with this Dockerfile can build and run the exact same app no "works on my machine" problems!

---

## 03 Volumes: Persistent Data

**Goal:** Understand how to keep data alive and share files between your machine and a container.

### The Problem

```bash
docker run -it ubuntu bash
echo "important data" > /myfile.txt
exit

# Run a new container the file is GONE
docker run -it ubuntu bash
cat /myfile.txt   # "No such file or directory"
exit
```

Containers are **ephemeral** when they're removed, their data disappears.

### Solution: Bind Mounts

A bind mount connects a folder on YOUR machine to a folder inside the container.

### Step 1: Look at the Site

```bash
cd 03-volumes/site
```

There's a simple `index.html` file.

### Step 2: Run Nginx with a Bind Mount
If linux/Mac:
```bash
docker run -d -p 8080:80 -v $(pwd)/site:/usr/share/nginx/html --name my-website nginx
```
If windows
```bash
docker run -d -p 8080:80 -v ${PWD}:/usr/share/nginx/html --name my-website nginx
```

- `-v $(pwd)/site:/usr/share/nginx/html` mounts the `site/` folder into the container

### Step 3: See It Live

Open [http://localhost:8080](http://localhost:8080) you should see the website.

### Step 4: Edit and Refresh

Open `site/index.html` in your text editor. Change the heading text to your name. Save the file. **Refresh the browser** your changes appear instantly!

### Step 5: Named Volumes (for Databases)

Named volumes are managed by Docker great for databases where you don't need direct file access.

```bash
# Create a named volume
docker volume create mydata

# Run a container with the named volume
docker run -d -v mydata:/data --name vol-test ubuntu bash -c "echo 'persisted!' > /data/test.txt && sleep 300"

# Check the data
docker exec vol-test cat /data/test.txt

# Stop and remove the container
docker stop vol-test && docker rm vol-test

# Data survives! Run a new container with the same volume
docker run --rm -v mydata:/data ubuntu cat /data/test.txt
```

### Step 6: Clean Up

```bash
docker stop my-website && docker rm my-website
docker volume rm mydata
```

### 💡 Key Takeaways

| Type | Use Case | Example |
|------|----------|---------|
| **Bind Mount** | Development share code between host and container | `-v $(pwd)/src:/app` |
| **Named Volume** | Production persist database data | `-v pgdata:/var/lib/postgresql/data` |

---

## 04 Docker Compose: Multi-Container Apps

**Goal:** Run a web app + database together using Docker Compose.

Real apps don't run alone they need databases, caches, queues, etc. Docker Compose lets you define and run multi-container applications.

### Step 1: Look at the Project

```bash
cd 04-docker-compose
```

Check out the structure:

```
04-docker-compose/
├── docker-compose.yml    # Defines all services
├── app/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── db/
    └── init.sql          # Database initialization script
```

### Step 2: Read the docker-compose.yml

Open `docker-compose.yml` and read through it. Notice:

- **Two services** are defined: `web` and `db`
- The `web` service **builds** from the `app/` folder
- The `db` service uses the official **postgres** image
- They share a **network** (created automatically by Compose)
- The database has a **volume** for persistent data
- Environment variables configure the database credentials

### Step 3: Start Everything

```bash
docker compose up --build
```

Watch the logs you'll see both the web app and database starting up.

### Step 4: Test It

Open [http://localhost:5000](http://localhost:5000) you should see a visitor counter.

Try these endpoints:
- [http://localhost:5000](http://localhost:5000) increments and shows visit count
- [http://localhost:5000/visitors](http://localhost:5000/visitors) shows all visits with timestamps

Refresh a few times the count goes up because it's stored in PostgreSQL!

### Step 5: Useful Compose Commands

Open a **new terminal** (keep the first one running):

```bash
docker compose ps                        # See running services
docker compose logs web                  # Logs for just the web service
docker compose exec db psql -U postgres -d workshop   # Connect to the database
```

Inside psql, try:

```sql
SELECT * FROM visitors;
\q
```

### Step 6: Stop Everything

Go back to the terminal running Compose and press `Ctrl+C`, then:

```bash
docker compose down            # Stops and removes containers + network
docker compose down -v         # Also removes volumes (deletes data!)
```

### 💡 Key Takeaways

- `docker-compose.yml` is your app's infrastructure as code
- `docker compose up` replaces multiple `docker run` commands
- Services can talk to each other by **service name** (e.g., the app connects to `db`, not `localhost`)
- Volumes persist data between restarts
- `docker compose down` cleans everything up

---

## 05 Networking: Containers Talking to Each Other

**Goal:** Understand how containers communicate on Docker networks.

### Step 1: The Default Behavior Isolation

Containers can't talk to each other by default:

```bash
# Run two containers
docker run -d --name container-a nginx
docker run -d --name container-b nginx

# Try to ping from A to B FAILS
docker exec container-a ping -c 2 container-b

# Clean up
docker stop container-a container-b && docker rm container-a container-b
```

### Step 2: Create a Custom Network

```bash
docker network create workshop-net
```

### Step 3: Run Containers on the Same Network

```bash
cd 05-networking

# Build and run app1 (a simple API)
docker build -t app1 app1/
docker run -d --name app1 --network workshop-net -p 3001:3000 app1

# Build and run app2 (calls app1)
docker build -t app2 app2/
docker run -d --name app2 --network workshop-net -p 3002:3000 app2
```

### Step 4: See Them Communicate

Open [http://localhost:3002](http://localhost:3002)

App2 calls App1 internally using the container name `app1` no ports needed between containers on the same network!

### Step 5: Verify the Network

```bash
# See all networks
docker network ls

# Inspect the network see which containers are connected
docker network inspect workshop-net

# Ping between containers by name
docker exec app2 ping -c 2 app1
```

### Step 6: Clean Up

```bash
docker stop app1 app2 && docker rm app1 app2
docker network rm workshop-net
```

### 💡 Key Takeaways

- Containers are **isolated by default** they can't reach each other
- Put containers on the **same network** to let them communicate
- Containers find each other by **name** (DNS), not IP address
- Docker Compose does this **automatically** every service is on the same network
- Port mapping (`-p`) is only needed for **external access** (your browser), not container-to-container

---

## 06 Challenge: Put It All Together! 🏆

**Goal:** Dockerize a Node.js app with Redis on your own.

You're given a working Node.js app that uses Redis as a cache. Your job:

1. Write a `Dockerfile` for the Node app
2. Write a `docker-compose.yml` that runs both the app and Redis
3. Make sure data persists using a volume
4. Verify everything works

### The App

```bash
cd 06-challenge/app
```

Look at `server.js` it's a simple task list API that stores tasks in Redis.

**Hints:**
- The Node app runs on port **3000**
- It expects Redis at host `redis` on port `6379`
- Use `node:18-slim` as the base image
- Redis data is stored at `/data` inside the container
- The official Redis image is just called `redis`

### What to Create

1. `06-challenge/app/Dockerfile`
2. `06-challenge/docker-compose.yml`

### Test Your Solution

```bash
cd 06-challenge
docker compose up --build
```

Then test:

```bash
# Add a task
curl -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{"task": "Learn Docker"}'

# List tasks
curl http://localhost:3000/tasks

# Or open http://localhost:3000/tasks in your browser
```

### Solution

Don't peek until you've tried! The solution files are in `06-challenge/solution/`.

---

## 🎉 Congratulations!

You've learned:

- ✅ What containers are and how to run them
- ✅ How to build custom images with Dockerfiles
- ✅ How to persist data with volumes
- ✅ How to run multi-container apps with Docker Compose
- ✅ How container networking works

### Cheat Sheet

| Command | What it does |
|---------|-------------|
| `docker run -it <image> bash` | Run a container interactively |
| `docker build -t <name> .` | Build an image from a Dockerfile |
| `docker run -d -p <host>:<container> <image>` | Run in background with port mapping |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker logs <container>` | View container logs |
| `docker exec -it <container> sh` | Open shell in running container |
| `docker stop <container>` | Stop a container |
| `docker rm <container>` | Remove a container |
| `docker images` | List images |
| `docker volume create <name>` | Create a named volume |
| `docker network create <name>` | Create a network |
| `docker compose up --build` | Start all services (build if needed) |
| `docker compose down` | Stop and remove all services |
| `docker compose down -v` | Stop, remove, and delete volumes |
| `docker compose ps` | List running services |
| `docker compose logs <service>` | View service logs |
| `docker compose exec <service> <cmd>` | Run command in a service |

### Next Steps

- [Docker Official Docs](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/) explore official images
- Multi-stage builds for smaller images
- Docker in CI/CD pipelines
- Deploying to the cloud with Docker
