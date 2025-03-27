#!/bin/bash

# Ask user for app name
read -p "Please enter your app name (without .fly.dev): " APP_NAME

# Validate app name is not empty
if [ -z "$APP_NAME" ]; then
    echo "Error: App name cannot be empty"
    exit 1
fi

# Create base URL with app name
BASE_URL="https://$APP_NAME.fly.dev"
REQUEST_URL="$BASE_URL/api/go-to-url?url=https%3A%2F%2Fwww.flychicago.com%2Fbusiness%2Fopportunities%2Fbidscontracts%2Falerts%2FPages%2Farticle.aspx%3Fnewsid%3D1666&ua=Mozilla%2F5.0%20(X11%3B%20Linux%20x86_64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F134.0.0.0%20Safari%2F537.36&trace=true"
TRACE_URL="$BASE_URL/api/get-trace"

# Number of requests
NUM_REQUESTS=5

# Create timestamp for unique folder
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_DIR="curl_results_${TIMESTAMP}"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Summary file
SUMMARY_FILE="$OUTPUT_DIR/summary.txt"

echo "Starting $NUM_REQUESTS curl requests to $BASE_URL..."
echo "Results will be stored in $OUTPUT_DIR/"

# Run the curl command NUM_REQUESTS times
for ((i=1; i<=$NUM_REQUESTS; i++)); do
    # Create request-specific directory
    REQUEST_DIR="$OUTPUT_DIR/request_$i"
    mkdir -p "$REQUEST_DIR"
    
    echo "Processing request $i/$NUM_REQUESTS"
    
    # File paths for this request
    RESPONSE_BODY="$REQUEST_DIR/response.html"
    STATUS_FILE="$REQUEST_DIR/status.txt"
    TRACE_FILE="$REQUEST_DIR/trace.zip"
    
    # Run curl and save both status code and response body
    HTTP_STATUS=$(curl -s -w "%{http_code}" --location "$REQUEST_URL" -o "$RESPONSE_BODY")
    
    # Save status code to file
    echo "$HTTP_STATUS" > "$STATUS_FILE"
    
    # Get trace zip file
    echo "Retrieving trace for request $i..."
    curl -s --location "$TRACE_URL" -o "$TRACE_FILE"
    
    # Append to main results list
    echo "$i,$HTTP_STATUS" >> "$OUTPUT_DIR/all_statuses.csv"
    
    # Add a small delay to avoid overwhelming the server
    sleep 0.5
done

echo "All requests completed. Generating summary..."

# Generate summary
echo "Status Code Summary:" > "$SUMMARY_FILE"
echo "----------------" >> "$SUMMARY_FILE"
cat "$OUTPUT_DIR/all_statuses.csv" | cut -d ',' -f 2 | sort | uniq -c | sort -nr | while read count code; do
    percentage=$(echo "scale=2; $count * 100 / $NUM_REQUESTS" | bc)
    echo "HTTP $code: $count times ($percentage%)" >> "$SUMMARY_FILE"
done

# Add timestamp
echo "" >> "$SUMMARY_FILE"
echo "Test completed at: $(date)" >> "$SUMMARY_FILE"

# Display summary
cat "$SUMMARY_FILE"
echo ""
echo "Complete results stored in $OUTPUT_DIR/"
echo "- Each request has its own folder with response body, status code, and trace file"
echo "- Summary available at $SUMMARY_FILE"