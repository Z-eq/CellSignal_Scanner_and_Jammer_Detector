from flask import render_template, request, redirect, url_for, jsonify
from datetime import datetime
from flask_socketio import emit
from models import WifiData, Watchlist, JammingEvent
from app import app, db, socketio
from flask import flash
# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Scanner route
@app.route('/scanner')
def scanner():
    saved_wifis = WifiData.query.all()
    watchlist = Watchlist.query.all()
    return render_template('scanner.html', saved_wifis=saved_wifis, watchlist=watchlist)

# Save Wi-Fi data route
@app.route('/save', methods=['POST'])
def save():
    try:
        data = request.form
        ssid = data['ssid']
        address = data['address']
        rssi = data['rssi']

        existing_wifi_data = WifiData.query.filter_by(ssid=ssid, address=address).first()
        if existing_wifi_data is None:
            wifi_data = WifiData(ssid=ssid, address=address, rssi=rssi)
            db.session.add(wifi_data)
        else:
            existing_wifi_data.rssi = rssi

        db.session.commit()
        flash("Wi-Fi data saved successfully!", "success")
        return jsonify(success=True)

    except Exception as e:
        db.session.rollback()
        flash(f"Error saving Wi-Fi data: {str(e)}", "danger")
        return jsonify(success=False, error=str(e))


# Delete Wi-Fi data route

@app.route('/delete_wifi_data', methods=['POST'])
def delete_wifi_data():
    try:
        wifi_ids = request.form.getlist('wifi_ids')
        WifiData.query.filter(WifiData.id.in_(wifi_ids)).delete(synchronize_session='fetch')
        db.session.commit()
        flash("Wi-Fi data deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting Wi-Fi data: {str(e)}", "danger")
    return redirect(url_for('scanner'))


# Add to Watchlist route
@app.route('/add_to_watchlist', methods=['GET', 'POST'])
def add_to_watchlist():
    if request.method == 'POST':
        ssid = request.form.get('ssid')
        address = request.form.get('address')
    else:
        ssid = request.args.get('ssid')
        address = request.args.get('address')

    if not ssid or not address:
        return "SSID or Address cannot be empty", 400

    existing_item = Watchlist.query.filter_by(ssid=ssid, address=address).first()
    if existing_item is None:
        item = Watchlist(ssid=ssid, address=address)
        db.session.add(item)
        db.session.commit()

    return redirect(url_for('scanner'))

# Remove from Watchlist route
@app.route('/remove_from_watchlist', methods=['POST'])
def remove_from_watchlist():
    watchlist_ids = request.form.getlist('watchlist_ids')
    if watchlist_ids:
        for watchlist_id in watchlist_ids:
            item = Watchlist.query.get(watchlist_id)
            if item:
                db.session.delete(item)
        db.session.commit()
    return redirect(url_for('scanner'))

# Update route
@app.route('/update')
def update():
    saved_wifis = WifiData.query.all()

    wifi_data_list = [
        {"ssid": wifi.ssid, "address": wifi.address, "rssi": wifi.rssi}
        for wifi in saved_wifis
    ]

    return jsonify(wifi_data_list)

# Delete selected Wi-Fi data route
@app.route('/delete_selected', methods=['POST'])
def delete_selected():
    ids = request.form.getlist('ids')
    for id in ids:
        wifi_data = WifiData.query.get(id)
        if wifi_data:
            db.session.delete(wifi_data)
            db.session.commit()
    return jsonify(success=True)

# Bluetooth scanner route
@app.route('/bluetooth-scanner')
def bluetooth_scanner():
    return render_template('bluetooth_scanner.html')

# Jammer route
@app.route('/jammer')
def jammer():
    jamming_events = JammingEvent.query.order_by(JammingEvent.timestamp.desc()).limit(10).all()
    return render_template('jammer.html', jamming_events=jamming_events)

# Jamming alert route
@app.route('/jamming_alert', methods=['POST'])
def jamming_alert():
    data = request.get_json()
    timestamp = datetime.fromtimestamp(int(data['timestamp']))  # Convert the timestamp to a datetime object
    current_strength = data['current_strength']
    moving_avg = data['moving_avg']
    packet_loss_avg = data.get('packet_loss_avg', None)  # Use get method to handle optional key

    jamming_event = JammingEvent(
        timestamp=timestamp,
        current_strength=current_strength,
        moving_avg=moving_avg,
        packet_loss_avg=packet_loss_avg
    )

    db.session.add(jamming_event)
    db.session.commit()

    # Emit jamming_detected event to all clients
    emit('jamming_detected', data, broadcast=True, namespace='')

    return {"message": "Jamming event saved successfully"}, 200

# Stop jamming route
@app.route('/stop_jamming')
def stop_jamming():
    # Emit reset_status event to all clients
    emit('reset_status', broadcast=True, namespace='')
    return jsonify(success=True)


# Get the latest signal data route
@app.route('/get_latest_signal_data')
def get_latest_signal_data():
    # Assuming the latest signal data is the last record in JammingEvent
    latest_signal_data = JammingEvent.query.order_by(JammingEvent.timestamp.desc()).first()
    if latest_signal_data:
        return jsonify({
            "current_strength": latest_signal_data.current_strength,
            "moving_avg": latest_signal_data.moving_avg
        })
    else:
        return jsonify({
            "current_strength": "N/A",
            "moving_avg": "N/A"
        })

# Get latest jamming events route
@app.route('/get_latest_jamming_events')
def get_latest_jamming_events():
    jamming_events = JammingEvent.query.order_by(JammingEvent.timestamp.desc()).limit(10).all()
    jamming_events_list = [
        {
            "timestamp": jamming.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "current_strength": jamming.current_strength,
            "moving_avg": jamming.moving_avg,
            "packet_loss_avg": jamming.packet_loss_avg
        }
        for jamming in jamming_events
    ]
    return jsonify(jamming_events_list)

# Get jamming status route
@app.route('/jamming_status')
def jamming_status():
    jamming_events = JammingEvent.query.order_by(JammingEvent.timestamp.desc()).limit(5).all()
    events_data = [
        {
            "timestamp": event.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "current_strength": event.current_strength,
            "moving_avg": event.moving_avg,
            "packet_loss_avg": event.packet_loss_avg
        }
        for event in jamming_events
    ]
    return jsonify(events_data)

# Continuous update route
@app.route('/continuous_update', methods=['POST'])
def continuous_update():
    data = request.get_json()
    current_strength = data['current_strength']
    moving_avg = data['moving_avg']

    # Emit continuous_update event to all clients
    emit('continuous_update', data, broadcast=True, namespace='')

    return {"message": "Continuous update received"}, 200
