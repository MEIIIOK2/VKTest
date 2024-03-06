import logo from './logo.svg';
import './App.css';
import LoginForm from './components/LoginForm';
import useIsAuthenticated from 'react-auth-kit/hooks/useIsAuthenticated';
import ImageUploader from './components/ImageUploader';
import LogoutButton from './components/LogoutButton';
import { useState } from 'react';
import axios from 'axios';
import { useEffect } from 'react';

function App() {
  const isAuthenticated = useIsAuthenticated();
  const [authorized, sertAuthorized] = useState(isAuthenticated());
  const handleAuth = () =>{
    sertAuthorized(isAuthenticated())
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
    if (authorized) {
      getImage()
    }
    
  })


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
