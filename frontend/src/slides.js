import {ref} from 'vue'
const pdfjsLib = await import('pdfjs-dist/build/pdf')
// TODO: this could break
pdfjsLib.GlobalWorkerOptions.workerSrc =
  'https://cdn.jsdelivr.net/npm/pdfjs-dist@2.16.105/build/pdf.worker.min.js';

export var pdf = undefined
export const slides_available = ref(false)

// keep labels private and only export getter
var labels = undefined
export var first_label_end = undefined
export var last_label_start = undefined
export const labels_available = ref(false)

export function get_label(x) {
  if (labels !== undefined) {
    return labels[x-1]
  } else {
    return x
  }
}

// helper methods
export function get_label_start(x) {
  //if (!labels_available) throw "labels not yet available"
  if (x < 1 || pdf.numPages < x) throw "x out of pdf bounds"
  let res = x
  while (get_label(res-1) === get_label(x) && res > 1) res--
  return res
}
export function get_label_end(x) {
  //if (!labels_available) throw "labels not yet available"
  if (x < 1 || pdf.numPages < x) throw "x out of pdf bounds"
  let res = x
  while (get_label(res+1) === get_label(x) && res < pdf.numPages) res++
  return res
}

export function has_next_label(x) {
  if(x === undefined) {return false}
  if(!labels_available) {return false}
  return x < last_label_start
}
export function has_prev_label(i) {
  if(i === undefined) {return false}
  if(!labels_available) {return false}
  return first_label_end < i
}

export function next_label_start(x) {
  if(x === undefined) return x
  if(!has_next_label(x)) return x

  return get_label_end(x) + 1
}
export function prev_label_end(x) {
  if(x === undefined) return x
  if(!has_prev_label(x)) return x

  return get_label_start(x) - 1
}

export function next_label_end(x) {
  if(x === undefined) return x
  if(!has_next_label(x)) return x

  let nls = next_label_start(x)
  return get_label_end(nls)
}
export function prev_label_start(x) {
  if(x === undefined) return x
  if(!has_prev_label(x)) return x

  let ple = prev_label_end(x)
  return get_label_start(ple)
}

export function load_slides(slide_url) {
  return new Promise((resolve, reject) => {
    // asynchronous download of PDF
    var loadingTask = pdfjsLib.getDocument({url: slide_url,withCredentials: true});
    loadingTask.promise
      .then(file => {
        pdf = file
        slides_available.value = true
        console.log("loaded pdf")
        console.log(file)

        // this resolves with null if the pdf has no labels
        file.getPageLabels()
          .then(lbl => {
            if(lbl !== null) {
              labels = lbl;
              last_label_start = get_label_start(pdf.numPages)
              first_label_end = get_label_end(1)
            } else {
              // every slide has its own label
              first_label_end = 1
              last_label_start = store.presentation.num_slides
            }
            // labels_available tracks if the labels are *initialized*
            // but it does not signify if the labels come from the pdf or are copies of the slide numbers
            labels_available.value = true
            resolve()
          })
          .catch((reason) => reject(reason));
    })
    .catch((reason) => reject(reason));
  });
}
