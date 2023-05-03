import './App.css';
import React, { useState, useEffect } from "react";
import LoginForm from './LoginForm';
import NavBar from './NavBar';
import SignUp from './SignUp';

function App() {


  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isSignedUp, setIsSignedUp] = useState(false);
  // useEffect(() => {
  //   fetch('/test', {
  //     method: "GET",
  //     mode: "no-cors"
  //   })
  //     .then((response) => response.json())
  //     .then((message) => console.log(message.message))
  //     .catch((e) => console.log(e));
  // }, []);

  useEffect(() => {
    const loggedInUser = localStorage.getItem("user");
    if (loggedInUser) {
      setIsSubmitted(true);
    }
  }, []);
  
  return (
    <div>
      {
        isSubmitted?
          <NavBar loginStatus={setIsSubmitted}/>
        :
          isSignedUp?
            <LoginForm 
              loginStatus={setIsSubmitted} 
              registrationStatus={setIsSignedUp}
            />
          :
            <SignUp registrationStatus={setIsSignedUp}/>
      }
    </div>
      
  );
}

export default App;
