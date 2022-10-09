<script>
import {store} from '../store.js'
import {backend} from '../backend.js'

export default {
  data() {
    return {
      store,
      input_name: ''
    };
  },
  methods: {
    onSubmit(e){
      // prevent browser from reloading etc
      e.preventDefault();
      backend.post('/user/name', {username: this.input_name})
        .then(res => {
          console.log(res)
          this.$router.push({path: '/' + this.$route.params.path})
        });
    },
  },
  created() {
    this.store.load_user()
      .then(() => {
        // if user already is named autoredirect
        this.$router.push({path: '/' + this.$route.params.path})
      })
      .catch()
  }
}
</script>

<template>

<h1>Hello!</h1>

<form @submit="onSubmit">
<label for="username">Name</label>
<br>
<input
  type="text"
  name="username"
  v-model="input_name">
<input type="submit"/>
</form>

</template>

<style scoped>
</style>