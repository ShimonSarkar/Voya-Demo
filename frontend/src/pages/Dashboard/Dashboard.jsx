import React from "react";
import "./Dashboard.css";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    Legend,
    PieChart,
    Pie,
    Cell,
    LineChart,
    Line,
    ResponsiveContainer,
} from "recharts";

// Expanded dummy data for the charts
const tripStats = [
    { month: "Jan", trips: 5 },
    { month: "Feb", trips: 8 },
    { month: "Mar", trips: 12 },
    { month: "Apr", trips: 15 },
    { month: "May", trips: 20 },
    { month: "Jun", trips: 25 },
    { month: "Jul", trips: 18 },
    { month: "Aug", trips: 22 },
    { month: "Sep", trips: 19 },
    { month: "Oct", trips: 24 },
    { month: "Nov", trips: 30 },
];

const reimbursementsData = [
    { name: "Approved", value: 4800 },
    { name: "Pending", value: 2200 },
    { name: "Rejected", value: 500 },
];

const costTrends = [
    { quarter: "Q1 2023", cost: 1200 },
    { quarter: "Q2 2023", cost: 1500 },
    { quarter: "Q3 2023", cost: 1100 },
    { quarter: "Q4 2023", cost: 1400 },
    { quarter: "Q1 2024", cost: 1300 },
    { quarter: "Q2 2024", cost: 1600 },
    { quarter: "Q3 2024", cost: 1150 },
    { quarter: "Q4 2024", cost: 1450 },
];

// Colors for the PieChart
const pieColors = ["#4caf50", "#f5a623", "#ff5733"];

// Expanded dummy data for reimbursements
const reimbursements = [
    {
        category: "Approved Reimbursements",
        items: [
            { description: "Flight to NYC", amount: "$400" },
            { description: "Hotel Stay", amount: "$800" },
            { description: "Client Dinner", amount: "$150" },
            { description: "Taxi to Airport", amount: "$75" },
            { description: "Conference Tickets", amount: "$300" },
        ],
        className: "approved",
    },
    {
        category: "Pending Reimbursements",
        items: [
            { description: "Flight to Chicago", amount: "$350" },
            { description: "Team Lunch", amount: "$200" },
            { description: "Ride to Hotel", amount: "$40" },
            { description: "Office Supplies", amount: "$60" },
        ],
        className: "pending",
    },
    {
        category: "Rejected Reimbursements",
        items: [
            { description: "Luxury Hotel Upgrade", amount: "$500" },
            { description: "Personal Expenses", amount: "$150" },
        ],
        className: "rejected",
    },
];

// Dummy data for upcoming trips
const upcomingTrips = [
    {
        title: "San Francisco to New York",
        description: "Business Conference",
        dates: "Dec 5 - Dec 7, 2024",
    },
    {
        title: "New York to Boston",
        description: "Client Meeting",
        dates: "Dec 10 - Dec 11, 2024",
    },
    {
        title: "Boston to Chicago",
        description: "Team Building Event",
        dates: "Dec 15 - Dec 18, 2024",
    },
];

const Dashboard = () => {
    return (
        <div className="dashboard">
            <h1 className="dashboard-title">Dashboard</h1>

            {/* Charts Section */}
            <div className="charts-section">
                <div className="charts-row">
                    <div className="chart-card">
                        <h3>Trips Completed</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={tripStats}>
                                <XAxis dataKey="month" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="trips" fill="#ff9505" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="chart-card">
                        <h3>Reimbursement Breakdown</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>
                                <Pie
                                    data={reimbursementsData}
                                    dataKey="value"
                                    nameKey="name"
                                    outerRadius={80}
                                >
                                    {reimbursementsData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={pieColors[index]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>
                <div className="charts-row">
                    <div className="chart-card">
                        <h3>Cost Per Trip</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <LineChart data={costTrends}>
                                <XAxis dataKey="quarter" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line
                                    type="monotone"
                                    dataKey="cost"
                                    stroke="#ff9505"
                                    strokeWidth={2}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Reimbursements Section */}
            <div className="reimbursements-section">
                <h2>Reimbursements</h2>
                <div className="reimbursements">
                    {reimbursements.map((reimbursement, index) => (
                        <div key={index} className={`reimbursement ${reimbursement.className}`}>
                            <h3>{reimbursement.category}</h3>
                            {reimbursement.items.map((item, idx) => (
                                <p key={idx}>
                                    {item.description}: {item.amount}
                                </p>
                            ))}
                        </div>
                    ))}
                </div>
            </div>

            {/* Upcoming Trips Section */}
            <div className="upcoming-trips-section">
                <h2>Upcoming Trips</h2>
                <div className="upcoming-trips">
                    {upcomingTrips.map((trip, index) => (
                        <div key={index} className="trip">
                            <h3>{trip.title}</h3>
                            <p>{trip.description}</p>
                            <p>{trip.dates}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
