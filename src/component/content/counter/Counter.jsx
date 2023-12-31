import axios from 'axios';
import './Counter.css';
import { useEffect, useState } from 'react';
import { SubLineChart } from '../chart/Chart';
import MoreVertIcon from '@mui/icons-material/MoreVert';


const DailyCounter = () => {
    const [totalCount, setTotalCount] = useState(0);
    const fetchTotalCount = async () => {
        try {
            let url = 'http://localhost:8000/stats/total-member';
            const res = await axios.get(url, { withCredentials : true });
            setTotalCount(res.data.monthly_join);
        } catch (error) {
            console.log(`request failed : ${error}`);
        }
    };

    const [monthlyJoin, setMonthlyJoin] = useState([]);
    const fetchMonthlyJoin = async () => {
        let url = 'http://localhost:8000/stats/monthly-join';
        const res = await axios.get(url, { withCredentials : true });
        setMonthlyJoin(res.data);
    }

    const formatNumber = () => {
        const styled = { style: 'decimal' }
        return totalCount.toLocaleString('en-US', styled);
    };

    const currentMonth = () => {
        const currentDate = new Date();
        const currentMonth = currentDate.toLocaleString('default', { month: 'long' });
        return currentMonth;
    }

    const [isHidden, setIsHidden] = useState(false);
    const handleModal = () => {
        setIsHidden(!isHidden);
    }

    useEffect(() => {
        fetchTotalCount();
        fetchMonthlyJoin();
    }, []);

    return (
        <div className='counter-area'>
            <div className="counter-header">
                <label>일일 가입자</label>
                <button onClick={handleModal}>
                    <MoreVertIcon />
                </button>
                <div>
                    {isHidden && (
                        <button>자세히..</button>
                    )}
                </div>
            </div>
            <div className="counter-body">
                <SubLineChart data={monthlyJoin} />
            </div>
            <div className="counter-footer">
                <span>{currentMonth()} 누적</span>
                <label>{formatNumber()}</label>
            </div>
        </div>
    );
};

export default DailyCounter;