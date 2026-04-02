from flask import Flask, jsonify, request

app = Flask(__name__)

class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }

events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


def get_event(event_id):
    return next((event for event in events if event.id == event_id), None)


# Created a new event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"message": "Please provide a title for the event"}), 400

    new_id = events[-1].id + 1 if events else 1
    new_event = Event(new_id, data["title"])

    events.append(new_event)

    return jsonify({
        "message": "Event created successfully",
        "event": new_event.to_dict()
    }), 201


# Updated the existing event
@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    event = get_event(event_id)

    if not event:
        return jsonify({"message": "Event not found"}), 404

    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"message": "New title is required"}), 400

    event.title = data["title"]

    return jsonify({
        "message": "Event updated",
        "event": event.to_dict()
    })


# Deleted an event
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = get_event(event_id)

    if not event:
        return jsonify({"message": "Event not found"}), 404

    events.remove(event)

    return jsonify({
        "message": f"Event {event_id} deleted"
    })


@app.route('/events', methods=['GET'])
def list_events():
    return jsonify([event.to_dict() for event in events])


if __name__ == "__main__":
    app.run(debug=True)