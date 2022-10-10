<script>
import {store} from '../store.js'
import {backend} from '../backend.js'
import { io } from 'socket.io-client'
import User from '../components/User.vue'

export default {
  data() {
    return {
      store,
    };
  },
  
  components: {
    User
  },

  methods: {
    next_slide() {
      store.presentation.current_slide++
      backend.post('/presentation/' + this.store.presentation._id.$oid + '/current_slide', 
        {new_slide: store.presentation.current_slide})
    },

    prev_slide() {
      store.presentation.current_slide--
      backend.post('/presentation/' + this.store.presentation._id.$oid + '/current_slide', 
        {new_slide: store.presentation.current_slide})
    }
  },

  created() {
    // redirect if user does not exist
    this.store.load_user()
      .then(() => {

      })
      .catch((msg) => {
        if (msg == 'unknown user') {
          this.$router.push(this.$route.fullPath + '/hello')
        }
      })
    
    // load presentation from url id
    backend.get('/presentation/' + this.$route.params.url_presentation_id)
      .then(res => {
        this.store.presentation = JSON.parse(res.data.presentation)

        // init socket after fetching url to guaratee that session (cookie) contains presentation_id
        const socket = io("http://127.0.0.1:5000", {
          withCredentials: true
          });
          
        // this event is emmited by the server if current_slide is updated
        socket.on('set_slide', (new_slide) => {
          this.store.presentation.current_slide = new_slide
        });
        
        // this event is emmited by the server if users join/leave
        socket.on('set_users', (new_users) => {
          var new_presentation = JSON.parse(new_users)
          console.log(new_presentation)
          this.store.presentation = new_presentation
        });
        
        socket.on("connect_error", (error) => {
          console.log(error)
        });
      })
      .catch(res => {
      })
  },
}
</script>

<template>
  <h1>Presentation</h1>
  <p v-if="store.user?.name !== undefined"> Username: {{store.user.name}} </p>
  <div v-if="store.presentation !== undefined">
    <p>Content: {{store.presentation.content}} </p> 

    <button @click="prev_slide">Prev</button>
    {{store.presentation.current_slide}}
    <button @click="next_slide">Next</button>
    
    <User 
      v-for="user in store.presentation.users"
      :name="user.$oid"
    />
  </div>

</template>

<style>

</style>