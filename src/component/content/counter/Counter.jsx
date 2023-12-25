import axios from 'axios';
import './Counter.css';
import { useEffect, useState } from 'react';


const CounterBoard = () => {
    const [totalCount, setTotalCount] = useState(0);
    const fetchMonthlyJoin = async () => {
        try {
            let url = 'http://localhost:8000/stats/total-member';
            const res = await axios.get(url, { withCredentials: true });
            setTotalCount(res.data['total_count']);
        } catch (error) {
            console.log('request failed');
        }
    }

    useEffect(() => {
        fetchMonthlyJoin();
    }, []);

    return (
        <div className='counter-area'>
            <div className='counter-indicator'>
                <label>{totalCount}</label>
            </div>
            <div className='counter-instruction'>
                월간 누적 가입자
            </div>
            <div className='counter-date'>
                기준일 2023-12-15
            </div>
        </div>
    );
};

export default CounterBoard;