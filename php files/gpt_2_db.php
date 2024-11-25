<?php
// Database connection parameters
$servername = "localhost"; // e.g., localhost or your database server
$username = "YOUR_DATABASE_USERNAME"; // Database username
$password = "YOUR_DATABASE_PASSWORD"; // Database password
$dbname = "YOUR_DATABASE_NAME"; // Database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get the stock symbol from the POST request
$symbol = $_POST['symbol'];

// Prepare and execute the SQL query
$sql = "SELECT created_at, summary, sentiment FROM stock_analysis WHERE stock_symbol = ? ORDER BY created_at DESC LIMIT 1";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $symbol);
$stmt->execute();
$stmt->bind_result($created_at, $summary, $sentiment);
$stmt->fetch();
$stmt->close();
$conn->close();

// Prepare the response
$response = "Created at: " . $created_at ."\nSummary: " . $summary . "\nSentiment: " . $sentiment;

// Save response to a TXT file
//file_put_contents("response.txt", $response);

// Output the response
echo $response;
?>