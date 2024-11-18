import {useEffect, useRef} from "react";
import {axiosLoadData} from "../api/axios.ts";

function NaverMap() {
    const mapRef = useRef(null);
    const lat = 37.3595704// 위도 숫자로 넣어주기
    const lng = 127.105399// 경도 숫자로 넣어주기

    const loadData = async () => {
        return await axiosLoadData()
    }

    useEffect(() => {
        const { naver } = window;
        loadData().then(r => console.log(r))
        if (mapRef.current && naver) {
            const location = new naver.maps.LatLng(lat, lng);
            const map = new naver.maps.Map(mapRef.current, {
                center: location,
                zoom: 15, // 지도 확대 정도
                scaleControl: true,
                mapDataControl: true,
                mapTypeControl: true,
                zoomControl: true,
                disableKineticPan: false,
                tileSpare: 6
            });

            navigator.geolocation.getCurrentPosition((position) => {
                map.panTo(new naver.maps.LatLng(position.coords.latitude, position.coords.longitude))
            })

        }
    }, []);


    return (
        <>
            <div ref={mapRef} style={{width: "100%", height: "100%"}}></div>
        </>

    );
}

export default NaverMap