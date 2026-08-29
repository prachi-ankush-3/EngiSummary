import { Routes, Route, Navigate } from 'react-router-dom'
import { DrawingProvider } from './context/DrawingContext.jsx'
import HomePage from './pages/HomePage.jsx'
import ProcessingPage from './pages/ProcessingPage.jsx'
import ResultPage from './pages/ResultPage.jsx'

export default function App() {
  return (
    <DrawingProvider>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/processing" element={<ProcessingPage />} />
        <Route path="/result" element={<ResultPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </DrawingProvider>
  )
}
