import { useEffect, useState } from "react";

export default function AnalyticsBoard() {
    const [data, setData] = useState([]);
    const [analytics, setAnalytics] = useState({
        totalRequests: 0,
        past7DaysRequests: 0,
        past10HoursRequests: 0,
        timeSinceLastRequest: "N/A",
        averageDimmingValue: "N/A",
    });

    useEffect(() => {
        async function fetchData() {
            const response = await fetch("/api");
            const patients = await response.json();
            setData(patients);
        }
        fetchData();
    }, []);

    useEffect(() => {
        if (data.length > 0) {
            const now = new Date();
            const sevenDaysAgo = new Date();
            const tenHoursAgo = new Date();

            sevenDaysAgo.setDate(now.getDate() - 7);
            tenHoursAgo.setHours(now.getHours() - 10);

            const totalRequests = data.length;
            const past7DaysRequests = data.filter((entry) => {
                const timestamp = new Date(entry.timestamp);
                timestamp.addHours(5);
                return timestamp >= sevenDaysAgo && timestamp <= now;
            }).length;

            const past10HoursRequests = data.filter((entry) => {
                const timestamp = new Date(entry.timestamp);
                timestamp.addHours(5);
                return timestamp >= tenHoursAgo && timestamp <= now;
            }).length;

            const lastRequest = data[0]; // Assuming data is already sorted by timestamp
            const timeSinceLastRequest = lastRequest
                ? formatTimeDifference(new Date(lastRequest.timestamp).addHours(5), now)
                : "N/A";

            const dimmingValues = data
                .filter((entry) => entry.action === "dimming_lights")
                .map((entry) => parseFloat(entry.value.replace("%", "")));

            const averageDimmingValue =
                dimmingValues.length > 0
                    ? (dimmingValues.reduce((sum, value) => sum + value, 0) / dimmingValues.length).toFixed(2) + "%"
                    : "N/A";

            setAnalytics({
                totalRequests,
                past7DaysRequests,
                past10HoursRequests,
                timeSinceLastRequest,
                averageDimmingValue,
            });
        }
    }, [data]);

    Date.prototype.addHours= function(h){
        this.setHours(this.getHours()+h);
        return this;
    }

    // Helper function to format time difference
    function formatTimeDifference(start, end) {
        const diffMs = end - start; // Difference in milliseconds
        const diffMinutes = Math.floor(diffMs / (1000 * 60));
        const hours = Math.floor(diffMinutes / 60);
        const minutes = diffMinutes % 60;

        return `${hours} hour(s) and ${minutes} minute(s) ago`;
    }

    return (
        <div className="p-6 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* <div className="p-4 bg-blue-100 rounded-lg shadow">
                    <h2 className="text-lg font-semibold">Total Nurse Requests</h2>
                    <p className="text-3xl font-bold">{analytics.totalRequests}</p>
                </div> */}
                <div className="p-4 bg-green-100 rounded-lg shadow">
                    <h2 className="text-md font-semibold">Requests in Past 7 Days</h2>
                    <p className="text-xl font-bold">{analytics.past7DaysRequests}</p>
                </div>
                <div className="p-4 bg-purple-100 rounded-lg shadow">
                    <h2 className="text-md font-semibold">Requests in Past 10 Hours</h2>
                    <p className="text-xl font-bold">{analytics.past10HoursRequests}</p>
                </div>
                <div className="p-4 bg-green-100 rounded-lg shadow">
                    <h2 className="text-md font-semibold">Time Since Last Nurse Visit</h2>
                    <p className="text-xl font-bold">{analytics.timeSinceLastRequest}</p>
                </div>
                <div className="p-4 bg-purple-100 rounded-lg shadow">
                    <h2 className="text-md font-semibold">Average Dimming Lights Value</h2>
                    <p className="text-xl font-bold">{analytics.averageDimmingValue}</p>
                </div>
            </div>
            <div className="p-4 bg-gray-100 rounded-lg shadow">
                <h2 className="text-nd font-semibold">Recent Requests</h2>
                <ul className="divide-y divide-gray-300">
                    {data.slice(0, 5).map((entry) => (
                        <li key={entry._id} className="py-2">
                            <p className="font-medium">Action: {entry.action}</p>
                            <p className="text-sm text-gray-600">
                                Value: {entry.value} | Time: {new Date(entry.timestamp).addHours(5).toLocaleString()}
                            </p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}
