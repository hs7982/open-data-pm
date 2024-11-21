import axios from "axios";

const instance = axios.create({
    baseURL: "/api",
    withCredentials: true,
    timeout: 15000
});


export const axiosGetDataBylocation = async (lat:number, lon:number, radius:number) => {
    try {
        const response = await instance.get("/data?latitude="+lat+"&longitude="+lon+"&radius="+radius, {
        });
        return response;
    } catch (error) {
        throw error;
    }
}