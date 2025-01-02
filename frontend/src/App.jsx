import { Route, Routes, BrowserRouter } from "react-router-dom";
import QuizApp from "./components/QuizApp";
import Home from "./components/Home";


function App() {

  return (
    <>
      <h1 className="text-red-500 text-5xl text-center">Proxima</h1>
      
      <BrowserRouter>
          <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/quiz/" element={<QuizApp />} />
          </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
