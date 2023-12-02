import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Main, Login } from './page/home/Home';


function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Main />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;