window.onload = function () {
    let selectAllCheckbox = document.getElementById('selectAllCheckbox');
    selectAllCheckbox.addEventListener('change', function (e) {
        let checkboxes = document.querySelectorAll('input[name="wifi_ids"]');
        for (let checkbox of checkboxes) {
            checkbox.checked = e.target.checked;
        }
    });

    let deleteButtons = document.querySelectorAll('.delete-button');
    for (let button of deleteButtons) {
        button.addEventListener('click', function (e) {
            if (confirm('Are you sure you want to delete this item?')) {
                let form = document.createElement('form');
                form.method = 'POST';
                form.action = '/delete_wifi_data';
                let input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'wifi_ids';
                input.value = e.target.dataset.id;
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            }
        });
    }

    // ... [Rest of the existing code from the second script]

    const socket = io();

    // Connect to the server
    socket.connect();

    // Listen for the 'continuous_update' event from the server
    socket.on('continuous_update', data => {
        // Update the UI with current signal strength and moving average
        const currentStrengthDisplay = document.getElementById('currentStrength');
        const movingAvgDisplay = document.getElementById('movingAvg');

        currentStrengthDisplay.innerText = `Current Strength: ${data.current_strength}`;
        movingAvgDisplay.innerText = `Moving Average: ${data.moving_avg}`;
    });

    // Listen for the 'jamming_detected' event from the server
    socket.on('jamming_detected', data => {
        // Update the UI to indicate jamming detected
        const jammingStatus = document.getElementById('jamming-alert');
        jammingStatus.innerText = 'Jamming Detected!';
        jammingStatus.style.color = 'red';
        jammingStatus.style.fontWeight = 'bold';

        // Add the new jamming event to the table
        addJammingEventToTable(data);
    });

    // Listen for the 'reset_status' event from the server
    socket.on('reset_status', () => {
        // Update the UI to indicate status reset
        const jammingStatus = document.getElementById('jamming-alert');
        jammingStatus.innerText = 'OK';
        jammingStatus.style.color = 'black';
        jammingStatus.style.fontWeight = 'normal';
    });

    // Function to add a jamming event to the table
    function addJammingEventToTable(data) {
        const tableBody = document.getElementById('latestEventsTableBody');
        const newRow = tableBody.insertRow(0);
        newRow.insertCell(0).innerText = new Date(data.timestamp * 1000).toLocaleString();
        newRow.insertCell(1).innerText = data.current_strength;
        newRow.insertCell(2).innerText = data.moving_avg;
        newRow.insertCell(3).innerText = data.packet_loss_avg;
    }

    // Function to fetch latest jamming events from the server
    function fetchLatestJammingEvents() {
        fetch('/get_latest_jamming_events')
            .then(response => response.json())
            .then(data => {
                // Clear the table
                const tableBody = document.getElementById('latestEventsTableBody');
                tableBody.innerHTML = '';

                // Add each jamming event to the table
                data.forEach(event => {
                    addJammingEventToTable(event);
                });
            });
    }

    // Fetch latest jamming events every 5 seconds
    setInterval(fetchLatestJammingEvents, 5000);
};

