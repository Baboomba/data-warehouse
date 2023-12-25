import './Main.css';
import CounterBoard from '../counter/Counter';


const MainContent = () => {
    
    return (
        <div className='main-content-area'>
            <div className='main-count-area'>
                <div className="main-content-count">
                    <CounterBoard />
                </div>
                <div className="main-content-count">count 2</div>
                <div className="main-content-count">count 3</div>
            </div>
            <div className='main-chart-area'>
                <div className="main-content-chart">chart 1</div>
                <div className="main-content-chart">chart 2</div>
                <div className="main-content-chart">chart 3</div>
            </div>
        </div>
    );
};

export { MainContent };