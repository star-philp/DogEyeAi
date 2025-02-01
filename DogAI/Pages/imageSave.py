def save_to_db(image, result):
    conn = sqlite3.connect('dog_health.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO results (image, analysis_result) VALUES (?, ?)', (image, result))
    conn.commit()