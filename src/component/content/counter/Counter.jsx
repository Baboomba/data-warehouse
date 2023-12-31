import axios from 'axios';
import './Counter.css';
import { useEffect, useState } from 'react';
import { SubLineChart } from '../chart/Chart';


const CounterBoard = () => {
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

    useEffect(() => {
        fetchTotalCount();
        fetchMonthlyJoin();
    }, []);

    return (
        <div className='counter-area'>
            <div className='counter-indicator'>
                <SubLineChart data={monthlyJoin} />
                <label>{formatNumber()}명</label>
            </div>
            <div className='counter-instruction'>
                일일 가입자
            </div>
            <div className='counter-date'>
                기준일 2023-12-15
            </div>
        </div>
    );
};

export default CounterBoard;