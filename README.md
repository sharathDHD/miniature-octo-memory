# Fan Fiction Novel Generator

A Flask web application that generates new novels based on an existing fan fiction database using AI-inspired content generation.

## Features

### 🏠 Dashboard
- **Statistics Overview**: View total novels, chapters, and generated content
- **Recent Novels**: Quick access to recently updated novels
- **Responsive Design**: Modern, mobile-friendly interface

### 📚 Browse Novels
- **Paginated Browsing**: Navigate through 324+ novels with 20 per page
- **Status Indicators**: Visual badges for Completed, Processing, Failed, and Generated novels
- **Chapter Counts**: See how many chapters each novel contains
- **Search & Filter**: Easy navigation through large collections

### 📖 Novel Details
- **Complete Information**: Title, status, chapter count, creation/update dates
- **Chapter Listing**: Browse up to 50 chapters with character counts
- **Source Links**: Access to original content sources
- **Statistics**: Progress tracking and content metrics

### 📝 Chapter Viewer
- **Full Content Display**: Read complete chapter content with proper formatting
- **Navigation**: Easy movement between chapters and back to novel
- **Character/Word Counts**: Content length information
- **Source Attribution**: Links to original content when available

### ✨ Novel Generation
- **AI-Inspired Generation**: Create new content based on existing novels
- **Flexible Prompts**: Describe your desired novel type, genre, and themes
- **Inspiration Sources**: 
  - Random selection from database
  - Specific novel-based inspiration
- **Instant Results**: Generated novels are immediately saved and viewable

## Database Schema

The application works with a SQLite database containing:

### Novels Table
```sql
CREATE TABLE novels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT UNIQUE,
    status TEXT DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    total_chapters INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP
);
```

### Chapters Table
```sql
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    novel_id INTEGER,
    url TEXT UNIQUE,
    title TEXT,
    content TEXT,
    status TEXT DEFAULT 'pending',
    scraped_at TIMESTAMP,
    FOREIGN KEY(novel_id) REFERENCES novels(id)
);
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- SQLite3
- Flask and dependencies

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure Database Exists**
   - Place your `novel_data.db` file in the project root
   - The database should contain novels and chapters as per the schema above

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Application**
   - Open your browser to `http://localhost:12000`
   - Or use the provided runtime URLs for hosted environments

## Usage Guide

### Generating a New Novel

1. **Navigate to Generate**: Click "Generate Novel" in the navigation
2. **Enter a Prompt**: Describe your desired novel:
   - "A magical academy story with romance and adventure elements"
   - "A time-traveling mystery thriller with supernatural elements"
   - "An epic fantasy adventure with dragons and ancient magic"
3. **Choose Inspiration**: 
   - Random selection for diverse inspiration
   - Specific novel for targeted style mimicking
4. **Generate**: Click "Generate Novel" and wait for processing
5. **View Results**: Automatically redirected to your new novel

### Browsing Existing Content

1. **Browse Novels**: Use the "Browse Novels" page to explore the collection
2. **View Details**: Click "View Details" on any novel to see chapters
3. **Read Chapters**: Click on individual chapters to read full content
4. **Navigate**: Use pagination to explore all 324+ novels

## Technical Details

### Content Generation Algorithm

The application uses a pattern-based approach to generate new content:

1. **Analysis Phase**: 
   - Extracts vocabulary and common words from inspiration chapters
   - Identifies sentence patterns and structures
   - Analyzes thematic elements

2. **Generation Phase**:
   - Creates introductory content based on prompt keywords
   - Incorporates modified sentences from source material
   - Weaves in thematic vocabulary and concepts
   - Ensures appropriate length and structure

3. **Storage Phase**:
   - Saves generated novel to database
   - Creates first chapter with generated content
   - Marks content as "generated" for identification

### API Endpoints

- `GET /` - Dashboard/home page
- `GET /browse` - Browse novels with pagination
- `GET /novel/<id>` - View specific novel details
- `GET /chapter/<id>` - View specific chapter content
- `GET /generate` - Novel generation form
- `POST /generate` - Process novel generation
- `GET /api/stats` - JSON statistics endpoint

## Current Database Stats

- **324 Novels** in the database
- **89,979 Chapters** with content
- **Multiple Genres** including fantasy, romance, adventure, mystery
- **Rich Content** with substantial chapter lengths (5,000-7,000+ characters each)

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, Custom CSS/JavaScript
- **Database**: SQLite3
- **Icons**: Font Awesome
- **Styling**: Modern responsive design with animations

## Future Enhancements

Potential improvements for the application:

1. **Advanced AI Integration**: OpenAI GPT or similar for higher quality generation
2. **User Accounts**: Personal libraries and generation history
3. **Export Features**: Download generated novels in various formats
4. **Advanced Search**: Full-text search across novels and chapters
5. **Collaborative Features**: Sharing and rating generated content
6. **Genre Classification**: Automatic tagging and categorization
7. **Batch Generation**: Generate multiple chapters or complete novels

## Contributing

This application provides a solid foundation for fan fiction content generation and management. The modular design makes it easy to extend with additional features or integrate with more sophisticated AI services.

## License

This project is provided as-is for educational and personal use. Please respect the original sources of the fan fiction content in your database.