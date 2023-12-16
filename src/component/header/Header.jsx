import './Header.css';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import { useState } from 'react';
import { ListModal } from '../modal/modal';



const CenterHeader = () => {
    return (
        <div className='header-container'>
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

    return (
        <div className='right-header'>
            <label className='settings-btn' onClick={handleSettings}>
                <SettingsIcon />
                settings
            </label>
            <label className='logout-btn'>
                <LogoutIcon />
                log-out
            </label>
            <ListModal onClicked={isClicked} />
        </div>
    );
}

export { CenterHeader, RightHeader };