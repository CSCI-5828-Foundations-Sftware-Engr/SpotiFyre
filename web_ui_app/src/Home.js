import { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';

function Home(props) {
    // const [spotifyLoginStatus, setSpotifyLoginStatus] = useState(false)

    useEffect(() => {
        fetch('/check_spotify_login', {
          method: "POST",
          mode: "no-cors"
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(data.message)
            console.log(data.data)
            props.setSpotifyLoginStatus(data.data)
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
                <><Button type="button" href='//127.0.0.1/spotify-login' target="_blank" variant="success">Link Spotify</Button>{' '}</>
            }
            
        </div>
    )
}

export default Home;