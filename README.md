Closest Place Finder
This FastAPI project provides an API for finding the closest place based on user input. You can use it to discover nearby locations by sending a POST request with a JSON payload containing the desired location name.

Getting Started
Run the FastAPI Server: Navigate to the project directory and run the FastAPI server:
uvicorn app3:app --host localhost --port 8000

Access the API Documentation: Open your web browser and navigate to http://localhost:8000/docs to view the Swagger API documentation. Here, you can explore the available endpoints and test them interactively.
Welcome Page: When you access the root URL http://localhost:8000/, you’ll be greeted with a welcoming HTML page for your FastAPI application.
API Usage
Closest Place Endpoint
Endpoint: POST /closest_place/
Request Payload:
JSON

{
  "name": "Lyon"
}

in Terminal: curl -X POST -H "Content-Type: application/json" -d '{"name":"Lyon"}' http://localhost:8000/closest_place/


Response: The API will return information about the closest place to the specified location.
Additional API Endpoint Latitude , Longitude 
Endpoint: GET /cities/{city_name}
Example: To get information about Paris, make a GET request to http://localhost:8000/cities/Paris
Contributing
Feel free to contribute by opening issues or pull requests. Let’s make this API even better!
