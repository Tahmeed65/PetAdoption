import { useState, useEffect } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Form } from 'react-bootstrap';
import axios from 'axios'
import Cookies from 'js-cookie'



function Questionnaire() {
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState<string[]>([]);
    const [submitted, setSubmitted] = useState(false);

    useEffect(() => {
        axios.get("http://localhost:5002/api/questionnaire").then((response) => {
            setQuestions(response.data);

            const newAnswers = [];
            for (let i = 0; i < response.data.length; i++) {
                newAnswers.push("");
            }

            setAnswers(newAnswers);
            // alert("got questions");
        })
    }, [])

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const user_id = Cookies.get("user_id");
        if (!user_id) {
            alert("you are not logged in");
            return;
        }

        for (let i = 0; i < questions.length; i++) {
            if (answers[i] === "") {
                alert("you left an answer blank");
                return;
            }
        }

        for (let i = 0; i < questions.length; i++) {
            axios.post(
                "http://localhost:5002/api/send-answer",
                {
                    user_id: Cookies.get("user_id"),
                    question: questions[i],
                    response: answers[i]
                }
            ).then(response => {
                if (response.status !== 200) {
                    alert("something went wrong");
                }
            });
        }
        setSubmitted(true);
    }

    return (
        <div className="questionaire">
            {!submitted &&
                <Form onSubmit={handleSubmit} className="buttons">

                    {questions.map((question, index) => (
                        <>
                            <div>{question}</div>
                            <Form.Group controlId="formQuestion" className="mb-3">
                                {/* <Form.Label></Form.Label> */}
                                <Form.Control
                                    type="text"
                                    // placeholder={question}
                                    value={answers[index]}
                                    onChange={(e) => setAnswers((oldAnswers) => {
                                        const newAnswers = [...oldAnswers];
                                        newAnswers[index] = e.target.value;
                                        return newAnswers;
                                    })}
                                    required
                                />
                            </Form.Group>
                        </>
                    ))}

                    <button className="betterbutton" type="submit">
                        Submit
                    </button>
                </Form>
            }
            {submitted && <p>Thanks for submitting your questionnaire</p>}
        </div>
    )
}


export default Questionnaire;
