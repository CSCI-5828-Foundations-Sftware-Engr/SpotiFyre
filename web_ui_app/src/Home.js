import { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';

function Home(props) {
    // const [spotifyLoginStatus, setSpotifyLoginStatus] = useState(false)

    useEffect(() => {
        fetch('http://35.222.7.52/check_spotify_login', {
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

      const logineSpotify = async (email, password, userid) => {
        await fetch('http://35.222.7.52/spotify-login', {
           method: 'POST',
           mode: 'cors',
           body: "email="+email+"&password="+password+"&user_id="+userid,
           headers: {
              'Content-type': "application/x-www-form-urlencoded",
           },
        })
           .then((response) => response.json())
           .then((data) => {
                window.open(data);
                // console.log(data)
                // if (!data.success) {
                //     alert(data.message)
                // }
                // if (data.success === true) {
                //     props.loginStatus(true)
                //     localStorage.setItem('user_id', Number(data.data.user_id))
                // }
           })
           .catch((err) => {
              console.log(err.message);
           });
    };

      const handleSpotifyLoginClick = () => {
        var userid = localStorage.getItem('user_id');

      }
    return (
        <div>
            <h1>
                Welcome to home page!
            </h1>
            {
                props.spotifyLoginStatus?
                <>Spotify is linked!</>
                :
                <><Button type="button" href='http://35.222.7.52/spotify-login' target="_blank" variant="success">Link Spotify</Button>{' '}</>
            }
            
        </div>
    )
}

export default Home;