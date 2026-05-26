export default function LoadingSpinner({ message = 'Loading...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4">
      <div className="animate-spin h-10 w-10 rounded-full border-4 border-divine-gold border-t-transparent" />
      <p className="text-gray-500 text-sm">{message}</p>
    </div>
  )
}
