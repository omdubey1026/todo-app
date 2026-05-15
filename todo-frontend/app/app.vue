<script setup>
import { ref, onMounted } from 'vue'

const todos = ref([])
const newTodo = ref("")

const fetchTodos = async () => {
  const res = await fetch("https://todo-app-hi0d.onrender.com/todos")
  todos.value = await res.json()
}

const addTodo = async () => {
  if (!newTodo.value) return

  await fetch(`https://todo-app-hi0d.onrender.com/todos?item=${newTodo.value}`, {
    method: "POST"
  })

  newTodo.value = ""
  fetchTodos()
}

const deleteTodo = async (id) => {
  await fetch(`https://todo-app-hi0d.onrender.com/todos/${id}`, {
    method: "DELETE"
  })
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
    <h1>Todo App</h1>

   <input v-model="newTodo" placeholder="Enter task" />

<<button @click="toggleComplete(todo[0])">
  ✔️
</button>

<ul>
  <li
  v-for="todo in todos"
  :key="todo[0]"
  :style="{
    textDecoration: todo[2] ? 'line-through' : 'none'
  }"
>
    {{ todo[1] }}

    <button @click="editTodo(todo[0], todo[1])">
      ✏️
    </button>

    <button @click="deleteTodo(todo[0])">
      ❌
    </button>
  </li>
</ul>

  </div>
</template>
<style>
body {
  font-family: Arial, sans-serif;
  background: #f4f4f4;
}

.container {
  max-width: 500px;
  margin: 50px auto;
  background: white;
  padding: 20px;
  border-radius: 10px;
}

h1 {
  text-align: center;
}

input {
  padding: 10px;
  width: 70%;
  margin-right: 10px;
}

button {
  padding: 10px;
  cursor: pointer;
}

li {
  margin-top: 10px;
}
</style>