import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function Groups(props) {
    
    const [groupsList, setGroupsList] = useState([])
    const [invitationsList, setInvitationsList] = useState([])
    const [requestsList, setRequestsList] = useState([])

    const createGroup = async (group_name, group_description) => {
        await fetch('/create_group', {
           method: 'POST',
           mode: 'no-cors',
           body: "group_name="+group_name+"&group_description="+group_description,
           headers: {
              'Content-type': "application/x-www-form-urlencoded",
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

    const showGroups = async () => {
        await fetch('/list_groups', {
            method: 'POST',
            mode: 'no-cors'
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

    const showInvitations = async () => {
        await fetch('/get_all_invitations', {
            method: 'POST',
            mode: 'no-cors'
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

    const showRequests = async () => {
        await fetch('/get_all_membership_requests', {
            method: 'POST',
            mode: 'no-cors'
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

    const requestGroupJoin = async (group_id) => {
        await fetch('/request_membership', {
            method: 'POST',
            mode: 'no-cors',
            body: "group_id="+group_id,
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

    const inviteUser = async (group_id, email) => {
        await fetch('/invite_members', {
            method: 'POST',
            mode: 'no-cors',
            body: "group_id="+group_id+"&email="+email,
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

    const sendInviteDecision = async (group_id, action) => {
        await fetch('/process_invitation', {
            method: 'POST',
            mode: 'no-cors',
            body: "group_id="+group_id+"&action="+action,
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

    const sendRequestDecision = async (group_id, user_id, action) => {
        await fetch('/process_membership_request', {
            method: 'POST',
            mode: 'no-cors',
            body: "group_id="+group_id+"&action="+action+"&user_id="+user_id,
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
        console.log(grpname.value, grpdesc.value)
        createGroup(grpname.value, grpdesc.value);
    };
    
    const handleInviteClick = (group_id) => {
        // e.preventDefault();
        // var email;
        var email = prompt("Invite e-mail address:", "");
        console.log(group_id);
        console.log(email);
        if (email == null || email == "") {
            alert("Invite cancelled");
          } else {
            inviteUser(group_id, email);
          }

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
                <Button type="button" onClick={() => showGroups()} variant="dark">Show Groups</Button>
                {
                    groupsList?
                        <div>
                            <ol>
                                {groupsList.map((group) => (
                                    <>
                                    <li key={group.id}>{group.name}</li>
                                    
                                        {
                                            group.owner.id === Number(localStorage.getItem("user_id"))?
                                                <Button type='button' variant="outline-dark" size='sm' onClick={() => handleInviteClick(group.id)}>
                                                    Invite
                                                </Button>
                                            : group.isMember?
                                                <>{}</>
                                            :
                                                <Button type='button' variant="outline-dark" size='sm' onClick={() => requestGroupJoin(group.id)}>
                                                    Request
                                                </Button>
                                        }
                                    
                                    </>
                                ))}
                            </ol>
                            
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
                <Button type="button" onClick={() => showInvitations()} variant="dark">Show Invitations</Button>
                {
                    invitationsList?
                        <div>
                            <ol>
                                {invitationsList.map((invitation) => (
                                    <>
                                    <li key={invitation.id}>From Group ID: {invitation.group_id}</li>
                                    
                                    <Button type='button' onClick={() => sendInviteDecision(invitation.group_id, 'accept')} variant="outline-dark" size='sm'>
                                        Accept
                                    </Button>
                                    <Button type='button' onClick={() => sendInviteDecision(invitation.group_id, 'reject')} variant="outline-dark" size='sm'>
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
                    <Button type="button" onClick={() => showRequests()} variant="dark">Show Requests</Button>
                    {
                        requestsList?
                            <div>
                                <ol>
                                    {requestsList.map((request) => (
                                        <>
                                        <li key={request.id}>From User ID: {request.user_id}</li>
                                        
                                        <Button type='button' onClick={() => sendRequestDecision(request.group_id, request.user_id, 'accept')} variant="outline-dark" size='sm'>
                                            Accept
                                        </Button>
                                        <Button type='button' onClick={() => sendRequestDecision(request.group_id, request.user_id, 'reject')} variant="outline-dark" size='sm'>
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