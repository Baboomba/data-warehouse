import axios from 'axios';
import './Chart.css';
import { BarChart, Tooltip, Legend, Line, LineChart, XAxis, YAxis } from 'recharts';


const MainChart = () => {
    const handleData = async () => {
        const response = await axios.get();
    };

    return (
        <LineChart width={250} height={200}>
            <XAxis />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type={'monotone'} />
        </LineChart>
    );
};


export { MainChart };