import './Header.css';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import { Button } from 'react-bootstrap';


const CenterHeader = () => {
    return (
        <div className='header-container'>
            <div className='header-left'>left</div>
            <div className='header-center'>center</div>
        </div>
    );
};

const RightHeader = () => {
    return (
        <div className='right-header'>
            <label className='settings-btn'>
                <SettingsIcon />
                settings
            </label>
            <label className='logout-btn'>
                <LogoutIcon />
                log-out
            </label>
        </div>
    );
}

export { CenterHeader, RightHeader };