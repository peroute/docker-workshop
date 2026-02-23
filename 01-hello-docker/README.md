# 01 — Hello Docker

**Goal:** Run your first container and explore what's inside.

## Step 1: Run Hello World

```bash
docker run hello-world
```

You should see a message saying "Hello from Docker!". This confirms Docker is working.

## Step 2: Explore a Container

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

## Step 3: See Your Containers

```bash
docker ps              # Shows running containers (should be empty)
docker ps -a           # Shows ALL containers (including stopped ones)
```

## Step 4: Clean Up

```bash
docker rm $(docker ps -a -q)   # Remove all stopped containers
```

## What just happened?

- `docker run` downloaded an image and created a container from it
- `-it` gave you an interactive terminal
- The container has its own filesystem, separate from your machine
- When you exited, the container stopped but still exists until you remove it
