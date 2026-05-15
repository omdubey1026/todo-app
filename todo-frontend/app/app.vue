<script setup>
import { ref, onMounted } from 'vue'

const todos = ref([])
const newTodo = ref("")

const fetchTodos = async () => {
  const res = await fetch(
    "https://todo-app-hi0d.onrender.com/todos"
  )

  const data = await res.json()

  todos.value = data.map(todo => ({
    id: todo[0],
    task: todo[1],
    completed: todo[2]
  }))
}

const addTodo = async () => {
  if (!newTodo.value) return

  await fetch(
    `https://todo-app-hi0d.onrender.com/todos?item=${newTodo.value}`,
    {
      method: "POST"
    }
  )

  newTodo.value = ""

  fetchTodos()
}

const deleteTodo = async (id) => {
  await fetch(
    `https://todo-app-hi0d.onrender.com/todos/${id}`,
    {
      method: "DELETE"
    }
  )

  fetchTodos()
}

const editTodo = async (id, oldText) => {
  const newText = prompt("Edit todo:", oldText)

  if (!newText) return

  await fetch(
    `https://todo-app-hi0d.onrender.com/todos/${id}?item=${newText}`,
    {
      method: "PUT"
    }
  )

  fetchTodos()
}

const toggleComplete = async (id) => {
  await fetch(
    `https://todo-app-hi0d.onrender.com/todos/${id}/complete`,
    {
      method: "PUT"
    }
  )

  fetchTodos()
}


onMounted(fetchTodos)
</script>

<template>
  <div class="container">
    <h1>📝 Todo App</h1>

    <div class="stats">
      <p>Total: <b>{{ todos.length }}</b></p>
      <p>Completed: <b>{{ todos.filter(t => t.completed).length }}</b></p>
    </div>

    <div class="input-box">
      <input
        v-model="newTodo"
        placeholder="Enter new task..."
        @keyup.enter="addTodo"
      />
      <button @click="addTodo">➕ Add</button>
    </div>

    <ul>
      <li
        v-for="todo in todos"
        :key="todo.id"
        class="todo-item"
        :class="{ done: todo.completed }"
      >
        <span>{{ todo.task }}</span>

        <div class="actions">
          <button @click="toggleComplete(todo.id)">✔</button>
          <button @click="editTodo(todo.id, todo.task)">✏</button>
          <button @click="deleteTodo(todo.id)">❌</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style>
body {
  font-family: Arial, sans-serif;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: white;
  margin: 0;
}

/* container */
.container {
  max-width: 520px;
  margin: 60px auto;
  background: rgba(255, 255, 255, 0.05);
  padding: 25px;
  border-radius: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

/* title */
h1 {
  text-align: center;
  background: linear-gradient(90deg, #4facfe, #00f2fe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* stats */
.stats {
  display: flex;
  justify-content: space-between;
  margin: 15px 0;
  font-size: 14px;
  color: #cbd5e1;
}

/* input box */
.input-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 10px;
  background: #111827;
  color: white;
  outline: none;
  border: 1px solid #334155;
}

input:focus {
  border: 1px solid #38bdf8;
}

/* add button */
button {
  padding: 10px 14px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  background: linear-gradient(135deg, #38bdf8, #6366f1);
  color: white;
  font-weight: bold;
  transition: 0.2s;
}

button:hover {
  transform: scale(1.05);
}

/* todo list */
ul {
  list-style: none;
  padding: 0;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 12px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  transition: 0.2s;
}

.todo-item:hover {
  background: rgba(255,255,255,0.1);
}

/* completed style */
.todo-item.done {
  text-decoration: line-through;
  opacity: 0.6;
  color: #94a3b8;
}

/* action buttons */
.actions button {
  margin-left: 6px;
  background: #1f2937;
}

.actions button:hover {
  background: #334155;
}

/* smooth animation */
.todo-item {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>