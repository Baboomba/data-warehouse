import './Chart.css';
import { BarChart, Tooltip, Legend, Line, LineChart, XAxis, YAxis, Bar } from 'recharts';


const SubLineChart = ({ data }) => {
    return (
        <LineChart width={150} height={100} data={data}>
            <Tooltip
              wrapperStyle={{ borderColor: 'transparent', boxShadow: 'none' }}
              contentStyle={{ background: 'transparent', border: 'none' }}
            />
            <Line type={'monotone'} dataKey='daily_count' dot={false} />
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