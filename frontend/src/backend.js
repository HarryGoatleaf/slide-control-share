import axios from 'axios'

export const backend = axios.create({
    withCredentials: true,
    baseURL: import.meta.env.BACKEND_URL + '/api',
})