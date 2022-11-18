import axios from 'axios'

export const backend = axios.create({
    withCredentials: true,
    baseURL: import.meta.env.VITE_BACKEND_URL + '/api',
})