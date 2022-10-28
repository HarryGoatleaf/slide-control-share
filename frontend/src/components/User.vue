<script>
export default {
    props: ['name', 'id'],
}
</script>

<template>
    <p><strong>User:</strong> {{name}}#{{id}}</p>
</template>