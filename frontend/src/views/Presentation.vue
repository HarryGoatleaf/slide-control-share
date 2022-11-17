<script>
import { store } from '../store.js'
import * as slides from '../slides.js'
import { backend } from '../backend.js'
import { io } from 'socket.io-client'
import User from '../components/User.vue'
import SlideView from '../components/SlideView.vue'
import MultiSlideView from '../components/MultiSlideView.vue'

export default {
  data() {
    return {
      store,
      slides,
      sidebarVisible: false,
      presenter_view: false,
    };
  },

  computed: {
    presenter_view() {
      if(store.presentation === undefined) return false
      if(store.presentation.host.id === store.user.id) return true
      else return false
    }
  },

  components: {
    User,
    SlideView,
    MultiSlideView
  },

  methods: {
    // this is a higher order function that takes a function f:Int -> Int and
    // modifies the current slide according to f
    map_slide(f) {
      // calc new slide
      let new_slide = f(store.presentation.current_slide)

      // return if slide does not change under f
      if (new_slide === store.presentation.current_slide) {return}
      // check slide bounds
      if (store.presentation.num_slides < new_slide || new_slide < 1) {return}

      // modify local data
      store.presentation.current_slide = new_slide
      // send update to server
      backend.post('/presentation/' + this.store.presentation.id + '/current_slide',
        {new_slide: new_slide})
    },

    next_slide() {this.map_slide((i) => {return i+1})},
    prev_slide() {this.map_slide((i) => {return i-1})},
    next_label() {this.map_slide((i) => {
      if(!slides.has_next_label(i)) {return i}
      return slides.next_label_start(i)
    })},
    prev_label() {this.map_slide((i) => {
      if(!slides.has_prev_label(i)) {return i}
      return slides.prev_label_start(i)
    })},
  },

  created() {
    // register hotkeys
    console.log("register event handler")
    window.addEventListener('keydown', (e) => {
      if (e.key === ' ') {
        e.preventDefault();
        this.next_slide();
      } else if (e.key === 'Backspace') {
        e.preventDefault();
        this.prev_slide();
      }
    });

    // redirect if user does not exist
    this.store.load_user()
      .catch((msg) => {
        if (msg == 'unknown user') {
          this.$router.push(this.$route.fullPath + '/hello')
        }
      })

    // load presentation from url id
    // backend.get('/presentation/' + this.$route.params.url_presentation_id)
    this.store.get_presentation(this.$route.params.url_presentation_id)
      .then(presi => {
        // init socket after fetching url to guaratee that session (cookie) contains presentation_id
        const socket = io("http://127.0.0.1:5000", {
          withCredentials: true
          });

        // register SocketIO events
        // this event is emmited by the server if current_slide is updated
        socket.on('set_slide', (new_slide) => {
          // only call set_slide when slide counter changes.
          // if set_slide is called while another invocation of set_slide is unfinished we get bugs.
          //if(this.store.presentation.current_slide != new_slide) {
          //  this.store.presentation.current_slide = new_slide
          //  set_slide(store.presentation.current_slide)
          //}
          this.store.presentation.current_slide = new_slide;
        });
        // this event is emmited by the server if users join/leave
        socket.on('set_users', (new_presentation) => {
          this.store.presentation = new_presentation
        });
        socket.on("connect_error", (error) => {
          console.log(error)
        });
      })
      .catch(res => {
        console.log(res)
      })
  },

  mounted() {
    // presentation slides url
    var slide_url = 'http://127.0.0.1:5000/api/presentation/'
      + this.$route.params.url_presentation_id
      + '/slides';
    slides.load_slides(slide_url);
  },
}
</script>

<template>
  <div id="container">
    <div id="sidebar">
      <div id="sidebarContent" v-if="sidebarVisible">
        <User
          v-for="user in store.presentation.users"
          :name="user.name"
          :id="user.id"
        />
      </div>
    </div>

    <div id="presentation-and-controls" v-if="slides.slides_available.value">
      <MultiSlideView v-if="presenter_view" :slide_num="store.presentation?.current_slide"/>
      <SlideView v-else :slide_num="store.presentation?.current_slide" :render_scale="5"/>

      <div id="controls">
        <button id="toggle-sidebar" @click="() => {sidebarVisible = !sidebarVisible}">T</button>

        <button
        @click="prev_label"
        :disabled="!slides.has_prev_label(store.presentation?.current_slide)">
          «
        </button>
        <button
        @click="prev_slide"
        :disabled="store.presentation.current_slide<=1">
          Prev
        </button>

        <div id="slide-counter">
          {{store.presentation.current_slide}}
        </div>

        <button
        @click="next_slide"
        :disabled="store.presentation.current_slide >= store.presentation.num_slides">
          Next
        </button>
        <button
        @click="next_label"
        :disabled="!slides.has_next_label(store.presentation?.current_slide)">
          »
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>

/*
css black magic:
https://stackoverflow.com/questions/28439310/scale-an-image-to-maximally-fit-available-space-and-center-it
*/
#container {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
}

#presentation-and-controls {
  height: 100%;
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

#controls {
  display: flex;
  justify-content: center;
  padding-top: 5px;
  padding-bottom: 5px;
}

#slide-counter {
  padding-left: 5px;
  padding-right: 5px;
}
#toggle-sidebar {
  position: absolute;
  left: 5px;
}
</style>