import React, { useState } from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function LoginForm(props) {
    const [errorMessages, setErrorMessages] = useState({});

    const validateUser = async (email, password) => {
        await fetch('/login', {
           method: 'POST',
           mode: 'no-cors',
           body: "email="+email+"&password="+password,
           headers: {
              'Content-type': "application/x-www-form-urlencoded",
           },
        })
           .then((response) => response.json())
           .then((data) => {
                console.log(data)
                if (!data.success) {
                    alert(data.message)
                }
                if (data.success === true) {
                    props.loginStatus(true)
                    localStorage.setItem('user_id', data.data.user_id)
                }
           })
           .catch((err) => {
              console.log(err.message);
           });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        var {uname, pass} = document.forms[0]
        console.log(uname.value, pass.value)
        validateUser(uname.value, pass.value);
    };   

    const handleLogin = () => props.registrationStatus(false);

  return (
    <div>
        <h1>Log in!</h1>
        <Form onSubmit={handleSubmit} style={{ width: 500, height: 500, marginLeft: "auto", marginRight: "auto", marginTop: 100}}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" placeholder="Username" name="uname"/>
                {/* {renderErrorMessage("uname")} */}
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" name="pass"/>
                {/* {renderErrorMessage("pass")} */}
            </Form.Group>
            <Button variant="primary" type="submit" >
                Submit
            </Button>
        </Form>
        If you don't have an account, <Button variant="primary" type="button" onClick={handleLogin}>Sign up!</Button>
    </div>
  );
}

export default LoginForm;