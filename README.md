# Geo News Scraper

A Dockerized web application that scrapes news articles from Geo.tv, stores them in MongoDB, and provides summarization functionality.

## Features

- **Web Scraping**: Extracts article titles, dates, descriptions, and images
- **Summarization**: Uses Sumy's LexRank algorithm to generate summaries
- **Dockerized**: Ready for deployment with MongoDB integration
- **Persistent Storage**: Images and database survive container restarts

## Technologies Used

- Python 3.9
- Flask
- MongoDB
- Sumy (NLTK, NumPy)
- BeautifulSoup4
- Docker

## Installation

### Prerequisites
- Docker
- Docker Compose

### Setup
```bash
git clone https://github.com/your-username/Geo-News-Scraper.git
cd Geo-News-Scraper
docker-compose up --build -d
