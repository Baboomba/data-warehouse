import './Chart.css';
import { BarChart, Tooltip, Legend, Line, LineChart, XAxis, YAxis, Bar } from 'recharts';


const SubLineChart = ({ data }) => {
    return (
        <LineChart width={250} height={200} data={data}>
            <XAxis />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type={'monotone'} />
        </LineChart>
    );
};

const SubBarChart = ({ data }) => {
    return (
        <BarChart width={100} height={70} data={data}>
            <Tooltip />
            <Bar dataKey={"policy_id"} fill='#8884d8' />
        </BarChart>
    );
}


export { SubLineChart, SubBarChart };