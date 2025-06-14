from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import random
import re
from datetime import datetime
import os
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

# Add built-in functions to Jinja2 environment
app.jinja_env.globals.update(min=min, max=max)

# Database configuration
DATABASE = 'novel_data.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_random_chapters(limit=10):
    """Get random chapters for inspiration"""
    conn = get_db_connection()
    chapters = conn.execute('''
        SELECT c.title, c.content, n.title as novel_title
        FROM chapters c
        JOIN novels n ON c.novel_id = n.id
        WHERE c.content IS NOT NULL AND LENGTH(c.content) > 1000
        ORDER BY RANDOM()
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return chapters

def get_chapter_by_novel(novel_id, limit=5):
    """Get chapters from a specific novel"""
    conn = get_db_connection()
    chapters = conn.execute('''
        SELECT title, content
        FROM chapters
        WHERE novel_id = ? AND content IS NOT NULL
        ORDER BY id
        LIMIT ?
    ''', (novel_id, limit)).fetchall()
    conn.close()
    return chapters

def generate_novel_content(prompt, inspiration_chapters, max_length=2000):
    """Generate novel content based on prompt and inspiration chapters"""
    # This is a simple text generation based on patterns from existing content
    # In a real application, you might want to integrate with OpenAI API or similar
    
    # Extract common patterns and vocabulary from inspiration chapters
    all_text = " ".join([chapter['content'] for chapter in inspiration_chapters if chapter['content']])
    
    # Simple word frequency analysis
    words = re.findall(r'\b\w+\b', all_text.lower())
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get common words (excluding very common ones)
    common_words = [word for word, freq in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:100]
                   if word not in ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should']]
    
    # Extract sentences for inspiration
    sentences = re.split(r'[.!?]+', all_text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20 and len(s.strip()) < 200]
    
    # Generate content based on prompt and inspiration
    generated_content = f"# Generated Novel: {prompt}\n\n"
    
    # Add some introductory content
    if 'adventure' in prompt.lower():
        generated_content += "The journey began on a day that seemed ordinary, but would prove to be anything but. "
    elif 'romance' in prompt.lower():
        generated_content += "Their eyes met across the crowded room, and in that moment, everything changed. "
    elif 'mystery' in prompt.lower():
        generated_content += "The first clue appeared where no one expected it, hidden in plain sight. "
    else:
        generated_content += "It was a story that needed to be told, one that would change everything. "
    
    # Add some content inspired by the database
    if sentences:
        # Select a few random sentences and modify them slightly
        selected_sentences = random.sample(sentences, min(3, len(sentences)))
        for sentence in selected_sentences:
            # Simple modification - you could make this more sophisticated
            modified_sentence = sentence.replace("I", "they").replace("my", "their").replace("me", "them")
            generated_content += modified_sentence + ". "
    
    # Add some thematic content based on common words
    if common_words:
        thematic_words = random.sample(common_words[:20], min(5, len(common_words[:20])))
        generated_content += f"\n\nThe story would involve elements of {', '.join(thematic_words[:3])}, "
        generated_content += f"with themes exploring {', '.join(thematic_words[3:])}. "
    
    # Truncate if too long
    if len(generated_content) > max_length:
        generated_content = generated_content[:max_length] + "..."
    
    return generated_content

@app.route('/')
def index():
    """Main page"""
    conn = get_db_connection()
    
    # Get some statistics
    novel_count = conn.execute('SELECT COUNT(*) FROM novels').fetchone()[0]
    chapter_count = conn.execute('SELECT COUNT(*) FROM chapters WHERE content IS NOT NULL').fetchone()[0]
    
    # Get recent novels
    recent_novels = conn.execute('''
        SELECT id, title, total_chapters, status
        FROM novels
        ORDER BY last_updated DESC
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         novel_count=novel_count,
                         chapter_count=chapter_count,
                         recent_novels=recent_novels)

@app.route('/browse')
def browse():
    """Browse existing novels"""
    conn = get_db_connection()
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    novels = conn.execute('''
        SELECT id, title, total_chapters, status, last_updated
        FROM novels
        ORDER BY last_updated DESC
        LIMIT ? OFFSET ?
    ''', (per_page, offset)).fetchall()
    
    total_novels = conn.execute('SELECT COUNT(*) FROM novels').fetchone()[0]
    total_pages = (total_novels + per_page - 1) // per_page
    
    conn.close()
    
    return render_template('browse.html', 
                         novels=novels,
                         page=page,
                         total_pages=total_pages,
                         has_prev=page > 1,
                         has_next=page < total_pages)

@app.route('/novel/<int:novel_id>')
def view_novel(novel_id):
    """View a specific novel and its chapters"""
    conn = get_db_connection()
    
    novel = conn.execute('SELECT * FROM novels WHERE id = ?', (novel_id,)).fetchone()
    if not novel:
        flash('Novel not found')
        return redirect(url_for('browse'))
    
    chapters = conn.execute('''
        SELECT id, title, LENGTH(content) as content_length, scraped_at
        FROM chapters
        WHERE novel_id = ? AND content IS NOT NULL
        ORDER BY id
        LIMIT 50
    ''', (novel_id,)).fetchall()
    
    conn.close()
    
    return render_template('novel.html', novel=novel, chapters=chapters)

@app.route('/chapter/<int:chapter_id>')
def view_chapter(chapter_id):
    """View a specific chapter"""
    conn = get_db_connection()
    
    chapter = conn.execute('''
        SELECT c.*, n.title as novel_title
        FROM chapters c
        JOIN novels n ON c.novel_id = n.id
        WHERE c.id = ?
    ''', (chapter_id,)).fetchone()
    
    if not chapter:
        flash('Chapter not found')
        return redirect(url_for('browse'))
    
    conn.close()
    
    return render_template('chapter.html', chapter=chapter)

@app.route('/generate')
def generate_form():
    """Show the novel generation form"""
    conn = get_db_connection()
    
    # Get some sample novels for inspiration selection
    sample_novels = conn.execute('''
        SELECT id, title, total_chapters
        FROM novels
        WHERE total_chapters > 10
        ORDER BY RANDOM()
        LIMIT 20
    ''').fetchall()
    
    conn.close()
    
    return render_template('generate.html', sample_novels=sample_novels)

@app.route('/generate', methods=['POST'])
def generate_novel():
    """Generate a new novel based on user input"""
    prompt = request.form.get('prompt', '').strip()
    inspiration_source = request.form.get('inspiration_source', 'random')
    novel_id = request.form.get('novel_id', type=int)
    
    if not prompt:
        flash('Please provide a prompt for the novel generation')
        return redirect(url_for('generate_form'))
    
    # Get inspiration chapters
    if inspiration_source == 'specific' and novel_id:
        inspiration_chapters = get_chapter_by_novel(novel_id, 5)
    else:
        inspiration_chapters = get_random_chapters(10)
    
    if not inspiration_chapters:
        flash('No inspiration content found. Please try again.')
        return redirect(url_for('generate_form'))
    
    # Generate the novel content
    generated_content = generate_novel_content(prompt, inspiration_chapters)
    
    # Save to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create a new novel entry
    cursor.execute('''
        INSERT INTO novels (title, url, status, total_chapters, created_at, last_updated)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (f"Generated: {prompt[:50]}", f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}", 
          'generated', 1, datetime.now(), datetime.now()))
    
    new_novel_id = cursor.lastrowid
    
    # Create the first chapter
    cursor.execute('''
        INSERT INTO chapters (novel_id, url, title, content, status, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (new_novel_id, f"generated_chapter_1_{new_novel_id}", "Chapter 1", 
          generated_content, 'generated', datetime.now()))
    
    conn.commit()
    conn.close()
    
    flash('Novel generated successfully!')
    return redirect(url_for('view_novel', novel_id=new_novel_id))

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    conn = get_db_connection()
    
    stats = {
        'novels': conn.execute('SELECT COUNT(*) FROM novels').fetchone()[0],
        'chapters': conn.execute('SELECT COUNT(*) FROM chapters WHERE content IS NOT NULL').fetchone()[0],
        'total_words': conn.execute('SELECT SUM(LENGTH(content) - LENGTH(REPLACE(content, " ", "")) + 1) FROM chapters WHERE content IS NOT NULL').fetchone()[0] or 0
    }
    
    conn.close()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12000, debug=True)