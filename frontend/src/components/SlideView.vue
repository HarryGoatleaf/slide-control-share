<script setup>
import * as slides from '../slides.js'

const props = defineProps(['slide_num', 'render_scale'])

async function render_to_canvas(canvas, slide_num, render_scale) {
    // Get canvas context
    let context = canvas.getContext("2d");
    console.log('fetch page')

    var page = await slides.pdf.getPage(slide_num)
    var viewport = page.getViewport({scale: render_scale});

    // Prepare canvas using PDF page dimensions
    // (this only sets the resolution of the canvas.
    //  not the size of the canvas on the page)
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    // Render PDF page into canvas context
    var renderContext = {
      canvasContext: context,
      viewport: viewport
    };

    await page.render(renderContext).promise
}

// this is the render queue (of size 1 ^^)
var queued_params = undefined
async function render_queue(canvas) {
  while(queued_params !== undefined) {
    // pop queue
    let slide_num = queued_params.slide_num;
    let render_scale = queued_params.render_scale;
    queued_params = undefined;

    await render_to_canvas(canvas, slide_num, render_scale)
  }
}

var render_busy = false
const vDisplaySlide = (canvas, binding) => {
    console.log('v binding call')
    if(slides.slides_available.value == false) {
      console.log('slides not available')
      return;
    }

    // add requested page params to queue
    queued_params = binding.value;

    // if render_queue is not already running => start it
    if(!render_busy) {
      render_busy = true;
      render_queue(canvas)
      .then(() => {
        render_busy = false;
      })
      .catch((reason) => console.log(reason));
    }

}
</script>

<template>
<div class="slide-container">
  <canvas v-if="slides.slides_available.value" v-display-slide="{slide_num: slide_num, render_scale: render_scale}"></canvas>
</div>
</template>

<style scoped>
.slide-container {
  display: block;
  overflow: hidden;
  position: relative;
  text-align: center;
  height:100%;
  width: 100%;
}

canvas {
  bottom: 0;
  left: 0;
  right: 0;
  top: 0;
  margin: auto;
  max-height: 100%;
  max-width: 100%;
  position: absolute;
}
</style>