<template>
  <div id="app">
    <h1>Flask-Vue Integration</h1>
    <ItemList />
  </div>
</template>

<script>
import ItemList from './components/ItemList.vue';

export default {
  components: {
    ItemList,
  },
};
</script>
