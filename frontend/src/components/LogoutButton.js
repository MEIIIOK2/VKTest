import React from 'react';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/esm/Image';
import useSignOut from 'react-auth-kit/hooks/useSignOut';
import axios from 'axios';

const LogoutButton = ({handleAuth ,image}) => {


  return (
    <div className='user-panel'>
            {image && <Image src={`data:image/jpeg;base64,${image}`} alt="Selected image" style={{ width: '4rem', height:'4rem', objectFit: 'cover'}}  roundedCircle  />}

      <Button  onClick={() => {
      axios.post(process.env.REACT_APP_BACKEND_URL+'api/logout/').then((res)=>{
        if (res.status == 200) {
          handleAuth(false);
        }
      })
    }}>
      Log Out
    </Button>
    </div>
    
  );
};

export default LogoutButton;