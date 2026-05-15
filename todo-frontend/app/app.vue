<script setup>
import { ref, computed, onMounted } from 'vue'

const todos = ref([])
const newTodo = ref("")

const filter = ref("all")
const search = ref("")

// FETCH TODOS
const fetchTodos = async () => {
  const res = await fetch("https://todo-app-hi0d.onrender.com/todos")
  const data = await res.json()

  todos.value = data.map(todo => ({
    id: todo[0],
    task: todo[1],
    completed: todo[2]
  }))
}

// ADD
const addTodo = async () => {
  if (!newTodo.value) return

  await fetch(
    `https://todo-app-hi0d.onrender.com/todos?item=${newTodo.value}`,
    { method: "POST" }
  )

  newTodo.value = ""
  await fetchTodos()
}

// DELETE
const deleteTodo = async (id) => {
  await fetch(
    `https://todo-app-hi0d.onrender.com/todos/${id}`,
    { method: "DELETE" }
  )

  await fetchTodos()
}

// TOGGLE
const toggleComplete = async (id) => {
  await fetch(
    `https://todo-app-hi0d.onrender.com/todos/${id}/complete`,
    { method: "PUT" }
  )

  await fetchTodos()
}

// EDIT
const editTodo = async (id, oldText) => {
  const newText = prompt("Edit task:", oldText)
  if (!newText) return

  await fetch(
    `https://todo-app-hi0d.onrender.com/todos/${id}?item=${newText}`,
    { method: "PUT" }
  )

  await fetchTodos()
}

// FILTERED + SEARCHED TODOS
const filteredTodos = computed(() => {
  return todos.value.filter(todo => {
    const matchSearch = todo.task
      .toLowerCase()
      .includes(search.value.toLowerCase())

    const matchFilter =
      filter.value === "all" ||
      (filter.value === "active" && !todo.completed) ||
      (filter.value === "done" && todo.completed)

    return matchSearch && matchFilter
  })
})

onMounted(fetchTodos)
</script>

<template>
  <div class="container">

    <h1>🚀 Task Dashboard</h1>

    <!-- PROGRESS BAR -->
    <div class="progress">
      <div
        class="bar"
        :style="{
          width: (todos.filter(t => t.completed).length / (todos.length || 1)) * 100 + '%'
        }"
      ></div>
    </div>

    <!-- SEARCH -->
    <input v-model="search" placeholder="🔍 Search tasks..." />

    <!-- FILTERS -->
    <div class="filters">
      <button @click="filter='all'">All</button>
      <button @click="filter='active'">Active</button>
      <button @click="filter='done'">Done</button>
    </div>

    <!-- INPUT -->
    <div class="input-box">
      <input
        v-model="newTodo"
        placeholder="Add new task..."
        @keyup.enter="addTodo"
      />
      <button @click="addTodo">Add</button>
    </div>

    <!-- LIST -->
    <ul>
      <li
        v-for="todo in filteredTodos"
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
  margin: 0;
  background: radial-gradient(circle at top, #1e293b, #0f172a);
  color: white;
}

.container {
  max-width: 520px;
  margin: 60px auto;
  padding: 25px;
  border-radius: 18px;
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 40px rgba(0,0,0,0.6);
}

h1 {
  text-align: center;
  background: linear-gradient(90deg, #38bdf8, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.progress {
  height: 8px;
  background: #1f2937;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 15px;
}

.bar {
  height: 100%;
  background: linear-gradient(90deg, #38bdf8, #a78bfa);
  transition: width 0.4s ease;
}

input {
  width: 100%;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 10px;
  border: none;
  background: #0b1220;
  color: white;
  outline: none;
}

.filters {
  display: flex;
  gap: 5px;
  margin-bottom: 10px;
}

.filters button {
  flex: 1;
  background: #111827;
  border: none;
  padding: 8px;
  color: white;
  border-radius: 8px;
  cursor: pointer;
}

.filters button:hover {
  background: #334155;
}

.input-box {
  display: flex;
  gap: 10px;
}

.input-box button {
  padding: 10px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #38bdf8, #6366f1);
  color: white;
  cursor: pointer;
}

ul {
  list-style: none;
  padding: 0;
  margin-top: 15px;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 12px;
  background: rgba(255,255,255,0.06);
  transition: 0.2s;
}

.todo-item.done {
  text-decoration: line-through;
  opacity: 0.5;
}

.actions button {
  margin-left: 5px;
  background: #1f2937;
  border: none;
  padding: 5px 8px;
  border-radius: 6px;
  color: white;
  cursor: pointer;
}

.actions button:hover {
  background: #334155;
}
</style>