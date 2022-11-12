<script setup>
import SlideView from './SlideView.vue'
import * as slides from '../slides.js'
import {computed} from 'vue'

const props = defineProps(['slide_num'])

const prevSlideAvailable = computed(() => {return 1 < props.slide_num})
const nextSlideAvailable = computed(() => {return props.slide_num < slides.pdf.numPages})
const prevLabelAvailable = computed(() => {return slides.has_prev_label(props.slide_num)})
const nextLabelAvailable = computed(() => {return slides.has_next_label(props.slide_num)})
</script>

<template>
<div id="whole-container">
  <div id="center-container">
    <SlideView style="height: 70%" :slide_num="slide_num" :render_scale="5"/>
    <div id="lower-preview-container">
      <SlideView id="prev-slide" v-if="prevSlideAvailable" :slide_num="slide_num-1" :render_scale="2"/>
      <div style="width: 100%"></div>
      <SlideView id="next-slide" v-if="nextSlideAvailable" :slide_num="slide_num+1" :render_scale="2"/>
    </div>
  </div>
  <div id="side-preview-container">
      <h3>Next Page</h3>
      <SlideView v-if="nextLabelAvailable" :slide_num="slides.next_label_end(slide_num)" :render_scale="4"/>
      <div style="height: 100%"></div>
  </div>
</div>
</template>

<style scoped>
#whole-container {
  display: flex;
  flex-direction: row;
  height: 100%;
  width: 100%;
}

#center-container {
  width:70%;
  height:100%;
}

#side-preview-container {
  width: 30%;
}

#lower-preview-container {
  height: 30%;
  width:100%;
  display: flex;
  flex-direction: row;
}
</style>