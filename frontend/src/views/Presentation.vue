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
    },
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
        console.log(res)
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

    mounted() {
      // somehow pdfjs has to be imported in this funky way
      import("pdfjs-dist/legacy/build/pdf.js")
      .then((pdfjsLib) => {
        // TODO: this could break
        pdfjsLib.GlobalWorkerOptions.workerSrc =
          "https://cdn.jsdelivr.net/npm/pdfjs-dist@2.16.105/build/pdf.worker.min.js";

        // presentation slides url
        var url = 'http://127.0.0.1:5000/api/presentation/'
          + this.$route.params.url_presentation_id 
          + '/slides';

        // Asynchronous download of PDF
        var loadingTask = pdfjsLib.getDocument({url: url,withCredentials: true});
        loadingTask.promise.then((pdf) => {
          console.log('PDF loaded');
          this.store.slides = pdf
          
          // fetch page
          var pageNumber = 1;
          pdf.getPage(pageNumber).then((page) => {
            console.log('Page loaded');
            
            var scale = 1.5;
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
            renderTask.promise.then(function () {
              console.log('Page rendered');
            });
          });
        }, function (reason) {
          // PDF loading error
          console.error(reason);
        });
      });
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
    <canvas id="the-canvas"></canvas>
  </div>

</template>

<style>

</style>