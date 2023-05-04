import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function Groups(props) {
    
    const [groupsList, setGroupsList] = useState([])

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
                // if (!data.success) {
                //     alert(data.message)
                // }
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
                 // if (!data.success) {
                 //     alert(data.message)
                 // }
                //  if (data.success === true) {
                //      props.setGroupOption(0)
                //  }
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
                                            :
                                                <Button type='button' variant="outline-dark" size='sm'>
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
        :
            <div>
                <h1>
                    Welcome to groups page!
                </h1>
                <Button type="button" onClick={() => props.setGroupOption(1)} variant="dark">Create Group</Button>
                <br></br>
                <br></br>
                <Button type="button" onClick={() => props.setGroupOption(2)} variant="dark">List Groups</Button>
            </div>
    )
}

export default Groups;