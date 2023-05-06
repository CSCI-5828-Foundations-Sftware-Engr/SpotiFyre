import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function Groups(props) {
    
    const [groupsList, setGroupsList] = useState(false)
    const [invitationsList, setInvitationsList] = useState([])
    const [requestsList, setRequestsList] = useState([])
    const [generatePlaylistForm, setGeneratePlaylistForm] = useState(false)
    const [playlistId, setPlaylistId] = useState()
    const [playlistLink, setPlaylistLink] = useState()

    const createGroup = async (group_name, group_description, user_id) => {
        await fetch('http://35.222.7.52/create_group', {
           method: 'POST',
           mode: 'cors',
           body: "group_name="+group_name+"&group_description="+group_description+"&user_id="+user_id,
           headers: {
              'Content-type': "application/x-www-form-urlencoded",
              'Accept': 'application/json'
           },
        })
           .then((response) => response.json())
           .then((data) => {
                console.log(data.message)
                alert(data.message)

                if (data.success === true) {
                    props.setGroupOption(0)
                }
           })
           .catch((err) => {
              console.log(err.message);
           });
    };

    const showGroups = async (user_id) => {
        await fetch('http://35.222.7.52/list_groups', {
            method: 'POST',
            mode: 'cors',
            body: "user_id="+user_id,
            headers: {
                'Content-type': "application/x-www-form-urlencoded",
             },
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data.message)
            console.log(data.data)
            if (data.success === true) {
                setGroupsList(data.data)
            }
        })
        .catch((err) => {
            console.log(err.message);
        })
    };

    const showInvitations = async (user_id) => {
        await fetch('http://35.222.7.52/get_all_invitations', {
            method: 'POST',
            mode: 'cors',
            body: "user_id="+user_id,
            headers: {
                'Content-type': "application/x-www-form-urlencoded",
             },
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data.message)
            console.log(data.data)
            if (data.success === true) {
                setInvitationsList(data.data)
            }
        })
        .catch((err) => {
            console.log(err.message);
        })
    };

    const showRequests = async (user_id) => {
        await fetch('http://35.222.7.52/get_all_membership_requests', {
            method: 'POST',
            mode: 'cors',
            body: "user_id="+user_id,
            headers: {
                'Content-type': "application/x-www-form-urlencoded",
             },
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data.message)
            console.log(data.data)
            if (data.success === true) {
                setRequestsList(data.data)
            }
        })
        .catch((err) => {
            console.log(err.message);
        })
    };

    const requestGroupJoin = async (group_id, user_id) => {
        await fetch('http://35.222.7.52/request_membership', {
            method: 'POST',
            mode: 'cors',
            body: "group_id="+group_id+"&user_id="+user_id,
            headers: {
               'Content-type': "application/x-www-form-urlencoded",
            },
         })
            .then((response) => response.json())
            .then((data) => {
                 console.log(data.message)
                 alert(data.message)
            })
            .catch((err) => {
               console.log(err.message);
            });
    };

    const inviteUser = async (group_id, email, user_id) => {
        await fetch('http://35.222.7.52/invite_members', {
            method: 'POST',
            mode: 'cors',
            body: "group_id="+group_id+"&email="+email+"&user_id="+user_id,
            headers: {
               'Content-type': "application/x-www-form-urlencoded",
            },
         })
            .then((response) => response.json())
            .then((data) => {
                 console.log(data.message)
                 alert(data.message)
            })
            .catch((err) => {
               console.log(err.message);
            });
    };

    const sendInviteDecision = async (group_id, action, user_id, invitation_id) => {
        await fetch('http://35.222.7.52/process_invitation', {
            method: 'POST',
            mode: 'cors',
            body: "group_id="+group_id+"&action="+action+"&user_id="+user_id+"&invitation_id="+invitation_id,
            headers: {
               'Content-type': "application/x-www-form-urlencoded",
            },
         })
            .then((response) => response.json())
            .then((data) => {
                 console.log(data.message)
                 alert(data.message)

            })
            .catch((err) => {
               console.log(err.message);
            });
    };

    const sendRequestDecision = async (group_id, user_id, action, request_id) => {
        await fetch('http://35.222.7.52/process_membership_request', {
            method: 'POST',
            mode: 'cors',
            body: "group_id="+group_id+"&action="+action+"&user_id="+user_id+"&membership_request_id="+request_id,
            headers: {
               'Content-type': "application/x-www-form-urlencoded",
            },
         })
            .then((response) => response.json())
            .then((data) => {
                 console.log(data.message)
                 alert(data.message)

            })
            .catch((err) => {
               console.log(err.message);
            });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        
        var {grpname, grpdesc} = document.forms[0]
        var userid = localStorage.getItem('user_id')
        console.log(grpname.value, grpdesc.value, userid)
        createGroup(grpname.value, grpdesc.value, userid);
    };
    
    const handleInviteClick = (group_id) => {
        // e.preventDefault();
        // var email;
        var email = prompt("Invite e-mail address:", "");

        var userid = localStorage.getItem("user_id");
        console.log(group_id);
        console.log(email);
        if (email == null || email == "") {
            alert("Invite cancelled");
          } else {
            inviteUser(group_id, email, userid);
          }

    }

    const generatePlaylist = async (group_id, playlist_name, num_tracks, user_id) => {
        await fetch('http://35.222.7.52/generate_playlist', {
            method: 'POST',
            mode: 'cors',
            body: "group-id="+group_id+"&playlist-name="+playlist_name+"&num-tracks="+num_tracks+"&user_id="+user_id,
            headers: {
               'Content-type': "application/x-www-form-urlencoded",
            },
         })
            .then((response) => response.json())
            .then((data) => {
                 console.log(data.message)
                 console.log(data.data)
                 if (data.success === true) {
                    setPlaylistId(data.data)
                 }
                 
            })
            .catch((err) => {
               console.log(err.message);
            });
    };
    
    const getPlaylistLink = async (playlist_id, user_id) => {
        await fetch('http://35.222.7.52/get_playlist_link', {
            method: 'POST',
            mode: 'cors',
            body: "playlist_id="+2+"&user_id="+user_id,
            headers: {
               'Content-type': "application/x-www-form-urlencoded",
            },
         })
            .then((response) => response.json())
            .then((data) => {
                console.log(data.message)
                setPlaylistLink(data.data)
                alert(data.data) 
            })
            .catch((err) => {
               console.log(err.message);
            });
    };

    const handleGeneratePlaylistForm = (group) => {
        setGroupsList(false);
        setGeneratePlaylistForm(group);
    }

    const handlePlaylistFormSubmit = (group_id) => {
        // e.preventDefault();
        // group_id.preventDefault()
        var {plstname, numtracks, group_id} = document.forms[0];
        var userid = localStorage.getItem("user_id")
        console.log(group_id, plstname.value, Number(numtracks.value), userid);
        generatePlaylist(group_id, plstname.value, Number(numtracks.value), userid);
    }

    const handleGetLink = () => {
        console.log("get link call")
        var userid = localStorage.getItem("user_id")
        console.log("playlis_id: ", playlistId)
        getPlaylistLink(playlistId, userid);
    }

    return (
        props.groupOption===1?
            <div>
               <Form onSubmit={handleSubmit} style={{ width: 500, height: 500, marginLeft: "auto", marginRight: "auto", marginTop: 100}}>
                    <Form.Group className="mb-3" controlId="formGroupName">
                        <Form.Label>Group Name</Form.Label>
                        <Form.Control type="text" placeholder="Roadtrip" name="grpname"/>
                        {/* {renderErrorMessage("uname")} */}
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formGroupDescription">
                        <Form.Label>Description</Form.Label>
                        <Form.Control type="text" placeholder="Trip to Utah!" name="grpdesc"/>
                        {/* {renderErrorMessage("pass")} */}
                    </Form.Group>

                    <Button variant="primary" type="submit" >
                        Submit
                    </Button>
                </Form>
            </div>
        : props.groupOption===2?
            <div>
                <h1>List groups</h1>
                <Button type="button" onClick={() => showGroups(localStorage.getItem('user_id'))} variant="dark">Show Groups</Button>
                {
                    groupsList?
                        <div>
                            <ol>
                                {groupsList.map((group) => (
                                    <>
                                    <li key={group.id}>{group.name}</li>
                                    
                                        {
                                            group.owner.id === Number(localStorage.getItem("user_id"))?
                                            <div>
                                                <Button type='button' variant="outline-dark" size='sm' onClick={() => handleInviteClick(group.id)}>
                                                    Invite
                                                </Button>
                                                <Button type='button' variant="outline-dark" size='sm' onClick={() => handleGeneratePlaylistForm(group)}>
                                                    Generate Playlist
                                                </Button>
                                                <Button type='button' variant="outline-dark" size='sm' onClick={() => handleGetLink()}>
                                                    Get playlist link
                                                </Button>
                                            </div>
                                                
                                            : group.isMember?
                                                <>Already a member</>
                                            :
                                                <Button type='button' variant="outline-dark" size='sm' onClick={() => requestGroupJoin(group.id, localStorage.getItem("user_id"))}>
                                                    Request
                                                </Button>
                                        }
                                    
                                    </>
                                ))}
                            </ol>
                            
                        </div>
                    :generatePlaylistForm?
                        <div>
                            <h1>Generate a playlist here for your group {generatePlaylistForm.name}</h1>
                            {/* <Button type='button' variant="outline-dark" size='sm' onClick={() => handlePlaylistFormSubmit(generatePlaylistForm.id)}>
                                Click here to generate playlist.
                            </Button> */}
                            <Form onSubmit={() => handlePlaylistFormSubmit(generatePlaylistForm.id)} style={{ width: 500, height: 500, marginLeft: "auto", marginRight: "auto", marginTop: 100}}>
                                <Form.Group className="mb-3" controlId="formPlaylistName">
                                    <Form.Label>Playlist Name</Form.Label>
                                    <Form.Control type="text" placeholder="Rock the party!" name="plstname"/>
                                    
                                </Form.Group>

                                <Form.Group className="mb-3" controlId="formTrackNum">
                                    <Form.Label>Number of tracks</Form.Label>
                                    <Form.Control type="number" placeholder="12" name="numtracks"/>
                                    {/* <div name="group_id" value={generatePlaylistForm.id}></div> */}
                                </Form.Group>
                                <Button variant="primary" type="submit" >
                                    Submit
                                </Button>
                            </Form>
                        </div>
                    :
                        <div>
                            <p>No groups found.</p>
                        </div>

                }

            </div>
        : props.groupOption===3?
            <div>
                <h1>Check your group invitations here!</h1>
                <Button type="button" onClick={() => showInvitations(localStorage.getItem("user_id"))} variant="dark">Show Invitations</Button>
                {
                    invitationsList?
                        <div>
                            <ol>
                                {invitationsList.map((invitation) => (
                                    <>
                                    <li key={invitation.id}>From user {invitation.user_name}, for group {invitation.group_name}</li>
                                    
                                    <Button type='button' onClick={() => sendInviteDecision(invitation.group_id, 'accept', localStorage.getItem("user_id"), invitation.id)} variant="outline-dark" size='sm'>
                                        Accept
                                    </Button>
                                    <Button type='button' onClick={() => sendInviteDecision(invitation.group_id, 'reject', localStorage.getItem("user_id"), invitation.id)} variant="outline-dark" size='sm'>
                                        Reject
                                    </Button>
                                    
                                    </>
                                ))}
                            </ol>
                            
                        </div>
                    :
                        <div>
                            <p>No invitations found.</p>
                        </div>

                }
            </div>
        : props.groupOption===4?
                <div>
                    <h1>Manage your group requests here!</h1>
                    <Button type="button" onClick={() => showRequests(localStorage.getItem("user_id"))} variant="dark">Show Requests</Button>
                    {
                        requestsList?
                            <div>
                                <ol>
                                    {requestsList.map((request) => (
                                        <>
                                        <li key={request.id}>From user {request.user_name}, for group {request.group_name}</li>
                                        
                                        <Button type='button' onClick={() => sendRequestDecision(request.group_id, request.user_id, 'accept', request.id)} variant="outline-dark" size='sm'>
                                            Accept
                                        </Button>
                                        <Button type='button' onClick={() => sendRequestDecision(request.group_id, request.user_id, 'reject', request.id)} variant="outline-dark" size='sm'>
                                            Reject
                                        </Button>
                                        
                                        </>
                                    ))}
                                </ol>
                                
                            </div>
                        :
                            <div>
                                <p>No requests found.</p>
                            </div>

                    }
                </div>
        :
            <div>
                <h1>
                    Welcome to groups page!
                </h1>
                <Button type="button" onClick={() => props.setGroupOption(1)} variant="dark">Create Group</Button>
                <br></br>
                <br></br>
                <Button type="button" onClick={() => props.setGroupOption(2)} variant="dark">List Groups</Button>
                <br></br>
                <br></br>
                <Button type="button" onClick={() => props.setGroupOption(3)} variant="dark">Group Invitations</Button>
                <br></br>
                <br></br>
                <Button type="button" onClick={() => props.setGroupOption(4)} variant="dark">Group Requests</Button>
            </div>
    )
}

export default Groups;