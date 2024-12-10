import {useEffect, useRef, useState, useCallback} from "react";
import {axiosGetDataBylocation} from "../api/axios.ts";
import type {Station} from "../types/map";

// 컴포넌트 외부로 분리
const getColorByGrade = (grade: string) => {
    const colors = {
        "1": "#2196F3",  // 파란색
        "2": "#4CAF50",  // 초록색
        "3": "#FFEB3B",  // 노란색
        "4": "#F44336",  // 빨간색
    } as const;
    return colors[grade as keyof typeof colors] ?? "#808080";
};

const getGradeText = (grade: string) => {
    const grades = {
        "1": "좋음",
        "2": "보통",
        "3": "나쁨",
        "4": "매우나쁨",
    } as const;
    return grades[grade as keyof typeof grades] ?? "정보없음";
};

const createInfoWindowContent = (station: Station) => `
    <div class="p-5 min-w-[350px] max-w-[350px] shadow-lg rounded-lg bg-white font-sans">
        <h3 class="m-0 mb-2.5 text-gray-800 text-lg font-semibold border-b-2 border-gray-100 pb-2.5">
            ${station.station_name}
        </h3>

        <div class="text-sm text-gray-600 leading-relaxed">
            <p class="my-1.5">
                <strong>측정소 주소:</strong> ${station.addr}
            </p>
            <p class="my-1.5">
                <strong>측정시간:</strong> ${new Date(station.data_time).toLocaleString()}
            </p>
            <div class="mt-4 pt-4 border-t border-gray-100">
                <div class="flex justify-between items-center my-1.5">
                    <span><strong>미세먼지(PM10):</strong> ${station.pm10_value} ㎍/㎥</span>
                    ${station.pm10_flag ? `<span class="text-xs text-red-500">${station.pm10_flag}</span>` : ''}
                    <span class="px-2 py-1 rounded text-xs text-white" style="background-color: ${getColorByGrade(station.pm10_grade)}">
                        ${getGradeText(station.pm10_grade)}
                    </span>
                </div>
                <div class="flex justify-between items-center my-1.5">
                    <span><strong>초미세먼지(PM2.5):</strong> ${station.pm2_5_value} ㎍/㎥</span>
                    ${station.pm2_5_flag ? `<span class="text-xs text-red-500">${station.pm2_5_flag}</span>` : ''}
                    <span class="px-2 py-1 rounded text-xs text-white" style="background-color: ${getColorByGrade(station.pm2_5_grade)}">
                        ${getGradeText(station.pm2_5_grade)}
                    </span>
                </div>
                <div class="flex justify-between items-center my-1.5">
                    <span><strong>통합대기환경지수:</strong> ${station.khai_value}</span>
                    <span class="px-2 py-1 rounded text-xs text-white" style="background-color: ${getColorByGrade(station.khai_grade)}">
                        ${getGradeText(station.khai_grade)}
                    </span>
                </div>
            </div>
        </div>
    </div>
`;


function NaverMap() {
    const mapRef = useRef<HTMLDivElement>(null);
    const [mapInstance, setMapInstance] = useState<naver.maps.Map | null>(null);
    const [markers, setMarkers] = useState<naver.maps.Marker[]>([]);
    const [data, setData] = useState<Station[]>([]);
    const [currentLocation, setCurrentLocation] = useState({
        lat: 37.3595704,
        lng: 127.105399
    });
    const [infoWindow, setInfoWindow] = useState<naver.maps.InfoWindow | null>(null);

    const loadData = useCallback(async (lat: number, lng: number) => {
        try {
            const radius = mapInstance?.getZoom() <= 10 ? 40000 : 20000;
            const response = await axiosGetDataBylocation(lat, lng, radius);
            setData(response.data);
        } catch (error) {
            console.error('데이터 로딩 실패:', error);
        }
    }, [mapInstance]);

    useEffect(() => {
        if (currentLocation.lat && currentLocation.lng) {
            setTimeout(()=>loadData(currentLocation.lat, currentLocation.lng), 200);
        }
    }, [currentLocation, loadData]);

    useEffect(() => {
        const { naver } = window;
        if (mapRef.current && naver) {
            const location = new naver.maps.LatLng(currentLocation.lat, currentLocation.lng);
            const map = new naver.maps.Map(mapRef.current, {
                center: location,
                zoom: 14,
                tileTransition: true,
                scaleControl: true,
                mapDataControl: true,
                mapTypeControl: true,
                zoomControl: false,
                disableKineticPan: false,
                tileSpare: 6
            });

            setMapInstance(map);

            // 지도 중심 좌표 변경 이벤트
            naver.maps.Event.addListener(map, 'dragend', () => {
                const center = map.getCenter();
                setCurrentLocation({
                    lat: center.lat(),
                    lng: center.lng()
                });
            });

            // 줌 변경 완료 이벤트
            naver.maps.Event.addListener(map, 'zoom_changed', () => {
                const center = map.getCenter();
                setCurrentLocation({
                    lat: center.lat(),
                    lng: center.lng()
                });
            });
        }
    }, []);

    useEffect(() => {
        if (mapInstance && data.length > 0) {
            markers.forEach(marker => marker.setMap(null));

            const { naver } = window;
            const info = new naver.maps.InfoWindow({
                content: '',
                backgroundColor: "#fff",
                borderWidth: 0,
                borderColor: "transparent",
                pixelOffset: new naver.maps.Point(0, -10)
            });

            const newMarkers = data.map(station => {
                const marker = new naver.maps.Marker({
                    position: new naver.maps.LatLng(station.latitude, station.longitude),
                    map: mapInstance,
                    icon: {
                        content: `
                            <div class="w-[30px] h-[30px] rounded-full border-[3px] border-white shadow-[0_2px_6px_rgba(0,0,0,0.3)]" 
                                 style="background-color: ${getColorByGrade(station.khai_grade)}">
                            </div>
                        `,
                        anchor: new naver.maps.Point(15, 15)
                    }
                });

                naver.maps.Event.addListener(marker, 'click', () => {
                    // 먼저 마커 위치로 부드럽게 이동
                    mapInstance.panTo(new naver.maps.LatLng(station.latitude, station.longitude), {
                        duration: 300,
                        easing: 'easeOutCubic'
                    });

                    setTimeout(() => {
                        // 줌 레벨 조정이 필요한 경우
                        if (mapInstance.getZoom() < 13) {
                            mapInstance.setZoom(14, {
                                animate: true,
                                duration: 200
                            });

                            // 줌 애니메이션이 완료된 후 InfoWindow 열기
                            setTimeout(() => {
                                info.setContent(createInfoWindowContent(station));
                                info.open(mapInstance, marker);
                            }, 400);
                        } else {
                            // 줌 조정이 필요없는 경우 바로 InfoWindow 열기
                            info.setContent(createInfoWindowContent(station));
                            info.open(mapInstance, marker);
                        }
                    }, 400);
                });

                return marker;
            });

            setMarkers(newMarkers);

            // 지도 클릭시 정보창 닫기
            naver.maps.Event.addListener(mapInstance, 'click', () => {
                info.close();
            });
        }
    }, [mapInstance, data]);

    // 현재 위치를 가져오는 함수
    const getCurrentLocation = useCallback(() => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    setCurrentLocation({
                        lat: latitude,
                        lng: longitude
                    });

                    // 지도가 존재하면 현재 위치로 부드럽게 이동
                    if (mapInstance) {
                        mapInstance.panTo(new naver.maps.LatLng(latitude, longitude), {
                            duration: 500,
                            easing: 'easeOutCubic'
                        });
                    }
                },
                (error) => {
                    console.error('위치 정보를 가져오는데 실패했습니다:', error);
                    alert('위치 정보를 가져오는데 실패했습니다. 위치 권한을 확인해주세요.');
                }
            );
        } else {
            alert('이 브라우저에서는 위치 정보를 지원하지 않습니다.');
        }
    }, [mapInstance]);

    // 컴포넌트 마운트 시 현재 위치 가져오기
    useEffect(() => {
        getCurrentLocation();
    }, [mapInstance]);

    return (
        <div className="relative w-full h-full">
            <div ref={mapRef} style={{width: "100%", height: "100%"}}></div>
            
            {/* 현위치 버튼 */}
            <button
                onClick={getCurrentLocation}
                className="absolute bottom-6 right-6 bg-white rounded-full p-3 shadow-lg hover:bg-gray-100 transition-colors duration-200"
                aria-label="내 위치로 이동"
            >
                <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    strokeWidth={1.5} 
                    stroke="currentColor" 
                    className="w-6 h-6 text-gray-700"
                >
                    <path 
                        strokeLinecap="round" 
                        strokeLinejoin="round" 
                        d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" 
                    />
                    <path 
                        strokeLinecap="round" 
                        strokeLinejoin="round" 
                        d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" 
                    />
                </svg>
            </button>
        </div>
    );
}

export default NaverMap