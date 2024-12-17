import { useState, useEffect } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button } from 'react-bootstrap';
import axios from 'axios'
import Cookies from 'js-cookie'
import { useNavigate } from 'react-router-dom';


function ApproveAdoption() {
  const [admin, setAdmin] = useState(false);

  interface AdoptionRequest {
    user_full_name: string;
    pet_name: string;
    pet_species: string;
    petID: number;
    userID: number;
  }

  const [requests, setRequests] = useState<AdoptionRequest[]>([]);
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


    axios.get(`http://localhost:5002/api/adoption-queue`)
      .then(response => {
        setRequests(response.data);
      })
      .catch(error => {
        alert("Error: " + error);
      });

  }, [adminID]);

  const toggleView = () => {
    if (view === "main") setView("detail");
    else setView("main");
  }

  const [petName, setPetName] = useState('');
  const [petImage, setPetImage] = useState('');
  const [petDescription, setPetDescription] = useState('');
  const [userFullName, setUserFullName] = useState('');

  interface UserResponse {
    question: string;
    response: string;
  }
  const [userResponses, setUserResponses] = useState<UserResponse[]>([]);

  const [petID, setPetID] = useState(0);
  const [userID, setUserID] = useState(0);

  const nav = useNavigate();

  // const [pet, setPetDescription] = useState('');

  const handleDetailButton = (index: number) => {
    setPetName(requests[index].pet_name);
    setPetID(requests[index].petID);
    setUserID(requests[index].userID);
    setUserFullName(requests[index].user_full_name);

    axios.get(`http://localhost:5002/api/pet/${requests[index].petID}`)
      .then((response) => {
        setPetImage(response.data.image);
        setPetDescription(response.data.description);
      })
      .catch(error => {
        alert("Error: " + error);
      });

    axios.get(`http://localhost:5002/api/questionnaire/${requests[index].userID}`)
      .then((response) => {
        console.log(response);
        setUserResponses(response.data);
      })


    toggleView();
  }

  const handleAccept = (userID: number, petID: number) => {
    axios.post(`http://localhost:5002/api/admin/approve-adoption/${adminID}/${userID}/${petID}`)
      .then(() => {
        alert("Success");
        toggleView();
        nav(0);
      })
      .catch(error => {
        alert("Error: " + error);
      });

  }

  const handleReject = (userID: number, petID: number) => {
    axios.post(`http://localhost:5002/api/admin/deny-adoption/${adminID}/${userID}/${petID}`)
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
        requests.map((req, index) => {
          return (
            <div>
              <hr />
              <div>
                User: {req.user_full_name}
              </div>
              <div>
                Pet: {req.pet_name} ({req.pet_species})
              </div>
              <button className="betterbutton" onClick={() => handleDetailButton(index)}>
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
              <div>
                Name: {petName}
              </div>
              <div>
                Description: {petDescription}
              </div>
            </div>
            <div className="sections">
              <img src={petImage} style={{ width: "50%", height: "auto" }} />
            </div>
          </div>
          <div className="sections">
            <div className="textbuffer">
              <h2>Adopter name</h2>
              <p>{userFullName}</p>
            </div>
          </div>
          <div className="sections">
            <div className="textbuffer">
              <h2>Questionnaire responses:</h2>
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
            <Button onClick={() => handleAccept(userID, petID)} style={{ backgroundColor: "green", margin: "5px", border: "2px solid black" }}>Accept</Button>
            <Button onClick={() => handleReject(userID, petID)} style={{ backgroundColor: "red", margin: "5px", border: "2px solid black" }}>Reject</Button>
            <Button variant="secondary" onClick={toggleView}style={{margin: "5px", border: "2px solid black" }}>
              Back
            </Button>
          </div>
        </div>
      }
    </>
  )
}


export default ApproveAdoption;
