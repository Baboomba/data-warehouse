import { Form }  from 'react-bootstrap';
import './Modal.css';
import CloseIcon from '@mui/icons-material/Close';
import SyncIcon from '@mui/icons-material/Sync';
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';
import { useState } from 'react';


const ModalContent = ({ handleClick }) => {
    const [isDarkMode, setIsDarkMode] = useState(() => {
        return localStorage.getItem('dark mode') === 'true' ? true : false
    });
    
    const handleCheck = () => {
        setIsDarkMode(prevIsDarkMode => {
            const newIsDarkMode = !prevIsDarkMode;
            localStorage.setItem('dark mode', newIsDarkMode);
            return newIsDarkMode;
        });
    };
    
    return (
        <div className='modal-content-area'>
            <span className='list-modal-title'>
                <CloseIcon
                  className='modal-close-icon'
                  onClick={handleClick}
                />
            </span>
            <ul className='modal-list'>
                <li className='modal-list-item'>
                    <label>Dark Mode</label>
                    <Form>
                        <Form.Check
                          type='switch'
                          defaultChecked={isDarkMode}
                          onClick={handleCheck}
                        />
                    </Form>
                </li>
                <li className='modal-list-item'>
                    <label>Data Update</label>
                    <SyncIcon
                      className='data-sync-icon'
                    />
                </li>
                <li className='modal-list-item'>
                    <label>Help</label>
                    <QuestionMarkIcon
                      className='help-icon'
                    />
                </li>
            </ul>
        </div>
    );
};

const ListModal = ({ onClicked, handleClick }) => {
    return (
        <div
          className={
            onClicked ?
            'list-modal-container' :
            'list-modal-container-hidden'
          }
        >
            <ModalContent handleClick={handleClick} />
        </div>
    );
};

export { ListModal };