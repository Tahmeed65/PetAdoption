import { useState, useEffect } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button } from 'react-bootstrap';
import axios from 'axios'
import Cookies from 'js-cookie'
import { useNavigate } from 'react-router-dom';


function ApproveQuestionnaire() {
  const [admin, setAdmin] = useState(false);

  interface Questionnaire {
    userID: number;
    user_full_name: string;
    questionnaireID: number;
  }

  const [questionnaires, setQuestionnaires] = useState<Questionnaire[]>([]);

  // view is either main or detail
  const [view, setView] = useState("main");

  const adminID = Cookies.get("user_id");


  useEffect(() => {
    const target_url = `http://localhost:5002/api/is-admin/${adminID}`;
    axios.get(target_url)
      .then(response => {
        console.log(response);
        setAdmin(response.data);
      })
      .catch(error => {
        console.error("Error checking if user is admin:", error);
      });
  }, [adminID]);


  // Recieves questionnaire data
  useEffect(() => {
    axios.get('http://localhost:5002/api/questionnaire-queue')
      .then(response => {
        setQuestionnaires(response.data);
        console.log(response.data)
      })
      .catch(error => {
        console.error("Error getting questionnaires:", error);
      });
  }, []);

  const toggleView = () => {
    if (view === "main") setView("detail");
    else setView("main");
  }

  const [userFullName, setUserFullName] = useState('');

  interface UserResponse {
    question: string;
    response: string;
  }
  const [userResponses, setUserResponses] = useState<UserResponse[]>([]);

  const [userID, setUserID] = useState(0);

  const nav = useNavigate();

  // const [pet, setPetDescription] = useState('');

  const handleDetailButton = (index: number) => {
    setUserID(questionnaires[index].userID);
    setUserFullName(questionnaires[index].user_full_name);

    axios.get(`http://localhost:5002/api/questionnaire/${questionnaires[index].questionnaireID}`)
      .then((response) => {
        console.log(response);
        setUserResponses(response.data);
      })

    toggleView();
  }

  const handleAccept = (userID: number) => {
    axios.post(`http://localhost:5002/api/approve-questionnaire/${userID}`)
      .then(() => {
        alert("Success");
        toggleView();
        nav(0);
      })
      .catch(error => {
        alert("Error: " + error);
      });

  }

  const handleReject = (userID: number) => {
    axios.post(`http://localhost:5002/api/deny-questionnaire/${userID}`)
      .then(() => {
        alert("Success");
        toggleView();
        nav(0);
      })
      .catch(error => {
        alert("Error: " + error);
      });

  }

  return (
    <>
      {!admin && <>Only admins can view this page!</>}
      {admin && view === "main" &&
        questionnaires.map((req, index) => {
          return (
            <div key={req.userID} className='sections'>
              <div className='textbuffer'>
                User: {req.user_full_name}
              </div>
              <button className="betterbutton" style={{ margin: "20px", border: "2px solid black" }} onClick={() => handleDetailButton(index)}>
                View details
              </button>
            </div>
          )
        })
      }
      {admin && view === "detail" &&
        <div style={{ display: "flex" }}>
          <div>
            <div className="sections">
              <h2>Name</h2>
              <p>{userFullName}</p>
            </div>
            <div className="sections">
              <h2 className="textbuffer">Questionnaire responses:</h2>
              {userResponses.map((obj) => {
                return (
                  <div>
                    <p>Question: {obj.question}</p>
                    <p>Response: {obj.response}</p>
                  </div>
                )
              })}
            </div>
          </div>
          <div>
            <Button onClick={() => handleAccept(userID)} style={{ backgroundColor: "green", margin: "5px", border: "2px solid black" }}>Accept</Button>
            <Button onClick={() => handleReject(userID)} style={{ backgroundColor: "red", margin: "5px", border: "2px solid black" }}>Reject</Button>
            <Button variant="secondary" style={{ margin: "5px", border: "2px solid black" }} onClick={toggleView}>
              Back
            </Button>
          </div>
        </div>
      }
    </>
  )
}


export default ApproveQuestionnaire;
