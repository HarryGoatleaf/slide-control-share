<script>
import {store} from '../store.js'
import {backend} from '../backend.js'

export default {

  data() {
    return {
      store
    };
  },

  methods: {
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
  },
}
</script>

<template>
  <h1>Presentation</h1>
  <p v-if="store.user?.name !== undefined">{{store.user.name}}</p>
</template>

<style>

</style>