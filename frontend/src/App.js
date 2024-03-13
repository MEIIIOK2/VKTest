import logo from './logo.svg';
import './App.css';
import LoginForm from './components/LoginForm';
import useIsAuthenticated from 'react-auth-kit/hooks/useIsAuthenticated';
import ImageUploader from './components/ImageUploader';
import LogoutButton from './components/LogoutButton';
import { useState } from 'react';
import axios from 'axios';
import { useEffect } from 'react';
import cookie from 'react-cookies';

function App() {
  const [authorized, setAuthorized] = useState(cookie.load('authorized'));
  const handleAuth = (value) =>{
    setAuthorized(value)
    if (!value) {
      cookie.remove('authorized')
    }
  }
  const [image, setImage] = useState()

  const getImage =() =>{
      axios.get(process.env.REACT_APP_BACKEND_URL+'api/avatar/').then((res)=>{
        if (res.status==200) {
          setImage(res.data)
        }
      })
  }

  useEffect(()=>{
   
    
    
    const sessionid = cookie.load('sessionid');
    if (sessionid) {
      handleAuth(true);
    }

    const csrftoken = cookie.load('csrftoken');
    if (! csrftoken) {
      axios.get(process.env.REACT_APP_BACKEND_URL+'api/csrf/').then((res)=>{
        if (res.status == 200) {
          axios.defaults.headers.post['X-CSRFToken'] = cookie.load('csrftoken');
        }
      })
    }
    else{
      axios.defaults.headers.post['X-CSRFToken'] = csrftoken;
    }
    if (authorized) {
      getImage(); 
    }
    
  },[authorized])


  if (authorized) {
    return(
      <div>
        <div className='userPanel'>
          <LogoutButton handleAuth ={handleAuth} image = {image}></LogoutButton>
        </div>
        
        <ImageUploader getImage={getImage}></ImageUploader>
      </div>
    )
  }
  return (
    <div className="App">
     <LoginForm handleAuth ={handleAuth}/>
    </div>
  );
 
}

export default App;
