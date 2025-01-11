<template>
  <div>
    <input v-model="newItem" placeholder="Enter item name" />
    <button @click="addItem">Add Item</button>
    <ul>
      <li v-for="item in items" :key="item.id">{{ item.name }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newItem: '',
      items: [],
    };
  },
  methods: {
    fetchItems() {
      axios.get('/items').then((response) => {
        this.items = response.data;
      });
    },
    addItem() {
      axios.post('/items', { name: this.newItem }).then(() => {
        this.newItem = '';
        this.fetchItems();
      });
    },
  },
  mounted() {
    this.fetchItems();
  },
};
</script>
