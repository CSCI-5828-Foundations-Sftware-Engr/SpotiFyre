import { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';

function Home(props) {
    // const [spotifyLoginStatus, setSpotifyLoginStatus] = useState(false)

    useEffect(() => {
        fetch('/check_spotify_login', {
          method: "POST",
          mode: "cors",
          body: "user_id="+localStorage.getItem("user_id"),
          headers: {
            'Content-type': "application/x-www-form-urlencoded",
            'Accept': 'application/json'
         }
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(localStorage.getItem("user_id"))
            console.log(data.message)
            console.log(data.data)
            props.setSpotifyLoginStatus(data.data)
            // props.setSpotifyLoginStatus(true)
        })
          .catch((e) => console.log(e));
      }, []);

    return (
        <div>
            <h1>
                Welcome to home page!
            </h1>
            {
                props.spotifyLoginStatus?
                <>Spotify is linked!</>
                :
                <><Button type="button" href='/spotify-login' target="_blank" variant="success">Link Spotify</Button>{' '}</>
            }
            
        </div>
    )
}

export default Home;