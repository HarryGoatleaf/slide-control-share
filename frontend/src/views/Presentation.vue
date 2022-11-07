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
function set_slide(slide_num) {
  if(slides === undefined) return

  slides.getPage(slide_num).then((page) => {
    console.log('Page loaded');

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
      console.log('Page rendered');
    });
  });
}


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
      // do nothing if on last page
      if (store.presentation.current_slide >= store.presentation.num_slides) {return}

      store.presentation.current_slide++
      backend.post('/presentation/' + this.store.presentation.id + '/current_slide',
        {new_slide: store.presentation.current_slide})
      set_slide(store.presentation.current_slide)
    },

    prev_slide() {
      // do nothing if on first page
      if (store.presentation.current_slide <= 1) {return}

      store.presentation.current_slide--
      backend.post('/presentation/' + this.store.presentation.id + '/current_slide',
        {new_slide: store.presentation.current_slide})
      set_slide(store.presentation.current_slide)
    },
  },

  created() {
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
      console.log('PDF loaded');
      slides = pdf
      set_slide(store.presentation.current_slide)
    }, function (reason) {
      // PDF loading error
      console.error(reason);
    });
  },
}
</script>

<template>

  <div id="presentation">
    <canvas id="the-canvas"></canvas>
  </div>

  <div id="footer">
    <div v-if="store.presentation !== undefined">
      <button
      @click="prev_slide"
      :disabled="store.presentation.current_slide<=1">
        Prev
      </button>

      {{store.presentation.current_slide}}

      <button
      @click="next_slide"
      :disabled="store.presentation.current_slide >= store.presentation.num_slides">
        Next
      </button>

      <User
        v-for="user in store.presentation.users"
        :name="user.name"
        :id="user.id"
      />
    </div>
  </div>
</template>

<style scoped>

/*
css black magic:
https://stackoverflow.com/questions/28439310/scale-an-image-to-maximally-fit-available-space-and-center-it
*/

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
#footer {
}
</style>