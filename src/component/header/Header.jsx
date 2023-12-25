import './Header.css';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import { useState } from 'react';
import { ListModal } from '../modal/modal';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';



const CenterHeader = () => {
    return (
        <div className='center-header'>
            <div className='header-left'>left</div>
            <div className='header-center'>center</div>
        </div>
    );
};

const RightHeader = () => {
    const [isClicked, setIsClicked] = useState(false);
    const handleSettings = () => {
        setIsClicked(!isClicked);
    }

    const navigate = useNavigate();
    const handleLogout = async () => {
        const url = 'http://localhost:8000/api/logout/';
        const refresh = sessionStorage.getItem('refresh');
        const getCSRFTokenFromCookie = () => {
            const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
            return csrfCookie ? csrfCookie.split('=')[1] : null;
        };


        try {
            const response = await axios.post(url, { refresh }, {
                withCredentials: true,
                headers: {
                    'X-CSRFToken': getCSRFTokenFromCookie()
                }
            });
            
            if (response.status === 200) {
                sessionStorage.removeItem('isLoggedIn');
                navigate('/login');
            }
        } catch (error) {
            console.error('reponse await error');
        }
    };

    return (
        <div className='right-header'>
            <label className='settings-btn' onClick={handleSettings}>
                <SettingsIcon />
                settings
            </label>
            <label className='logout-btn' onClick={handleLogout}>
                <LogoutIcon />
                log-out
            </label>
            <ListModal onClicked={isClicked} handleClick={handleSettings} />
        </div>
    );
}

export { CenterHeader, RightHeader };