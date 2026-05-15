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
    <h1>Todo App</h1>
    <p>Total Tasks: {{ todos.length }}</p>

<p>
  Completed:
  {{
    todos.filter(todo => todo.completed).length
  }}
</p>

    <input
  v-model="newTodo"
  placeholder="Enter task"
  @keyup.enter="addTodo"
/>

    <button @click="addTodo">
      Add
    </button>

    <ul>
      <li
        v-for="todo in todos"
        :key="todo.id"
        :style="{
  textDecoration: todo.completed
    ? 'line-through'
    : 'none',
  color: todo.completed
    ? 'lightgreen'
    : 'white'
}"
      >
        {{ todo.task }}

        <button @click="toggleComplete(todo.id)">
          ✔️
        </button>
        const clearCompleted = async () => {
  await fetch(
    "https://todo-app-hi0d.onrender.com/todos/completed",
    {
      method: "DELETE"
    }
  )

  fetchTodos()
}


        <button @click="editTodo(todo.id, todo.task)">
          ✏️
        </button>

        <button @click="deleteTodo(todo.id)">
          ❌
        </button>
      </li>
      <button @click="clearCompleted">
  Clear Completed
</button>

    </ul>
  </div>
</template>

<style>
body {
  font-family: Arial, sans-serif;
  background: #121212;
  color: white;
}

.container {
  max-width: 500px;
  margin: 50px auto;
  background: #1e1e1e;
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
  background: #333;
  color: white;
  border: none;
}

button {
  padding: 10px;
  margin-left: 5px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
}

li {
  margin-top: 10px;
}
</style>