import './Main.css';


const MainContent = () => {
    return (
        <div className='main-content-area'>
            <div className='main-chart-area'>
                <div className="main-content-chart">chart 1</div>
                <div className="main-content-chart">chart 2</div>
                <div className="main-content-chart">chart 3</div>
            </div>
            <div className='main-board-area'>
                <div className="main-board-area">board 1</div>
                <div className="main-board-area">board 2</div>
                <div className="main-board-area">board 3</div>
            </div>
        </div>
    );
};

export { MainContent };