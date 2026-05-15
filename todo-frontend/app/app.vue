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
  background: #0f0f0f;
  color: #fff;
}

.container {
  max-width: 500px;
  margin: 50px auto;
  background: #1c1c1c;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0,0,0,0.5);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  color: #aaa;
}

.input-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  background: #333;
  color: white;
}

button {
  padding: 10px 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background: #4cafef;
  color: white;
  transition: 0.2s;
}

button:hover {
  opacity: 0.8;
}

ul {
  list-style: none;
  padding: 0;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #2a2a2a;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  transition: 0.2s;
}

.todo-item.done {
  text-decoration: line-through;
  opacity: 0.6;
}

.actions button {
  margin-left: 5px;
  background: #444;
}

.actions button:hover {
  background: #666;
}
</style>