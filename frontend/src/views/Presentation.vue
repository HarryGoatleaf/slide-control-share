<script>
import {store} from '../store.js'
import {backend} from '../backend.js'
import { io } from 'socket.io-client'
import User from '../components/User.vue'
// TODO: why is await necessary here?
const pdfjsLib = await import('pdfjs-dist/build/pdf')
// TODO: this could break
pdfjsLib.GlobalWorkerOptions.workerSrc =
  'https://cdn.jsdelivr.net/npm/pdfjs-dist@2.16.105/build/pdf.worker.min.js';

// TODO: is this ugly?
var slides = undefined;
var labels = undefined;
// TODO: maybe this could become a closure?
function get_label(i) {
  if (labels !== undefined) {
    //
    return labels[i-1]
  } else {
    return i
  }
}

function set_slide(slide_num) {
  if(slides === undefined) return

  slides.getPage(slide_num).then((page) => {
    var scale = 5;
    var viewport = page.getViewport({scale: scale});

    // Prepare canvas using PDF page dimensions
    var canvas = document.getElementById('the-canvas');
    var context = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    // Render PDF page into canvas context
    var renderContext = {
      canvasContext: context,
      viewport: viewport
    };
    var renderTask = page.render(renderContext);
    renderTask.promise.then(() => {
      // console.log('Page rendered');
    });
  });
}

export default {
  data() {
    return {
      store,
      sidebarVisible: false,
      hotkeys_registered: false,
      last_label_start: undefined,
      first_label_end: undefined,
    };
  },

  components: {
    User
  },

  methods: {
    register_hotkeys() {
      if(this.hotkeys_registered) {return}
      this.hotkeys_registered = true;
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
    },

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
      // render new page
      set_slide(new_slide)
    },

    next_slide() {this.map_slide((i) => {return i+1})},
    prev_slide() {this.map_slide((i) => {return i-1})},
    next_label() {this.map_slide((i) => {
      if(!this.has_next_label(i)) {return i}
      let res = i
      while(get_label(res) === get_label(i) && i < this.store.presentation.num_slides) {res++}
      return res
    })},
    prev_label() {this.map_slide((i) => {
      if(!this.has_next_label(i)) {return i}
      let res = i
      while(get_label(res) === labels[i-1] && i > 1) {res--}
      return res
    })},

    // helper methods
    has_next_label(i) {
      if(i === undefined) {return false}
      if(this.last_label_start === undefined) {return false}
      return i < this.last_label_start
    },
    has_prev_label(i) {
      if(i === undefined) {return false}
      if(this.first_label_end === undefined) {return false}
      return this.first_label_end < i
    },

  },

  created() {
    this.register_hotkeys();

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
        console.log(presi)

        // init socket after fetching url to guaratee that session (cookie) contains presentation_id
        const socket = io("http://127.0.0.1:5000", {
          withCredentials: true
          });

        // this event is emmited by the server if current_slide is updated
        socket.on('set_slide', (new_slide) => {
          // only call set_slide when slide counter changes.
          // if set_slide is called while another invocation of set_slide is unfinished we get bugs.
          if(this.store.presentation.current_slide != new_slide) {
            this.store.presentation.current_slide = new_slide
            set_slide(store.presentation.current_slide)
          }
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

    // asynchronous download of PDF
    var loadingTask = pdfjsLib.getDocument({url: slide_url,withCredentials: true});
    loadingTask.promise.then(pdf => {
      // console.log('PDF loaded');
      //pdf.getDestinations().then(labels => {console.log("info: "); console.log(labels);})
      slides = pdf

      // this resolves with null if the pdf has no labels
      pdf.getPageLabels().then(lbl => {
        if(lbl !== null) {
          labels = lbl;
          // serch for last label start
          let last_label = get_label(store.presentation.num_slides)
          let lls = store.presentation.num_slides;
          while (get_label(lls-1) === last_label && lls > 1) {
            lls--
          }
          this.last_label_start = lls
          // search for first label end
          let first_label = get_label(1)
          let fle = 1
          while(get_label(fle-1) === first_label && fle < store.presentation.num_slides) {
            fle++
          }
          this.first_label_end = fle
        } else {
          // every slide has its own label
          this.first_label_end = 1
          this.last_label_start = store.presentation.num_slides
        }
      })
      set_slide(store.presentation.current_slide)
    }, function (reason) {
      // PDF loading error
      console.error(reason);
    });
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

    <div id="presentation-and-controls">
      <div id="presentation">
        <canvas id="the-canvas"></canvas>
      </div>

      <div id="controls">
        <button id="toggle-sidebar" @click="() => {sidebarVisible = !sidebarVisible}">T</button>

        <button
        @click="prev_label"
        :disabled="!has_prev_label(store.presentation?.current_slide)">
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
        :disabled="!has_next_label(store.presentation?.current_slide)">
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

#presentation {
  display: block;
  overflow: hidden;
  position: relative;
  text-align: center;
  height:100%;
  width: 100%;
}
#the-canvas {
  bottom: 0;
  left: 0;
  right: 0;
  top: 0;
  margin: auto;
  max-height: 100%;
  max-width: 100%;
  position: absolute;
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