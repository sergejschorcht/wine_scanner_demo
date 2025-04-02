import Image from 'next/image'

export default function Home() {
  return (
      <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-red-900 to-purple-900 p-24">
        <div className="relative flex flex-col items-center justify-center">
          {/* Wine icon */}
          <div className="mb-8">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="80"
                height="80"
                viewBox="0 0 24 24"
                fill="none"
                stroke="rgba(255,255,255,0.9)"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
            >
              <path d="M8 22h8"></path>
              <path d="M12 11v11"></path>
              <path d="M12 11a5 5 0 0 0 5-5c0-2-.5-4-2-8H9c-1.5 4-2 6-2 8a5 5 0 0 0 5 5z"></path>
            </svg>
          </div>

          {/* Main title */}
          <h1 className="text-5xl md:text-7xl font-bold text-center text-white mb-4 tracking-wide">
            Wine Scanner Demo
          </h1>

          {/* Decorative underline */}
          <div className="h-1 w-48 bg-white opacity-50 rounded-full mb-8"></div>

          {/* Subtle caption */}
          <p className="text-white text-opacity-80 text-xl text-center max-w-md">
            Discover wine details with a simple scan
          </p>
        </div>
      </main>
  )
}