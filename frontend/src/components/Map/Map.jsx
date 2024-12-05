import React from "react";
import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";

const mapContainerStyle = {
	width: "100%",
	height: "400px",
};

const center = {
	lat: 40.748817, // Central location, e.g., Conference Headquarters
	lng: -73.985428,
};

const Map = ({ locations }) => {
	return (
		<LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
			<GoogleMap
				mapContainerStyle={mapContainerStyle}
				center={center}
				zoom={12}
			>
				{locations.map((location) => (
					<Marker
						key={location.id}
						position={{ lat: location.lat, lng: location.lng }}
						title={location.name}
					/>
				))}
			</GoogleMap>
		</LoadScript>
	);
};

export default Map;
