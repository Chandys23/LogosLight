export default function LoadingSpinner({ message = 'Seeking wisdom...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 border-4 border-purple-500/20 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-transparent border-t-amber-400 border-r-purple-400 rounded-full animate-spin"></div>
      </div>
      <p className="text-purple-300/70 text-sm animate-pulse">{message}</p>
    </div>
  )
}
