<script setup>
const props = defineProps(['name', 'id'])
</script>

<template>
    <p><strong>User:</strong> {{name}}#{{id}}</p>
</template>