<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Read the raw binary data from the request body
    $binaryData = file_get_contents("php://input");

    // Extract headers
    $headers = getallheaders();
    $filename = '';

    // Check if the Content-Disposition header is set
    if (isset($headers['Content-Disposition'])) {
        // Use a regex to extract the filename from the header
        if (preg_match('/filename="?(?<filename>[^"]+)"?/', $headers['Content-Disposition'], $matches)) {
            $filename = basename($matches['filename']);
        }
    }

    // If no filename is extracted, fall back to a default name
    if (empty($filename)) {
        $filename = 'screenshot_' . time() . '.png'; // Default name
    } else {
        // Ensure the file extension is .png
        if (pathinfo($filename, PATHINFO_EXTENSION) !== 'png') {
            $filename .= '.png';
        }
    }

    // Set the upload directory to the same directory as this script
    $uploadDir = dirname(__FILE__) . '/'; // Current directory
    $uploadFile = $uploadDir . $filename; // Use the extracted or default filename

    // Write the binary data to a new PNG file
    if (file_put_contents($uploadFile, $binaryData) !== false) {
        echo "File is valid and was successfully uploaded: " . $uploadFile;
    } else {
        echo "Failed to write the file.";
    }
} else {
    echo "Invalid request method.";
}
?>