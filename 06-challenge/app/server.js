const http = require("http");
const { createClient } = require("redis");

const PORT = 3000;
const REDIS_URL = `redis://${process.env.REDIS_HOST || "redis"}:${process.env.REDIS_PORT || "6379"}`;

let client;

async function connectRedis() {
  client = createClient({ url: REDIS_URL });
  client.on("error", (err) => console.log("Redis error:", err));

  let retries = 5;
  while (retries > 0) {
    try {
      await client.connect();
      console.log("Connected to Redis!");
      return;
    } catch (err) {
      retries--;
      console.log(`Redis not ready, retrying... (${retries} attempts left)`);
      await new Promise((r) => setTimeout(r, 2000));
    }
  }
  throw new Error("Could not connect to Redis");
}

const server = http.createServer(async (req, res) => {
  // POST /tasks — add a task
  if (req.method === "POST" && req.url === "/tasks") {
    let body = "";
    req.on("data", (chunk) => (body += chunk));
    req.on("end", async () => {
      try {
        const { task } = JSON.parse(body);
        if (!task) {
          res.writeHead(400, { "Content-Type": "application/json" });
          return res.end(JSON.stringify({ error: "task is required" }));
        }
        const id = Date.now().toString();
        await client.hSet("tasks", id, JSON.stringify({ id, task, created_at: new Date().toISOString() }));
        res.writeHead(201, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ message: "Task added!", id, task }));
      } catch (err) {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  // GET /tasks — list all tasks
  if (req.method === "GET" && req.url === "/tasks") {
    try {
      const tasks = await client.hGetAll("tasks");
      const taskList = Object.values(tasks).map((t) => JSON.parse(t));
      taskList.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ count: taskList.length, tasks: taskList }));
    } catch (err) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // DELETE /tasks — clear all tasks
  if (req.method === "DELETE" && req.url === "/tasks") {
    try {
      await client.del("tasks");
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ message: "All tasks cleared!" }));
    } catch (err) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // Default
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(
    JSON.stringify({
      message: "🐳 Docker Challenge — Task List API",
      endpoints: {
        "POST /tasks": 'Add a task — body: {"task": "your task"}',
        "GET /tasks": "List all tasks",
        "DELETE /tasks": "Clear all tasks",
      },
    })
  );
});

connectRedis().then(() => {
  server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
});
