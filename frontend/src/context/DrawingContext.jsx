import { createContext, useContext, useMemo, useState, useCallback } from 'react'

const DrawingContext = createContext(null)

export function DrawingProvider({ children }) {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [drawingId, setDrawingId] = useState(null)
  const [result, setResult] = useState(null)

  const selectFile = useCallback((selected) => {
    setFile(selected)
    setPreviewUrl(selected ? URL.createObjectURL(selected) : null)
    setDrawingId(null)
    setResult(null)
  }, [])

  const reset = useCallback(() => {
    setFile(null)
    setPreviewUrl(null)
    setDrawingId(null)
    setResult(null)
  }, [])

  const value = useMemo(
    () => ({
      file,
      previewUrl,
      drawingId,
      setDrawingId,
      result,
      setResult,
      selectFile,
      reset,
    }),
    [file, previewUrl, drawingId, result, selectFile, reset]
  )

  return <DrawingContext.Provider value={value}>{children}</DrawingContext.Provider>
}

export function useDrawing() {
  const ctx = useContext(DrawingContext)
  if (!ctx) throw new Error('useDrawing must be used within a DrawingProvider')
  return ctx
}
