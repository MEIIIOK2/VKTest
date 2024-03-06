import React from 'react';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/esm/Image';
import useSignOut from 'react-auth-kit/hooks/useSignOut';

const LogoutButton = ({handleAuth ,image}) => {

  const signOut = useSignOut();

  return (
    <div className='user-panel'>
            {image && <Image src={`data:image/jpeg;base64,${image}`} alt="Selected image" style={{ width: '4rem', height:'4rem', objectFit: 'cover'}}  roundedCircle  />}

      <Button  onClick={() => {
      signOut();
      handleAuth();
    }}>
      Log Out
    </Button>
    </div>
    
  );
};

export default LogoutButton;