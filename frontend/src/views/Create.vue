<script>
import {store} from '../store.js'
import {backend} from '../backend.js'

export default {
  data() {
    return {
      store,
      input_slides: undefined,
    };
  },

  methods: {
    onSubmit(e){
      e.preventDefault();
      // load file
      var reader = new FileReader()
      reader.readAsDataURL(this.input_slides)
      reader.onload = () => {

        // create presentation creation message object
        // var message = {content: , slides: this.input_slides}
        const form = new FormData();
        form.append('slides', this.input_slides)

        backend.post('/presentation/create', form, {headers: {'Content-Type': 'multipart/form-data'}})
          .then(res => {
            console.log(res)
            this.store.presentation = res.data.presentation
            // navigate to newly created presentation
            this.$router.push({path: '/presentation/' + this.store.presentation.id})
          })
          .catch((error) => {
            console.log(error)
          });

      }
      reader.onerror = () => {
        console.log(reader.error)
      }

    },
  },

  created() {
    // redirect to hello page if user is unknown to server
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

<div id="wrapper">
  <div id="content">

    <h1>Create Session</h1>

    <form @submit="onSubmit">

    <label for="slides">PDF File: </label>
    <br>
    <input
      type="file"
      name="slides"
      accept=".pdf"
      @change="event => input_slides = event.target.files[0]">
    <br>
    <input type="submit" value="Start!"/>
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