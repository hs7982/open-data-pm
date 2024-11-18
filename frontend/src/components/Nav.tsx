function Nav() {

    return (
        <>
            <nav className="w-[1200px] absolute z-50 p-3 m-3 bg-white rounded-xl flex shadow-xl">
                <span className="text-2xl font-semibold text-sky-600 mx-auto">이게먼지?</span>
                <span className="my-auto end-5 top-4 absolute">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                     stroke="currentColor" className="size-6">
                    <path strokeLinecap="round" strokeLinejoin="round"
                          d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/>
                </svg>
                    </span>
            </nav>
        </>

    );
}

export default Nav
