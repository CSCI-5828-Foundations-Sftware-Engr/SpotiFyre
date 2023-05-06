import './App.css';
import React, { useState, useEffect } from "react";
import LoginForm from './LoginForm';
import NavBar from './NavBar';
import SignUp from './SignUp';
import Home from './Home';
import Groups from './Groups';

function App() {


  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isSignedUp, setIsSignedUp] = useState(false);
  const [navToggle, setNavToggle] = useState(1);
  const [groupToggle, setGroupToggle] = useState(0)
  const [spotifyLoginStatus, setSpotifyLoginStatus] = useState(false)

  useEffect(() => {
    fetch('http://35.222.7.52/test', {
      method: "GET",
      mode: "cors"
    })
      .then((response) => response.json())
      .then((message) => console.log(message.message))
      .catch((e) => console.log(e));
  }, []);

  useEffect(() => {
    const loggedInUser = localStorage.getItem("user_id");
    if (loggedInUser) {
      setIsSubmitted(true);
    }
  }, []);
  
  return (
    <div>
      {
        isSubmitted?
          <div>
            <NavBar 
              loginStatus={setIsSubmitted}
              navOption={setNavToggle}  
              setGroupOption={setGroupToggle}
              spotifyLoginStatus={spotifyLoginStatus}
            />
          
            {
              navToggle===2?
                <div>
                  <Groups
                    setGroupOption={setGroupToggle}
                    groupOption={groupToggle}
                  />
                </div>
              : navToggle === 1?
                <div>
                  <Home 
                    spotifyLoginStatus={spotifyLoginStatus}
                    setSpotifyLoginStatus={setSpotifyLoginStatus}
                  />
                </div>
              :
                <div>
                </div>
            }
          </div>
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
