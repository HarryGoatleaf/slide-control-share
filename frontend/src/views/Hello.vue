<script>
import {store} from '../store.js'
import {backend} from '../backend.js'

export default {
  data() {
    return {
      name: undefined
    };
  },
  methods: {
    onSubmit(e){
      e.preventDefault();
      backend.post('/user/name', {username: this.name})
        .then(res => {
          console.log(res)
          this.name = res.data.name;
          this.$router.push({path: '/' + this.$route.params.path})
        });
    },
    getName() {
      backend.get('/user/name')
        .then((res) => {
          if(res.data.status == 'success') {
            this.$router.push({path: '/' + this.$route.params.path})
          }
        })
        .catch((error) => {
          console.error(error)
        });
    }
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
  v-model="name">
<input type="submit"/>
</form>

</template>

<style scoped>
</style>