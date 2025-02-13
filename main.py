# Non-personal imports
from flask import Flask, json, jsonify,  render_template, abort, redirect, url_for, request, flash
from datetime import date
from flask_wtf.csrf import CSRFProtect
from markupsafe import escape

# Personal imports
from units.db_populate import populate_emotioncolour,check_database_existence
from units.forms import UserEmotionDescription
from units.DAO import EmotionColourDAO,RecordDAO
from units.db_init import init_db
from units.NLP import NLP


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

app.config['SECRET_KEY'] = 'your_secret_key_here'


# Enable CSRF protection
csrf = CSRFProtect(app)

NLP.setup()

COLOUR_COLUMNS = [
    ['black', "#000000"],
    ['red', "#FF0000"],
    ['gray', "#808080"],
    ['yellow', "#FFFF00"],
    ['light_purple', "#D8BFD8"],
    ['sky_blue', "#87CEEB"],
    ['jade', "#00A86B"],
    ['green', "#008000"],
    ['aqua', "#00FFFF"],
    ['indigo', "#4B0082"],
    ['blue', "#0000FF"],
    ['bright_pink', "#FF007F"],
    ['chocolate', "#D2691E"],
    ['dark_yellow', "#FFD700"],
    ['light_green', "#90EE90"]
]

# General routes ---------------------------------------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
# Emotion Regulator main functionality related routes --------------------------------------------------------------------

@app.route("/emotion_description",methods=["GET","POST"])
def emotion_description():
    form = UserEmotionDescription()
    if form.validate_on_submit():
        description = form.description.data
        return redirect(url_for("display_colour",emotion_name=description))
    return render_template("emotion_description.html",form=form)

@app.route("/display_colour/<emotion_name>")
def display_colour(emotion_name):
    
    emotion_name = NLP.operate(escape(emotion_name)).capitalize()
    print(emotion_name)
    emotions = [emotion.emotion_name for emotion in EmotionColourDAO.get_all_emotions()]
    
    if emotion_name not in emotions:
        abort(404)
    
    result = EmotionColourDAO.get_emotion_colours(emotion_name,
                                                  available_colours=[c[0] for c in COLOUR_COLUMNS])
    if not result:
        abort(500)
    
    organised_colours = organise_colours(add_colour_hex_pairs(result))
    print(organised_colours)
    # return render_template("display_colour.html")
    return render_template("display_colour.html",colour_list=organised_colours,emotion_name=emotion_name)


@app.route('/process_results', methods=['POST'])
def process_results():
    print("reached")
    data = request.get_json()  # Safely get JSON data from the POST request
    if not data or 'results' not in data:
        return jsonify({'message': 'Bad request, results not found'}), 400

    results = data.get('results')  # Extract the list of results (0s and 1s)
    colours = data.get('colours')
    emotion_name = data.get('emotion_name')
    # Debugging: Print the results received on the server
    # print("Received results:", results)
    # print("Colours:",colours)
    # print("Emotion name:",emotion_name)
    
    shortened_colour_list = calculate_updated_colour_list(results,colours)
    paired_colour_rating_list = pair_colour_and_rating(results,shortened_colour_list)
    manage_record(paired_colour_rating_list,emotion_name)
    # Respond with a success message
    return jsonify({'message': 'Results processed successfully!'}), 200


# Helper functions ---------------------------------------------------------------------------------------------------


def manage_record(n_list, emotion_name):
    # Fetch the emotion record using the DAO
    record = EmotionColourDAO.get_emotion_record_by_emotion(emotion_name)

    if not record:
        print(f"No record found for emotion: {emotion_name}")
        return

    # Fetch the current sample size
    sample_size = record.sample_size

    # Loop through the n_list and update each column
    updates = {}
    for n in n_list:
        colour = n[0]
        choice = n[1]

        # Dynamically get the current value of the colour
        value = getattr(record, colour, None)
        if value is None:
            print(f"Invalid column: {colour}")
            continue

        # Calculate the new value
        new_value = calculate_updated_value(value, choice, sample_size)
        
        colour_match = False
        if choice == 1:
            colour_match = True
        
        RecordDAO.create_record(
            emotion_name=emotion_name,
            likelihood_score=value,
            colour_displayed=colour,
            record_date=date.today(),
            colour_match=colour_match
        )
        # Store the updated value in a dictionary for batch updating
        updates[colour] = new_value

    # Increment the sample size
    updates["sample_size"] = sample_size + 1

    # Use the DAO to apply the updates to the database
    EmotionColourDAO.update_emotion(record.emotion_id, **updates)
    print(f"Successfully updated record for {emotion_name}")


def calculate_updated_value(value,choice,sample_size):
    new_value = 0
    contribution = calculate_contribution(value,sample_size)
    if choice == 0:
        new_value = decrement_value(value,contribution)
        if value < 0:
            new_value = 0
    elif choice == 1:
        new_value = increment_value(value,contribution)
        if value > 10:
            new_value = 10
    
    return new_value
        

def calculate_contribution(current_value,sample_size):
    return current_value/sample_size

def increment_value(current_value,contribution):
    return current_value + contribution
    
def decrement_value(current_value,contribution):
    return current_value - contribution
    

def pair_colour_and_rating(results,colour_list):
    colour_rating_list = []
    for i in range(len(results)):
        c = colour_list[i][0]
        r = results[i]
        colour_rating_list.append([c,r])
    return colour_rating_list

def calculate_updated_colour_list(results,colours):
    new_list = colours[:len(results)]
    return new_list


def add_colour_hex_pairs(colour_dict):
    colour_list_to_dict = {colour[0]: colour[1] for colour in COLOUR_COLUMNS}
    temp_dict = {}
    for key in colour_dict:
        temp_dict[key] = [colour_dict[key],colour_list_to_dict[key]]
    
    return temp_dict
        
        
def organise_colours(colour_dict):
    sorted_list = sorted(colour_dict.items(),key=lambda x:x[1],reverse=True)
    
    return sorted_list

# Record related routes --------------------------------------------------------------------------------------------------

@app.route("/records", methods=["GET"])
def get_records():
    records = RecordDAO.get_all_records()
    if not records:
        return "No records available"
    return jsonify([{
        "record_id": record.record_id,
        "emotion_name": record.emotion_name,
        "likelihood_score": record.likelihood_score,
        "colour_displayed": record.colour_displayed,
        "record_date": record.record_date,
        "colour_match": record.colour_match
    } for record in records])

@app.route("/records/<int:record_id>", methods=["GET"])
def get_record_by_id(record_id):
    record = RecordDAO.find_record_by_id(record_id)
    if record:
        return jsonify({
            "record_id": record.record_id,
            "emotion_name": record.emotion_name,
            "likelihood_score": record.likelihood_score,
            "colour_displayed": record.colour_displayed,
            "record_date": record.record_date,
            "colour_match": record.colour_match
        })
    return jsonify({"error": "Record not found"}), 404

@app.route("/records", methods=["POST"])
def create_record():
    data = request.json
    new_record = RecordDAO.add_record(
        emotion_name=data.get("emotion_name"),
        likelihood_score=data.get("likelihood_score"),
        colour_displayed=data.get("colour_displayed"),
        record_date=date.fromisoformat(data.get("record_date")),
        colour_match=data.get("colour_match")
    )
    return jsonify({
        "record_id": new_record.record_id,
        "emotion_name": new_record.emotion_name,
        "likelihood_score": new_record.likelihood_score,
        "colour_displayed": new_record.colour_displayed,
        "record_date": new_record.record_date,
        "colour_match": new_record.colour_match
    }), 201

@app.route("/records/<int:record_id>", methods=["PUT"])
def update_record(record_id):
    data = request.json
    updated_record = RecordDAO.update_record(
        record_id,
        emotion_name=data.get("emotion_name"),
        likelihood_score=data.get("likelihood_score"),
        colour_displayed=data.get("colour_displayed"),
        record_date=date.fromisoformat(data.get("record_date")),
        colour_match=data.get("colour_match")
    )
    if updated_record:
        return jsonify({
            "record_id": updated_record.record_id,
            "emotion_name": updated_record.emotion_name,
            "likelihood_score": updated_record.likelihood_score,
            "colour_displayed": updated_record.colour_displayed,
            "record_date": updated_record.record_date,
            "colour_match": updated_record.colour_match
        })
    return jsonify({"error": "Record not found"}), 404

@app.route("/records/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    if RecordDAO.delete_record(record_id):
        return jsonify({"message": "Record deleted successfully"})
    return jsonify({"error": "Record not found"}), 404

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Form validation (you can customize this further)
        if not name or not email or not message:
            flash("Please fill out all fields.", "error")
        else:
            # Handle form submission (e.g., send email or store in database)
            flash("Thank you for contacting us!", "success")
            return redirect('/contact')  # Redirect to prevent form re-submission

    return render_template('contact.html')

# Running the app -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    with app.app_context():

        if not check_database_existence(filepath="instance/project.db"):
            init_db(app=app)
            populate_emotioncolour()
        else:
            init_db(app=app)
        
        app.run(debug=True)
