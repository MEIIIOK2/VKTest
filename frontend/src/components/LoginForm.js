import React from 'react'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useState } from 'react';
import axios from 'axios';
import useIsAuthenticated from 'react-auth-kit/hooks/useIsAuthenticated';
import Alert from '@mui/material/Alert';

import useSignIn from 'react-auth-kit/hooks/useSignIn';


function LoginForm({handleAuth}) {
    const signIn = useSignIn();
    let isAuthenticated = useIsAuthenticated();
    const [formdata, setformData] = useState({
        'loginMode':true,
        'email':'',
        'password':'',
        'password1':''
    });
    const[alert, setAlert] = useState({
        'text':'',
        'enabled':false,
        'severity':'error'
    })
    
    const onSubmit = (e) =>{
        
        e.preventDefault()
        if (formdata['loginMode']) {
            axios.post(process.env.REACT_APP_BACKEND_URL+'api/login/',formdata).then(
                (res)=>{
                    if(res.status === 200){
                        if(signIn(
                            {
                                auth: {
                                    token: res.data.token,
                                    type: 'Bearer'
                                },
                            }
                        )){ 
                            
                            handleAuth()
                           
                        }
                        else {
                            console.log(res.status)
                        }
                    }
                }
            ).catch((res)=>{
                console.log(res.status)
                setAlert({'enabled':true,'text':'Wrong email or password or account inactive'})
            })

        }
        else{
            axios.post(process.env.REACT_APP_BACKEND_URL+'api/register/',formdata).then(
                (res)=>{
                    if (res.status===200){
                        setAlert({'enabled':true,'text':'Registration successful. Please check inbox','severity':'success'})
                    }
                }
            )
        }
    }

    function switchMode(params) {
        setformData({...formdata, loginMode : !formdata['loginMode']})
    }

  

    let match = formdata['password']===formdata['password1']
  return (
    <div className='FormContainer'>
        
        <Form onSubmit={onSubmit}>
            
        <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control type="email" placeholder="Enter email" onChange={
                (e)=>setformData({...formdata,email:e.target.value})
            }/>
            <Form.Text className="text-muted">
            </Form.Text>
        </Form.Group>
        
        {
            formdata['loginMode'] ? (
                <Form.Group className="mb-3" controlId="formBasicPasswordLogin">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password" onChange={
                        (e)=>setformData({...formdata,password:e.target.value})
                    }/>
                </Form.Group>
            ): (
                <div>
                    <Form.Group className="mb-3" controlId="formBasicPasswordRegister">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Password" autoComplete='false' onChange={
                            (e)=>setformData({...formdata,password:e.target.value})
                            } />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicPasswordRepeat">
                        <Form.Label>Repeat Password</Form.Label>
                        <Form.Control type="password" placeholder="Password"onChange={
                            (e)=>setformData({...formdata,password1:e.target.value})
                            } />
                    </Form.Group>
                    <div style={{color:'red'}}>
                        {match?'':'Passwords do not match'}
                    </div>
                    
                </div>
            )
        }
        

        <Button style={{width:'100%'}} variant="primary" type="submit" disabled= {!formdata['loginMode']&!match || formdata['password']===''}>
                Submit
        </Button>

        <div style={{display:'flex', justifyContent:'space-evenly', marginTop:'1rem',alignItems:'baseline'}}>
            Or
            <Button variant="primary" type="reset" onClick={switchMode}>
                {formdata['loginMode']? 'Sign Up':'Sign In'}
            </Button>
        </div>
            {alert['enabled']&&<Alert severity={alert['severity']}>{alert['text']}</Alert>}
        </Form>
    </div>
  );
}

export default LoginForm;