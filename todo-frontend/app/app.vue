<script setup>
import { ref, onMounted } from 'vue'

const todos = ref([])
const newTodo = ref("")

const fetchTodos = async () => {
  const res = await fetch("http://127.0.0.1:8000/todos")
  todos.value = await res.json()
}

const addTodo = async () => {
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

  await fetch(`http://127.0.0.1:8000/todos/${id}?item=${newText}`, {
    method: "PUT"
  })

  fetchTodos()
}

onMounted(fetchTodos)
</script>

<template>
  <div style="padding:20px">
    <h1>Todo App</h1>

    <input v-model="newTodo" placeholder="Enter task" />
    <button @click="addTodo">Add</button>

    <ul>
      <li v-for="todo in todos" :key="todo[0]">
        {{ todo[1] }}
        <button @click="editTodo(todo[0], todo[1])">✏️</button>
        <button @click="deleteTodo(todo[0])">❌</button>
      </li>
    </ul>
  </div>
</template>
