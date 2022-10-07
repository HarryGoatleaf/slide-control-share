<script>
import {store} from '../store.js'
import {backend} from '../backend.js'
export default {

    data() {
        return {
            user_name: store.user_name,
            user_id: store.user_id,
        };
    },
    
    methods: {
        getName() {
            backend.get('/user/name')
                .then((res) => {
                    if(res.data.status == 'success') {
                        console.log(res)
                        store.user_name = res.data.user.name;
                        store.user_id = res.data.user.id;
                        this.user_id = store.user_id;
                        this.user_name = store.user_name;
                    } else if(res.data.message == 'unknown user') {
                        console.log(res)
                        this.$router.push({path: this.$route.fullPath + '/hello'})
                    }
                })
                .catch((error) => {
                    console.error(error)
                });
        }
    },
    
    created() {
        this.getName();
    },
}
</script>

<template>
<h1>Presentation</h1>
<p v-if="user_name !== undefined">{{user_name}}</p> 
</template>

<style>

</style>