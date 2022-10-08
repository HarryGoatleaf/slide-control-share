<script>
import {store} from '../store.js'
import {backend} from '../backend.js'

export default {
  data() {
    return {
      store,
      input_content: ''
    };
  },
  methods: {
    onSubmit(e){
      e.preventDefault();
      backend.post('/presentation/create', {content: this.input_content})
        .then(res => {
          console.log(res)
          this.$router.push({path: '/presentation/' + res.data.presentation})
        });
    },
  },
  created() {
    this.store.load_user()
      .then(() => {
      })
      .catch((msg) => {
        if (msg == 'unknown user') {
          this.$router.push(this.$route.fullPath + '/hello')
        }
      })
  }
}
</script>

<template>

<h1>Create</h1>

<form @submit="onSubmit">
<label for="content">Content</label>
<br>
<input
  type="text"
  name="content"
  v-model="input_content">
<input type="submit"/>
</form>

</template>

<style scoped>
</style>