import {useState, useEffect} from 'react';

import Modal from 'react-bootstrap/Modal';
import Alert from 'react-bootstrap/Alert';
import Table from 'react-bootstrap/Table';
import Spinner from 'react-bootstrap/Spinner';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';

export default function EditCameras(props){

  const [foundCameras, setFoundCameras] = useState([]);
  const [isSearching, setSearching] = useState(false);

  const searchCameras = (event) => {
    setFoundCameras([]);
    setSearching(true);
    fetch('/api/devices/cameras')
      .then(resp => resp.json()
      .then(data => {
        // Cycle through currently added cameras
        props.cameras.map(cam=> {
          // Cycle through the found cameras
          data.map((dcam, idx) => {
            // If a camera is already added, remove it
            if (dcam.index === cam.index && dcam.interface === cam.interface) {
              data.splice(idx, 1);
            }
          })
        })
        setFoundCameras(data);
        setSearching(false);
      }))
  }

  const addCamera = (event, idx) => {
    event.target.textContent = 'Adding...';
    event.target.disabled = true;
    // Send Message to API
    fetch('/api/system/settings/cameras', {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({...foundCameras[idx]})})
      .then(resp => {
        if (resp.ok) { return resp.json()}
        else { console.error(resp.message) }
      })
      .then(data => {
        let prevCameras = [...foundCameras]
        prevCameras.splice(idx, 1)
        setFoundCameras(prevCameras);
        props.setCameras([...props.cameras, data]);
        event.target.textContent = 'Add';
        event.target.disabled = false;
      })

  }

  const removeCamera = (event, idx) => {
    //Send Message to API
    fetch('/api/system/settings/'+idx, {
      method: "DELETE",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({config:null})})
    .then(resp => {
      if (resp.ok) {
        let prevCameras = [...props.cameras];
        setFoundCameras([...foundCameras, prevCameras[idx]]);
        prevCameras.splice(idx, 1);
        props.setCameras(prevCameras);
      }
    })
    .catch(err=> console.log(err))
  }

  useEffect(()=> {
    searchCameras(null)
  },[])

  const cameraTable = (cameras, text) => {
    return (
      <Table className="text-center">
        <tbody>
          <tr><th></th><th>Interface</th><th>Index</th><th></th></tr>
          {
          cameras.map((cam, idx)=>{
            const [func, id] = (text === 'Add') ? [addCamera,idx] : [removeCamera,idx]
            if (text === 'Add') {
              const add = Object.values(props.cameras).map((c)=>{
                if (c.interface === cam.interface && c.index === cam.index) {
                    return false
                } else {
                  return true
                }
              });
              if (!add.every(v=>v===true)) {return null}
            }
            return(
              <tr key={idx}>
                <td>
                  <Button onClick={(e)=>func(e, id)}>{text}</Button>
                </td>
                <td>{cam.interface}</td>
                <td>{cam.index}</td>
                <td>
                  <Button variant="secondary">Show Info</Button>
                </td>
              </tr>
            )
          })
        }
        </tbody>
      </Table>
    )
  }

  return(
    <div>{
      <Modal show={props.show} onHide={props.hideEditing}>
        <Modal.Header closeButton>
          <Modal.Title>
            Choosing Cameras
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Container>
            <Row className="mb-3">
              <Col>
                <Modal.Title>
                  Available Cameras
                </Modal.Title>
              </Col>
              <Col><Button onClick={searchCameras}>Search</Button></Col>
            </Row>
            <Row className="justify-content-center">
              {
                isSearching ?
                <Alert variant='info'>
                  <Spinner animation="border" size='sm'/>  Searching for Cameras...
                </Alert> : null
              }
              {
                foundCameras.length > 0 ? cameraTable(foundCameras, 'Add') : null
              }
            </Row>
            <Row className="mb-3">
              <Col>
                <Modal.Title>
                  Current Cameras
                </Modal.Title>
              </Col>
            </Row>
            <Row className="justify-content-center">
              {
                Object.values(props.cameras).length > 0 ?
                cameraTable(Object.values(props.cameras), 'Remove') :
                <Alert variant='warning'>No Cameras Added</Alert>
              }
            </Row>
          </Container>
        </Modal.Body>
      </Modal>
    }</div>
  )
}
