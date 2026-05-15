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
    <h1>✨ My Todo Space</h1>

    <div class="stats">
      <p>📌 Total: <b>{{ todos.length }}</b></p>
      <p>✅ Done: <b>{{ todos.filter(t => t.completed).length }}</b></p>
    </div>

    <div class="input-box">
      <input
        v-model="newTodo"
        placeholder="What do you want to do?"
        @keyup.enter="addTodo"
      />
      <button @click="addTodo">Add +</button>
    </div>

    <transition-group name="list" tag="ul">
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
    </transition-group>
  </div>
</template>

<style>
body {
  font-family: 'Segoe UI', sans-serif;
  margin: 0;
  background: radial-gradient(circle at top, #1e293b, #0f172a);
  color: white;
}

/* container */
.container {
  max-width: 520px;
  margin: 60px auto;
  padding: 25px;
  border-radius: 18px;
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 40px rgba(0,0,0,0.6);
  transform: translateY(0);
  animation: floatIn 0.6s ease;
}

@keyframes floatIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* title */
h1 {
  text-align: center;
  font-size: 28px;
  background: linear-gradient(90deg, #38bdf8, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* stats */
.stats {
  display: flex;
  justify-content: space-between;
  margin: 15px 0;
  color: #cbd5e1;
}

/* input */
.input-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  flex: 1;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #334155;
  background: #0b1220;
  color: white;
  outline: none;
  transition: 0.2s;
}

input:focus {
  border-color: #38bdf8;
  box-shadow: 0 0 10px #38bdf8;
}

/* button */
button {
  padding: 10px 14px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  background: linear-gradient(135deg, #38bdf8, #6366f1);
  color: white;
  font-weight: bold;
  transition: 0.2s;
}

button:hover {
  transform: scale(1.08);
}

/* list */
ul {
  list-style: none;
  padding: 0;
}

/* todo item */
.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 14px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  transition: 0.25s;
}

.todo-item:hover {
  transform: translateY(-3px);
  background: rgba(255,255,255,0.12);
}

/* done animation */
.todo-item.done {
  text-decoration: line-through;
  opacity: 0.5;
  transform: scale(0.98);
}

/* buttons */
.actions button {
  margin-left: 6px;
  background: #1f2937;
}

.actions button:hover {
  background: #334155;
}

/* LIST ANIMATION */
.list-enter-active, .list-leave-active {
  transition: all 0.4s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>