import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

function NavBar(props) {
    const changeToLogout = () => {
        props.navOption(1)
        props.loginStatus(false)
        localStorage.clear()
    };

    const changeNavOption = (opt) => {
        if (opt === 2) {
          if (props.spotifyLoginStatus === true) {
            props.navOption(opt)
            props.setGroupOption(0)
          }
          else {
            alert("Please link to spotify!")
          }
        }
        else {
          props.navOption(opt)
        }
        
    };

    return (
        <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand onClick={() => changeNavOption(1)}>SpotiFyre</Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link onClick={() => changeNavOption(1)}>Home</Nav.Link>
            <Nav.Link onClick={() => changeNavOption(2)}>Groups</Nav.Link>
            <Nav.Link href="#pricing">Pricing</Nav.Link>
          </Nav>
          <Nav>
            <Nav.Link onClick={changeToLogout}>Logout</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    )
}

export default NavBar;