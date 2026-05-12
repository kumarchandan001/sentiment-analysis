from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import sqlite3 
from datetime import datetime 
import io
import csv
from flask import Response

app = Flask(__name__)

model = joblib.load('sentiment_model.joblib')

# --- Main Analyzer Route ---
@app.route('/')
def home():
    return render_template('index.html')

# --- Prediction API Route ---
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    review_text = data['review_text']
    
    probabilities = model.predict_proba([review_text])[0]
    prediction = np.argmax(probabilities)
    confidence = probabilities[prediction] * 100
    sentiment = 'Positive' if prediction == 1 else 'Negative'
    
# NEW: Save the prediction to the database
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (review_text, sentiment, confidence) VALUES (?, ?, ?)",
            (review_text, sentiment, round(confidence, 2))
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}") 

    return jsonify({
        'prediction': sentiment,
        'confidence': round(confidence, 2)
    })

# NEW: Create a new route to display the history page
@app.route('/history')
def history():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    # Fetch all reviews, ordered by the newest first
    cursor.execute("SELECT * FROM reviews ORDER BY timestamp DESC")
    reviews = cursor.fetchall()
    conn.close()
    # Pass the fetched reviews to the new history.html template
    return render_template('history.html', reviews=reviews)

# NEW: Create a new route to provide data for the chart
@app.route('/stats')
def stats():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Query to count the occurrences of each sentiment
    cursor.execute("SELECT sentiment, COUNT(*) FROM reviews GROUP BY sentiment")
    data = cursor.fetchall()
    conn.close()

    # Process the data into a simple dictionary for our chart
    stats_dict = {row[0]: row[1] for row in data}

    return jsonify(stats_dict)
# NEW: Route to delete a specific review
@app.route('/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()
    # Return a success response
    return jsonify({'status': 'success'})
@app.route('/export')
def export_csv():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, review_text, sentiment, confidence FROM reviews ORDER BY timestamp DESC")
    data = cursor.fetchall()
    conn.close()

    # Use an in-memory text stream to build the CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Write the header row
    writer.writerow(['Timestamp', 'Review', 'Sentiment', 'Confidence'])
    # Write the data rows
    writer.writerows(data)

    output.seek(0)

    # Return the CSV data as a file download
    return Response(output,
                   mimetype="text/csv",
                   headers={"Content-Disposition":"attachment;filename=sentiment_history.csv"})

if __name__ == '__main__':
    app.run(debug=True)