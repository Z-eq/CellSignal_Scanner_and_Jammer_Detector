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

    const socket = io();

    // Connect to the server
    socket.connect();

    // Listen for the 'continuous_update' event from the server
    socket.on('continuous_update', data => {
        const currentStrengthDisplay = document.getElementById('currentStrength');
        const movingAvgDisplay = document.getElementById('movingAvg');

        currentStrengthDisplay.innerText = `Current Strength: ${data.current_strength} dBm`;
        movingAvgDisplay.innerText = `Moving Average: ${data.moving_avg} dBm`;
    });

    // Listen for the 'jamming_detected' event from the server
    socket.on('jamming_detected', data => {
        const jammingStatus = document.getElementById('jamming-alert');
        jammingStatus.innerText = 'Jamming Detected!';
        jammingStatus.style.color = 'red';
        jammingStatus.style.fontWeight = 'bold';

        addJammingEventToTable(data);
    });

    // Function to add a jamming event to the table
    function addJammingEventToTable(data) {
        const tableBody = document.getElementById('latestEventsTableBody');
        const newRow = tableBody.insertRow(0);
        newRow.insertCell(0).innerText = new Date(data.timestamp * 1000).toLocaleString();
        newRow.insertCell(1).innerText = data.current_strength;
        newRow.insertCell(2).innerText = data.moving_avg;
        newRow.insertCell(3).innerText = data.packet_loss_avg || 'N/A';

    }

    // Function to fetch the latest signal data from the server
    function fetchLatestSignalData() {
        fetch('/get_latest_signal_data')
            .then(response => response.json())
            .then(data => {
                const currentStrengthDisplay = document.getElementById('currentStrength');
                const movingAvgDisplay = document.getElementById('movingAvg');

                currentStrengthDisplay.innerText = `Current Strength: ${data.current_strength} dBm`;
                movingAvgDisplay.innerText = `Moving Average: ${data.moving_avg} dBm`;
            });
    }

    // Function to fetch latest jamming events from the server
    function fetchLatestJammingEvents() {
        fetch('/get_latest_jamming_events')
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('latestEventsTableBody');
                tableBody.innerHTML = '';
                data.forEach(event => {
                    addJammingEventToTable(event);
                });
            });
    }

    // Fetch the latest signal data and jamming events every 5 seconds
    setInterval(() => {
        fetchLatestSignalData();
        fetchLatestJammingEvents();
    }, 1000);
};
