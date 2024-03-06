import React, { useState } from 'react';
import axios from 'axios';
import useAuthHeader from 'react-auth-kit/hooks/useAuthHeader';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Image from 'react-bootstrap/Image';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';


const ImageUploader = ({getImage}) => {
    const authHeader = useAuthHeader();
    axios.defaults.headers.common['Authorization'] = authHeader
    const[file, setFile] = useState()


    
    const handleImageChange = (e) => {
    const file = e.target.files[0];
    setFile(file)
  };

    const handleUpload = (e) => {
      let formdata = {};
      formdata['file'] = file
      e.preventDefault();
      axios.post(process.env.REACT_APP_BACKEND_URL+'api/avatar/upload/',formdata, {headers:{'Content-Type': 'multipart/form-data'}}).then(()=>{
        getImage();
      }).catch((err)=>{
        console.log(err);
        let message = '';
        let error_obj =  err.response.data
        Object.keys(error_obj).forEach(element => {
          message+= error_obj[element]
        }); 
        alert(message)
      })
  };

    return (
    <div className='FormContainer'>
        <Form onSubmit={handleUpload}>
        <Form.Group controlId="formFile" className="mb-3" style={{width: '25vw'}}>
            <Form.Label  >Choose Image</Form.Label>
            <Row>
                <Col>
                    <Form.Control className='col-sm-2' type="file" accept='.jpg,.png' onChange={handleImageChange} />
                </Col>
                
                <Col>
                    <Button type='submit'>Upload</Button>
                </Col>
            </Row>  
        </Form.Group>
        
       
        </Form>
    </div>
  );
};

export default ImageUploader;