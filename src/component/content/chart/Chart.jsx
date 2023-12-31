import './Chart.css';
import { BarChart, Tooltip, Legend, Line, LineChart, XAxis, YAxis, Bar } from 'recharts';


const SubLineChart = ({ data }) => {
    return (
        <LineChart width={200} height={120} data={data}>
            <Line type={'monotone'} dataKey='daily_count' dot={false} strokeWidth={3} />
        </LineChart>
    );
};

const SubBarChart = ({ data }) => {
    return (
        <BarChart width={100} height={70} data={data}>
            <Tooltip />
            <Bar dataKey={"daily_count"} fill='#8884d8' />
        </BarChart>
    );
}


export { SubLineChart, SubBarChart };