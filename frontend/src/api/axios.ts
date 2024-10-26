import axios from "axios";

const instance = axios.create({
    baseURL: "/api",
    withCredentials: true,
    timeout: 15000
});

export const axiosLoadData = async () => {
    try {
        const response = await instance.get("/loadData", {
        });
        return response;
    } catch (error) {
        throw error;
    }

}