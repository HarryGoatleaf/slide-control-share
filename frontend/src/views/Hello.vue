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


<div id="wrapper">
  <div id="content">
    <h1>Hello!</h1>
    <form @submit="onSubmit" id="form">
    <input
      type="text"
      name="username"
      placeholder="name"
      autofocus
      v-model="input_name">
    <input type="submit" value="go!"/>
    </form>
  </div>
</div>

</template>

<style scoped>
#wrapper {
  display: flex;
  height: 100%;
  flex-direction: row;
  justify-content: center;
  padding-top: 20%;
}

h1 {
  text-align: center;
}
</style>