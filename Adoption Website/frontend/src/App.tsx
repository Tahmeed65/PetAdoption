import { useState, useEffect } from 'react'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { Container, Navbar, Nav, Form } from 'react-bootstrap';
import axios from 'axios'
import Cookies from 'js-cookie'
import Pets from './Pets'
import Questionnaire from './Questionnaire'
import ApproveAdoption from './ApproveAdoption';
import ApproveQuestionnaire from './ApproveQuestionnaire';
import Home from './Home';


function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post("http://localhost:5002/api/basicauth/login", { username: username, password: password }).then(
      response => {
        if (response.data.authenticated) {
          Cookies.set("session_id", response.data.session_id);
          Cookies.set("name", response.data.name);
          Cookies.set("user_id", response.data.user_id);

          alert("logged in!");
          navigate('/')
        }
        else {
          alert("incorrect password");
        }
      }).catch(error => { console.error(error) });
  }
  return (
    <div className="loginpage">
      <div className="loginpageelements">
        <h1>LOGIN PAGE</h1>
        <Form onSubmit={handleSubmit} className="buttons">
          <Form.Group controlId="formUsername" className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </Form.Group>

          <Form.Group controlId="formPassword" className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </Form.Group>

          <button className="betterbutton" type="submit">
            Login
          </button>
        </Form>
      </div>
    </div>
  );
}

function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    Cookies.remove("session_id");
    Cookies.remove("name");
    Cookies.remove("user_id");
    // alert("logged out!");
    navigate('/');
  }, [navigate]);

  return null;
}

function App() {
  return (
    <Router>
      <div>
        <Navbar bg="black" variant="dark" expand="lg">
          <Container>
            <Navbar.Brand as={Link} to="/">PetFinder</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                <Nav.Link as={Link} to="/login">Login</Nav.Link>
                <Nav.Link as={Link} to="/logout">Logout</Nav.Link>
                <Nav.Link as={Link} to="/questionnaire">Questionnaire</Nav.Link>
                <Nav.Link as={Link} to="/pets">Pets</Nav.Link>
                <Nav.Link as={Link} to="/approve-adoption">Approve Adoption</Nav.Link>
                <Nav.Link as={Link} to="/approve-questionnaire">Approve Questionnaire</Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
        <Container className="mt-3">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="/questionnaire" element={<Questionnaire />} />
            <Route path="/pets" element={<Pets />} />
            <Route path="/approve-adoption" element={<ApproveAdoption />} />
            <Route path="/approve-questionnaire" element={<ApproveQuestionnaire />} />
          </Routes>
        </Container>
      </div>
    </Router>
  );
}

export default App
