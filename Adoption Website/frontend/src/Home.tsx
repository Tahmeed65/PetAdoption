import { useState, useEffect } from 'react'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios'
import Cookies from 'js-cookie'



function Home() {
    const session_id = Cookies.get("session_id");
    const user_id = Cookies.get("user_id");
    const [name, setName] = useState('');
    const [qStatus, setQStatus] = useState('');
    const [adoptStatus, setAdoptStatus] = useState('');
    const [isAdmin, setAdmin] = useState('');
    const [qsPending, setQsPending] = useState('');
    const [qLoading, setQLoading] = useState(true);
    const [adoptLoading, setAdoptLoading] = useState(true);
    const [adoptPending, setAdoptPending] = useState('');

    useEffect(() => {
        const target_url = `http://localhost:5002/api/questionnaire-status/${user_id}`;
        axios.get(target_url)
            .then(response => {
                console.log(response);
                setQStatus(response.data);
                setQLoading(false);
            })
            .catch(error => {
                console.error("Error fetching questionnaire status:", error);
            });
    }, [user_id]);

    useEffect(() => {
        const target_url = `http://localhost:5002/api/adoption-status/${user_id}`;
        axios.get(target_url)
            .then(response => {
                console.log(response);
                setAdoptStatus(response.data);
                setAdoptLoading(false);
            })
            .catch(error => {
                console.error("Error fetching adopotion request status:", error);
            });
    }, [user_id]);

    useEffect(() => {
        const target_url = `http://localhost:5002/api/is-admin/${user_id}`;
        axios.get(target_url)
            .then(response => {
                console.log(response);
                setAdmin(response.data);
            })
            .catch(error => {
                console.error("Error checking if user is admin:", error);
            });
    }, [user_id]);

    useEffect(() => {
        const target_url = 'http://localhost:5002/api/admin/pending-questionnaires';
        axios.get(target_url)
            .then(response => {
                console.log(response);
                setQsPending(response.data);
            })
            .catch(error => {
                console.error("Failed to check if there are pending questionnaires:", error);
            });
    }, []);

    useEffect(() => {
        const target_url = 'http://localhost:5002/api/admin/pending-adopts';
        axios.get(target_url)
            .then(response => {
                console.log(response);
                setAdoptPending(response.data);
            })
            .catch(error => {
                console.error("Failed to check if there are pending adoption requests:", error);
            });
    }, []);

    useEffect(() => {
        if (session_id) {
            setName(Cookies.get("name"));
        }
    }, [session_id]);

    const extra_large_font = {
        fontSize: "100px"
    };

    const getQuestionnaires = () => {
        if (name && isAdmin.is_admin === 0 && qLoading === false) {
            return (
                <div className="textbuffer">
                    <h2>Your questionnaire statuses</h2>
                    <table>
                        <thead>
                            <tr>
                                <th><h4>Questionnaire ID</h4></th>
                                <th><h4>Submit Time</h4></th>
                                <th><h4>Status</h4></th>
                            </tr>
                        </thead>
                        <tbody>
                            {qStatus.map(component => (
                                <tr key={component.questionnaire_id}>
                                    <td>{component.questionnaire_id}</td>
                                    <td>{component.time}</td>
                                    <td>{component.status}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )
        } else {
            return null
        }
    }

    const getAdoptreqs = () => {
        if (name && isAdmin.is_admin === 0 && adoptLoading === false) {
            return (
                <div className="textbuffer">
                    <h2>Your adoption requests</h2 >
                    <table>
                        <thead>
                            <tr>
                                <th><h4>Request ID</h4></th>
                                <th><h4>Pet ID</h4></th>
                                <th><h4>Submit Time</h4></th>
                                <th><h4>Status</h4></th>
                            </tr>
                        </thead>
                        <tbody>
                            {adoptStatus.map(component => (
                                <tr key={component.request_id}>
                                    <td>{component.request_id}</td>
                                    <td>{component.pet_id}</td>
                                    <td>{component.time}</td>
                                    <td>{component.status}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )
        } else {
            return null
        }
    }

    const awaitingQuests = () => {
        if (name && isAdmin.is_admin === 1 && qsPending.pending === 'true') {
            return <h2>You have awaiting questionnaires!</h2>
        } else if (name && isAdmin.is_admin === 1 && qsPending.pending === 'false') {
            return <h2>You have no pending questionnaires.</h2>
        } else {
            return null
        }
    }

    const awaitingAdopts = () => {
        if (name && isAdmin.is_admin === 1 && adoptPending.pending === 'true') {
            return <h2>You have awaiting adoption requests!</h2>
        } else if (name && isAdmin.is_admin === 1 && adoptPending.pending === 'false') {
            return <h2>You have no new adoption requests.</h2>
        } else {
            return null
        }
    }

    return (
        <div className="homepage">
            <h1 style={extra_large_font}>PetFinder Home</h1>
            {name && <h1>Welcome {name}!</h1>}
            {!name && <h1>Please log in</h1>}
            {name &&
            (
            <div>
            <br></br>
            <div className="sections">
            {getQuestionnaires()}
            {awaitingQuests()}
            </div>
            <br></br>
            <div className="sections">
            {getAdoptreqs()}
            {awaitingAdopts()}
            </div>
            </div>
            )
            }
        </div>
    );
}

export default Home;
