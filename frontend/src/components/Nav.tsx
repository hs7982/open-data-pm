import React, { useState } from 'react';

function Nav() {
    const [isSearchMode, setIsSearchMode] = useState(false);

    return (
        <>
            <nav className="w-[1200px] absolute z-50 p-3 m-3 bg-white rounded-xl flex justify-between items-center shadow-xl">
                {!isSearchMode ? (
                    <>
                        <span className="text-2xl font-bold text-sky-600 flex-1 text-center">이게먼지?</span>
                        <button 
                            onClick={() => setIsSearchMode(true)}
                            className="hover:text-sky-600 transition-colors p-2 rounded-full hover:bg-sky-50"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                                stroke="currentColor" className="size-6">
                                <path strokeLinecap="round" strokeLinejoin="round"
                                    d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/>
                            </svg>
                        </button>
                    </>
                ) : (
                    <div className="w-full flex items-center gap-2">
                        <input
                            type="text"
                            placeholder="검색어를 입력하세요"
                            className="w-full px-4 py-2 outline-none rounded-lg focus:bg-gray-50"
                            autoFocus
                        />
                        <button 
                            onClick={() => setIsSearchMode(false)}
                            className="px-3 py-2 hover:text-sky-600 transition-colors rounded-lg hover:bg-sky-50 whitespace-nowrap"
                        >
                            취소
                        </button>
                    </div>
                )}
            </nav>
        </>
    );
}

export default Nav
