import React, { useState } from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function SignUp(props) {
    const [errorMessages, setErrorMessages] = useState({});

    const addUser = async (name, email, password) => {
        await fetch('/signup', {
           method: 'POST',
           mode: 'cors',
           body: "name="+name+"&email="+email+"&password="+password,
           headers: {
              'Content-type': "application/x-www-form-urlencoded",
           },
        })
           .then((response) => response.json())
           .then((data) => {
                console.log(data)
                if (!data.success) {
                    console.log(data.message)
                }
                if (data.success === true) {
                    props.registrationStatus(true)
                }
           })
           .catch((err) => {
              console.log(err.message);
           });
    };
    
    const handleSubmit = (e) => {
        e.preventDefault();
        var {name, uname, pass} = document.forms[0]
        console.log(name.value, uname.value, pass.value)
        addUser(name.value, uname.value, pass.value);
    };    

    const handleLogin = () => props.registrationStatus(true);

  return (
    <div>
        <h1>Sign up!</h1>
        <Form onSubmit={handleSubmit} style={{ width: 500, height: 500, marginLeft: "auto", marginRight: "auto", marginTop: 100}}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Name</Form.Label>
                <Form.Control type="text" placeholder="Name" name="name"/>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" placeholder="Username" name="uname"/>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" name="pass"/>
            </Form.Group>
            <Button variant="primary" type="submit" >
                Submit
            </Button>
        </Form>
        <h3>If you already have an account, </h3><Button variant="primary" type="button" onClick={handleLogin}>Login</Button>
    </div>
    
  );
}

export default SignUp;