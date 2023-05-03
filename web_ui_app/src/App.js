import './App.css';
import React, { useState } from "react";
import LoginForm from './LoginForm';
import NavBar from './NavBar';

function App() {


  const [isSubmitted, setIsSubmitted] = useState(false);

  return (
    <div>
      {
        isSubmitted?
          <NavBar loginStatus={setIsSubmitted}/>
        :
          <LoginForm loginStatus={setIsSubmitted}/>
      }
    </div>
      
  );
}

export default App;
