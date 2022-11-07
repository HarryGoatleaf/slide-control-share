import { reactive } from 'vue'
import { backend } from './backend.js'

// global variables
export const store = reactive({
  user: undefined,
  presentation: undefined,
  slides: undefined,

  load_user() {
    return new Promise((resolve, reject) => {
      // if user already loaded immediately resolve
      if(this.user !== undefined) resolve()
      // otherwise fetch user data from backend
      backend.get('/user/name')
        .then((res) => {
          if (res.data.status == 'success') {
            this.user = res.data.user
            resolve()
          } else if (res.data.message == 'unknown user') {
            reject(res.data.message)
          }
        })
        .catch((error) => {
          console.error(error)
          reject(error)
        });
    });
  },

  get_presentation(presentation_id) {
    return new Promise((resolve, reject) => {
      // if presentation already loaded immediately resolve
      // if(this.presentation !== undefined) resolve(this.presentation)
      // otherwise fetch user data from backend
      backend.get('/presentation/' + presentation_id)
        .then((res) => {
          if (res.data.status == 'success') {
            this.presentation = res.data.presentation
            resolve(res.data.presentation)
          } else if (res.data.message == 'unknown user') {
            reject(res.data.message)
          }
        })
        .catch((error) => {
          console.error(error)
          reject(error)
        });
    });

  }
});