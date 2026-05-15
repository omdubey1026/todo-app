<script setup>
import { ref, onMounted } from "vue"

const todos = ref([])
const newTodo = ref("")

// GET TODOS
const fetchTodos = async () => {
  const res = await fetch("https://todo-app-hi0d.onrender.com/todos")
  const data = await res.json()

  todos.value = data
}

// ADD TODO
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

// DELETE
const deleteTodo = async (id) => {
  await fetch(
    `https://todo-app-hi0d.onrender.com/todos/${id}`,
    {
      method: "DELETE"
    }
  )

  fetchTodos()
}

// TOGGLE COMPLETE
const toggleComplete = async (id) => {
  if (!id) return

  await fetch(
    `https://todo-app-hi0d.onrender.com/todos/${id}/complete`,
    {
      method: "PUT"
    }
  )

  fetchTodos()
}

// EDIT
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

// CLEAR COMPLETED
const clearCompleted = async () => {
  await fetch(
    "https://todo-app-hi0d.onrender.com/todos/completed",
    {
      method: "DELETE"
    }
  )

  fetchTodos()
}

onMounted(fetchTodos)
</script>

<template>
  <div class="container">
    <h1>Todo App</h1>

    <p>Total: {{ todos.length }}</p>

    <p>
      Completed:
      {{ todos.filter(t => t.completed).length }}
    </p>

    <input v-model="newTodo" @keyup.enter="addTodo" />

    <button @click="addTodo">Add</button>

    <ul>
      <li
        v-for="todo in todos"
        :key="todo.id"
        :style="{ textDecoration: todo.completed ? 'line-through' : '' }"
      >
        {{ todo.task }}

        <button @click="toggleComplete(todo.id)">✔️</button>
        <button @click="editTodo(todo.id, todo.task)">✏️</button>
        <button @click="deleteTodo(todo.id)">❌</button>
      </li>
    </ul>

    <button @click="clearCompleted">Clear Completed</button>
  </div>
</template>

<style>
body {
  font-family: Arial;
  background: #111;
  color: white;
}

.container {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  background: #222;
  border-radius: 10px;
}

input {
  padding: 10px;
  width: 70%;
}

button {
  margin: 5px;
  padding: 8px;
  cursor: pointer;
}
</style>