import './Logo.css';
import pyshicsImg from '../../../asset/physics.svg';

const Logo = () => {
    return (
        <div>
            <label className='logo-label'>
                <img className="logo-img" src={pyshicsImg} alt="it doesn't work" />
                WORK STATS
            </label>
        </div>
    );
};


export { Logo }