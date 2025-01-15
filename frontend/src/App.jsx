import { Route, Routes, BrowserRouter } from "react-router-dom";
import QuizApp from "./components/QuizApp";
import Home from "./components/Home";
import QuizList from "./components/QuizList";
// import QuizResults from "./components/QuizResults";
import Login from "./components/Login";
import Register from "./components/Register"
import QuizResult from "./components/QuizResult";
// import PrivateRoute from "./components/PrivateRoute";


function App() {

  return (
    <>
      <h1 className="text-red-500 text-5xl text-center">Proxima</h1>
      
      <BrowserRouter>
          <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/register" element={<Register />} />
              <Route path="/login" element={<Login />} />
              <Route path="/quiz/" element={<QuizList />} />
              <Route path="/quiz/:id" element={<QuizApp />} />
              <Route path="/result/" element={<QuizResult />} />

              {/* <Route path="/quiz-result/" element={<QuizResults />} /> */}
          </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
