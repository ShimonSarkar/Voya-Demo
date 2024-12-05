import React, { useEffect, useState } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";
import "./Trip.css";
import Map from "../../components/Map/Map";

const localizer = momentLocalizer(moment);

const Trip = () => {
    // State Management
    const [events, setEvents] = useState([]);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState("");
    const [selectedExpenses, setSelectedExpenses] = useState({
        expenses: [],
        totalExpense: 0,
    });
    const [selectedLocations, setSelectedLocations] = useState([
        { id: 1, name: "Conference Headquarters", lat: 40.748817, lng: -73.985428 },
    ]);

    // Data Sets
    const Events0 = [
        {
            trip_id: 1,
            entity_id: 102,
            entity_type: "reservation",
            summary: "Conference: Day 1",
            start_time: "2024-12-11T10:00:00-05:00",
            end_time: "2024-12-11T17:00:00-05:00",
            description: "Conference: Day 1",
            location: "Company HQ",
        },
        {
            trip_id: 1,
            entity_id: 104,
            entity_type: "reservation",
            summary: "Conference: Day 2",
            start_time: "2024-12-12T10:00:00-05:00",
            end_time: "2024-12-12T17:00:00-05:00",
            description: "Conference: Day 2",
            location: "Company HQ",
        },
    ];

    const Expenses0 = {
        expenses: [],
        totalExpense: 0,
    };

    const Events1 = [
        {
            trip_id: 1,
            entity_id: 101,
            entity_type: "flight",
            summary: "Flight to NYC: Flight A",
            start_time: "2024-12-10T15:00:00-05:00",
            end_time: "2024-12-10T21:00:00-05:00",
            description: "Flight from San Francisco to New York",
            location: "Airport A",
        },
        {
            trip_id: 1,
            entity_id: 102,
            entity_type: "reservation",
            summary: "Conference: Day 1",
            start_time: "2024-12-11T10:00:00-05:00",
            end_time: "2024-12-11T17:00:00-05:00",
            description: "Conference: Day 1",
            location: "Company HQ",
        },
        {
            trip_id: 1,
            entity_id: 103,
            entity_type: "reservation",
            summary: "Dinner at Restaurant A",
            start_time: "2024-12-11T18:00:00-05:00",
            end_time: "2024-12-11T20:00:00-05:00",
            description: "Dinner at Restaurant A",
            location: "Restaurant A",
        },
        {
            trip_id: 1,
            entity_id: 104,
            entity_type: "reservation",
            summary: "Conference: Day 2",
            start_time: "2024-12-12T10:00:00-05:00",
            end_time: "2024-12-12T17:00:00-05:00",
            description: "Conference: Day 2",
            location: "Company HQ",
        },
        {
            trip_id: 1,
            entity_id: 105,
            entity_type: "reservation",
            summary: "Dinner at Restaurant B",
            start_time: "2024-12-12T18:00:00-05:00",
            end_time: "2024-12-12T20:00:00-05:00",
            description: "Dinner at Restaurant B",
            location: "Restaurant B",
        },
        {
            trip_id: 1,
            entity_id: 106,
            entity_type: "flight",
            summary: "Flight to SF: Flight B",
            start_time: "2024-12-13T08:00:00-05:00",
            end_time: "2024-12-13T14:00:00-05:00",
            description: "Flight from New York to San Francisco",
            location: "Airport A",
        },
    ];

    const Expenses1 = {
        tripId: 1,
        totalExpense: 1705,
        expenses: [
            {
                category: "Flight",
                items: [
                    { description: "Flight to NYC: Flight A", amount: 350 },
                    { description: "Flight to SF: Flight B", amount: 400 },
                ],
            },
            {
                category: "Accommodation",
                items: [{ description: "Hotel A: 2 Nights", amount: 750 }],
            },
            {
                category: "Meals (Projected Expense)",
                items: [
                    { description: "Restaurant A", amount: 50 },
                    { description: "Restaurant B", amount: 50 },
                ],
            },
            {
                category: "Transport (Projected Expense)",
                items: [
                    {
                        description: "Ubers",
                        rides: [
                            { route: "Airport A to Hotel A", amount: 50 },
                            { route: "Hotel A to Company HQ", amount: 10 },
                            { route: "Company HQ to Restaurant A", amount: 15 },
                            { route: "Restaurant A to Hotel A", amount: 27 },
                            { route: "Hotel A to Company HQ", amount: 10 },
                            { route: "Company HQ to Restaurant B", amount: 17 },
                            { route: "Restaurant B to Hotel A", amount: 26 },
                            { route: "Hotel A to Airport A", amount: 50 },
                        ],
                    },
                ],
            },
        ],
    };

    const Events2 = [
        {
            trip_id: 1,
            entity_id: 101,
            entity_type: "flight",
            summary: "Flight to NYC: Flight C",
            start_time: "2024-12-10T13:00:00-05:00",
            end_time: "2024-12-10T19:00:00-05:00",
            description: "Flight from San Francisco to New York",
            location: "Airport C",
        },
        {
            trip_id: 1,
            entity_id: 102,
            entity_type: "reservation",
            summary: "Conference: Day 1",
            start_time: "2024-12-11T10:00:00-05:00",
            end_time: "2024-12-11T17:00:00-05:00",
            description: "Conference: Day 1",
            location: "Company HQ",
        },
        {
            trip_id: 1,
            entity_id: 103,
            entity_type: "reservation",
            summary: "Dinner at Restaurant A",
            start_time: "2024-12-11T18:00:00-05:00",
            end_time: "2024-12-11T20:00:00-05:00",
            description: "Dinner at Restaurant A",
            location: "Restaurant A",
        },
        {
            trip_id: 1,
            entity_id: 104,
            entity_type: "reservation",
            summary: "Conference: Day 2",
            start_time: "2024-12-12T10:00:00-05:00",
            end_time: "2024-12-12T17:00:00-05:00",
            description: "Conference: Day 2",
            location: "Company HQ",
        },
        {
            trip_id: 1,
            entity_id: 105,
            entity_type: "reservation",
            summary: "Dinner at Restaurant B",
            start_time: "2024-12-12T18:00:00-05:00",
            end_time: "2024-12-12T20:00:00-05:00",
            description: "Dinner at Restaurant B",
            location: "Restaurant B",
        },
        {
            trip_id: 1,
            entity_id: 106,
            entity_type: "flight",
            summary: "Flight to SF: Flight B",
            start_time: "2024-12-13T08:00:00-05:00",
            end_time: "2024-12-13T14:00:00-05:00",
            description: "Flight from New York to San Francisco",
            location: "Airport A",
        },
    ];

    const Expenses2 = {
        tripId: 1,
        totalExpense: 1705,
        expenses: [
            {
                category: "Flight",
                items: [
                    { description: "Flight to NYC: Flight C", amount: 375 },
                    { description: "Flight to SF: Flight B", amount: 400 },
                ],
            },
            {
                category: "Accommodation",
                items: [{ description: "Hotel A: 2 Nights", amount: 750 }],
            },
            {
                category: "Meals",
                items: [
                    { description: "Restaurant A (projected expense)", amount: 50 },
                    { description: "Restaurant B (projected expense)", amount: 50 },
                ],
            },
            {
                category: "Transport",
                items: [
                    {
                        description: "Ubers (projected expense)",
                        rides: [
                            { route: "Airport A to Hotel A", amount: 50 },
                            { route: "Hotel A to Company HQ", amount: 10 },
                            { route: "Company HQ to Restaurant A", amount: 15 },
                            { route: "Restaurant A to Hotel A", amount: 27 },
                            { route: "Hotel A to Company HQ", amount: 10 },
                            { route: "Company HQ to Restaurant B", amount: 17 },
                            { route: "Restaurant B to Hotel A", amount: 26 },
                            { route: "Hotel A to Airport A", amount: 50 },
                        ],
                    },
                ],
            },
        ],
    };

    const Events3 = [
        {
            trip_id: 1,
            entity_id: 101,
            entity_type: "flight",
            summary: "Flight to NYC: Flight C",
            start_time: "2024-12-10T13:00:00-05:00",
            end_time: "2024-12-10T19:00:00-05:00",
            description: "Flight from San Francisco to New York",
            location: "Airport C",
        },
        {
            trip_id: 1,
            entity_id: 102,
            entity_type: "reservation",
            summary: "Conference: Day 1",
            start_time: "2024-12-11T10:00:00-05:00",
            end_time: "2024-12-11T17:00:00-05:00",
            description: "Conference: Day 1",
            location: "Company HQ",
        },
        {
            trip_id: 1,
            entity_id: 103,
            entity_type: "reservation",
            summary: "Dinner at Restaurant A",
            start_time: "2024-12-11T18:00:00-05:00",
            end_time: "2024-12-11T20:00:00-05:00",
            description: "Dinner at Restaurant A",
            location: "Restaurant A",
        },
        {
            trip_id: 1,
            entity_id: 104,
            entity_type: "reservation",
            summary: "Conference: Day 2",
            start_time: "2024-12-12T10:00:00-05:00",
            end_time: "2024-12-12T17:00:00-05:00",
            description: "Conference: Day 2",
            location: "Company HQ",
        },
        {
            trip_id: 1,
            entity_id: 107,
            entity_type: "reservation",
            summary: "Emergency Meeting",
            start_time: "2024-12-12T17:30:00-05:00",
            end_time: "2024-12-12T18:30:00-05:00",
            description: "Emergency Meeting",
            location: "Company HQ",
        },
        {
            trip_id: 1,
            entity_id: 105,
            entity_type: "reservation",
            summary: "Dinner at Restaurant B",
            start_time: "2024-12-12T19:00:00-05:00",
            end_time: "2024-12-12T21:00:00-05:00",
            description: "Dinner at Restaurant B",
            location: "Restaurant B",
        },
        {
            trip_id: 1,
            entity_id: 106,
            entity_type: "flight",
            summary: "Flight to SF: Flight B",
            start_time: "2024-12-13T08:00:00-05:00",
            end_time: "2024-12-13T14:00:00-05:00",
            description: "Flight from New York to San Francisco",
            location: "Airport A",
        },
    ];

    const locations0 = [
        { id: 1, name: "Conference Headquarters", lat: 40.748817, lng: -73.985428 },
    ];

    const locations1 = [
        { id: 1, name: "Conference Headquarters", lat: 40.748817, lng: -73.985428 },
        { id: 2, name: "Hotel A", lat: 40.752622, lng: -73.977229 },
        { id: 3, name: "Hotel B", lat: 40.756977, lng: -73.986941 },
        { id: 4, name: "Airport A", lat: 40.641766, lng: -73.780968 },
        { id: 5, name: "Restaurant A", lat: 40.73061, lng: -73.935242 },
        { id: 6, name: "Restaurant B", lat: 40.741895, lng: -73.989308 },
    ];

    // API Calls
    const fetchEvents = async () => {
        const token = localStorage.getItem("jwt");
        const startDate = "2024-12-01";
        const endDate = "2024-12-31";

        try {
            const response = await fetch(
                `http://localhost:5001/calendar/events?start_date=${startDate}&end_date=${endDate}`,
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );

            if (!response.ok) throw new Error("Failed to fetch events");

            const data = await response.json();
            if (data.events) {
                const formattedEvents = data.events.map((event) => ({
                    title: event.summary,
                    start: new Date(event.start),
                    end: new Date(event.end),
                }));
                setEvents(formattedEvents);
            }
        } catch (err) {
            setError(err.message);
            console.error("Error fetching calendar events:", err);
        }
    };

    const handleRemoveEvents = async () => {
        const token = localStorage.getItem("jwt");
        const start_time = "2024-12-01T00:00:00";
        const end_time = "2024-12-31T23:59:59";

        try {
            const response = await fetch(`http://localhost:5001/calendar/events/remove`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ start_time, end_time }),
            });

            if (!response.ok) throw new Error("Failed to remove events");

            const data = await response.json();
            setSuccessMessage(data.message);
            setEvents([]); // Clear events after removal
        } catch (err) {
            setError(err.message);
            console.error("Error removing calendar events:", err);
        }
    };

    const handleAddEvents = async ({ events, expenses, locations }) => {
        const token = localStorage.getItem("jwt");
        // Remove existing events before adding new ones
        await handleRemoveEvents();

        setSelectedExpenses(expenses);
        setSelectedLocations(locations);

        try {
            const response = await fetch(`http://localhost:5001/calendar/events/add-multiple`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ events }),
            });

            if (!response.ok) throw new Error("Failed to add events");

            const data = await response.json();
            setSuccessMessage(data.message);
            fetchEvents(); // Refresh events after addition
        } catch (err) {
            setError(err.message);
            console.error("Error adding calendar events:", err);
        }
    };

    useEffect(() => {
        fetchEvents();
    }, []);

    return (
        <>
            <div className="trip-container">
                <h1 className="trip-title">Trip 7302: NYC Conference</h1>
                <div className="calendar-component">
                    <Calendar
                        localizer={localizer}
                        events={events}
                        startAccessor="start"
                        endAccessor="end"
                        style={{ height: 500 }}
                    />
                </div>

                <div className="map-expenses-section">
                    <div className="map-container">
                        <Map locations={selectedLocations} />
                    </div>

                    {/* Projected Expenses Section */}
                    <div className="projected-expenses-section">
                        <h2 className="section-title">Projected Expenses</h2>
                        <div className="expense-cards-container">
                            {selectedExpenses.expenses.map((expenseCategory, index) => (
                                <div key={index} className="expense-card">
                                    <h3 className="expense-category-title">{expenseCategory.category}</h3>
                                    <div className="expense-items">
                                        {expenseCategory.items.map((item, idx) => (
                                            <div key={idx} className="expense-item">
                                                {item.rides ? (
                                                    <div>
                                                        <p className="expense-description">{item.description}</p>
                                                        <ul className="rides-list">
                                                            {item.rides.map((ride, rideIdx) => (
                                                                <li key={rideIdx} className="ride-item">
                                                                    {ride.route}: ${ride.amount}
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                ) : (
                                                    <p className="expense-description">
                                                        {item.description}: ${item.amount}
                                                    </p>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                        <h3 className="total-expense">
                            Total Expense: ${selectedExpenses.totalExpense}
                        </h3>
                    </div>
                </div>
            </div>

            <div className="trip-policy-section">
                <h2 className="policy-title">Trip Policy</h2>
                <ul className="policy-list">
                    <li>Flights are booked through approved vendors.</li>
                    <li>Hotel stays are limited to $400 per night.</li>
                    <li>Meals reimbursement capped at $50 per meal with a limit of 3 meals per day.</li>
                    <li>Transportation expenses include taxis, Ubers, and public transit.</li>
                    <li>All expenses must be submitted within 30 days post-trip.</li>
                </ul>

                <div className="events-buttons-section">
                    <button
                        className="add-events-button"
                        onClick={() => handleAddEvents({ events: Events0, expenses: Expenses0, locations: locations0 })}
                    >
                        Begin Demo
                    </button>
                    <button
                        className="add-events-button"
                        onClick={() => handleAddEvents({ events: Events1, expenses: Expenses1, locations: locations1 })}
                    >
                        Generate Itinerary
                    </button>
                    <button
                        className="add-events-button"
                        onClick={() => handleAddEvents({ events: Events2, expenses: Expenses2, locations: locations1 })}
                    >
                        Simulate Flight Delay
                    </button>
                    <button
                        className="add-events-button"
                        onClick={() => handleAddEvents({ events: Events3, expenses: Expenses2, locations: locations1 })}
                    >
                        Simulate Emergency Meeting
                    </button>
                    <button
                        className="remove-events-button"
                        onClick={() => {
                            setSelectedExpenses(Expenses0);
                            handleRemoveEvents();
                        }}
                    >
                        Clear All
                    </button>
                </div>
            </div>
        </>
    );
};

export default Trip;
