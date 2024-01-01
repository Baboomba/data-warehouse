import './Header.css';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import { useEffect, useState } from 'react';
import { ListModal } from '../modal/modal';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import SearchIcon from '@mui/icons-material/Search';
import { useDispatch, useSelector } from 'react-redux';
import { logOut } from '../../slices/loginSlice';


const SearchBar = () => {
    const [searchWord, setSearchWord] = useState('');
    const handleChange = (e) => {
        setSearchWord(e.target.value);
    };

    useEffect(() => {
        console.log(searchWord);
    }, [searchWord])

    return (
        <div className='header-search-bar'>
            <span>
                <SearchIcon className='search-bar-icon' />
                <input
                  placeholder='search...'
                  onChange={handleChange}
                />
            </span>
        </div>
    );
};

const CenterHeader = () => {
    return (
        <div className='center-header'>
            <div className='header-left'>
                <SearchBar />
            </div>
            <div className='header-center'></div>
        </div>
    );
};

const RightHeader = () => {
    const [isClicked, setIsClicked] = useState(false);
    const handleSettings = () => {
        setIsClicked(!isClicked);
    }

    const navigate = useNavigate();

    const refresh = useSelector((state) => state.auth.refresh);
    const dispatch = useDispatch();

    const handleLogout = async () => {
        const url = 'http://localhost:8000/api/logout/';
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
                console.log('logout ok')
                dispatch(logOut());
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