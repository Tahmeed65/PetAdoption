import { useState, useEffect } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import Cookies from 'js-cookie'

function Pets() {
    const [pets, setPets] = useState([]);

    // Fetch pets from API
    useEffect(() => {
        axios.get("http://localhost:5002/api/pets")
            .then(response => {
                console.log(response);
                setPets(response.data);
            })
            .catch(error => {
                console.error("Error fetching pets:", error);
            });
    }, []);

    // Handler for button click
    const handleButtonClick = (petId) => {
        const user_id = Cookies.get("user_id")
        if (!user_id) {
            alert("you're not logged in!")
            return
        }
        axios.post(`http://localhost:5002/api/request-adoption/${user_id}/${petId}`)
            .then(response => {
                console.log("Action successful:", response.data);
                alert(`Action for pet ${petId} was successful!`);
            })
            .catch(error => {
                console.error("Error performing action:", error);
                alert(`Action for pet ${petId} failed.`);
            });
    };

    return (
        <div className="pets-container">
            {pets.map((pet) => (
                <div key={pet.petID} className="pet-card">
                    <p>Pet name: {pet.name}</p>
                    <p>Pet species: {pet.species}</p>
                    <img src={pet.image} alt={`Image of ${pet.name}`} />
                    <button
                        className="betterbutton"
                        onClick={() => handleButtonClick(pet.petID)}
                    >
                        Adopt!
                    </button>
                </div>
            ))}
        </div>
    );
}

export default Pets;
