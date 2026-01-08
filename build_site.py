#!/usr/bin/env python3
"""
YMCA Matara Website Build Script (v2.0)
=======================================
This script automatically generates the news section of the YMCA Matara website.

Usage:
    python build_site.py

What it does:
1. Scans the 'news/' directory for programme folders
2. Reads info.json (title, date, description) and article.md from each folder
3. Generates 'news.html' with filterable programme cards (by year/month)
4. Generates 'index.html' inside each programme folder with Markdown content and media gallery

Requirements:
    pip install markdown
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# Try to import markdown, provide helpful error if not installed
try:
    import markdown
except ImportError:
    print("=" * 50)
    print("[ERROR] 'markdown' library not found!")
    print()
    print("Please install it by running:")
    print("    pip install markdown")
    print("=" * 50)
    exit(1)

# Configuration
SCRIPT_DIR = Path(__file__).parent
NEWS_DIR = SCRIPT_DIR / "news"
NEWS_HTML = SCRIPT_DIR / "news.html"

# Supported media extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov', '.avi', '.mkv'}

# Month names for display
MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]


def get_common_styles() -> str:
    """Return the common CSS styles used across all pages"""
    return '''
        :root {
            --ymca-blue: #004a99;
            --ymca-blue-dark: #003570;
            --ymca-red: #cc0000;
            --ymca-red-dark: #a30000;
            --white: #ffffff;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-600: #4b5563;
            --gray-700: #374151;
            --gray-800: #1f2937;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--gray-700);
            background: var(--gray-50);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Navigation */
        .navbar {
            background: linear-gradient(135deg, var(--ymca-blue) 0%, var(--ymca-blue-dark) 100%);
            padding: 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: var(--shadow-lg);
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 1.5rem;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 1rem 0;
            text-decoration: none;
            color: var(--white);
        }

        .logo-icon {
            width: 45px;
            height: 45px;
            background: var(--white);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 4px;
            box-shadow: var(--shadow-md);
            object-fit: contain;
        }

        .logo-text {
            font-weight: 700;
            font-size: 1.25rem;
            letter-spacing: -0.025em;
        }

        .logo-text span {
            display: block;
            font-size: 0.75rem;
            font-weight: 500;
            opacity: 0.9;
            letter-spacing: 0.05em;
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 0.25rem;
        }

        .nav-links a {
            display: block;
            padding: 0.75rem 1.5rem;
            color: var(--white);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            border-radius: 8px;
            transition: all 0.2s ease;
            position: relative;
        }

        .nav-links a:hover {
            background: rgba(255,255,255,0.15);
        }

        .nav-links a.active {
            background: rgba(255,255,255,0.2);
        }

        .nav-links a.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 30px;
            height: 3px;
            background: var(--ymca-red);
            border-radius: 3px 3px 0 0;
        }

        /* Page Header */
        .page-header {
            background: linear-gradient(135deg, var(--ymca-blue) 0%, var(--ymca-blue-dark) 50%, #002244 100%);
            color: var(--white);
            padding: 3rem 1.5rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .page-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 1;
        }

        .page-header-content {
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        .page-header h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 800;
            margin-bottom: 0.75rem;
            letter-spacing: -0.025em;
        }

        .page-header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* Main Content */
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 1.5rem;
            flex: 1;
            width: 100%;
        }

        /* Filter Section */
        .filter-section {
            background: var(--white);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--gray-100);
        }

        .filter-row {
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .filter-label {
            font-weight: 600;
            color: var(--gray-700);
            font-size: 0.95rem;
        }

        .filter-select {
            padding: 0.75rem 2.5rem 0.75rem 1rem;
            font-size: 1rem;
            border: 2px solid var(--gray-200);
            border-radius: 10px;
            background: var(--white);
            color: var(--gray-700);
            cursor: pointer;
            min-width: 160px;
            min-height: 48px;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23374151' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 1rem center;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .filter-select:hover {
            border-color: var(--ymca-blue);
        }

        .filter-select:focus {
            outline: none;
            border-color: var(--ymca-blue);
            box-shadow: 0 0 0 3px rgba(0, 74, 153, 0.15);
        }

        /* News List Styles */
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        .news-card {
            background: var(--white);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: all 0.3s ease;
            border: 1px solid var(--gray-100);
            text-decoration: none;
            color: inherit;
            display: block;
        }

        .news-card.hidden {
            display: none;
        }

        .news-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-xl);
        }

        .news-card-header {
            background: linear-gradient(135deg, var(--ymca-blue), var(--ymca-blue-dark));
            padding: 1.5rem 2rem;
            color: var(--white);
        }

        .news-card-header h3 {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            line-height: 1.3;
        }

        .news-card-date {
            font-size: 0.85rem;
            opacity: 0.85;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .news-card-body {
            padding: 1.5rem 2rem;
        }

        .news-card-body p {
            color: var(--gray-600);
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .news-card-footer {
            padding: 0 2rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--ymca-blue);
            font-weight: 500;
            font-size: 0.9rem;
        }

        /* Thumbnail Card Styles */
        .news-card {
            position: relative;
            overflow: hidden;
            background: var(--white);
        }

        .card-bg-thumb {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: 0;
            transition: transform 0.5s ease;
        }

        .card-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.85));
            z-index: 1;
        }

        .news-card:hover .card-bg-thumb {
            transform: scale(1.05);
        }

        .news-card.has-thumbnail .news-card-header {
            background: linear-gradient(135deg, rgba(0, 74, 153, 0.75), rgba(0, 53, 112, 0.75));
            position: relative;
            z-index: 2;
            text-shadow: none;
        }

        .news-card.has-thumbnail .news-card-body {
            position: relative;
            z-index: 2;
        }

        .news-card.has-thumbnail .news-card-body p {
            color: var(--white);
            text-shadow: 0 1px 3px rgba(0,0,0,0.8);
            font-weight: 500;
        }

        .news-card.has-thumbnail .news-card-footer {
            position: relative;
            z-index: 2;
            background: transparent;
            padding: 0 2rem 2rem;
        }

        .news-card.has-thumbnail .footer-btn {
            background: rgba(255, 255, 255, 0.4);
            color: var(--ymca-blue);
            padding: 0.6rem 1.2rem;
            border-radius: 50px;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 700;
            font-size: 0.85rem;
            backdrop-filter: blur(8px);
            transition: all 0.2s ease;
        }

        .news-card.has-thumbnail .news-card-date {
            opacity: 0.9;
            color: rgba(255, 255, 255, 0.9);
        }

        /* No Results State */
        .no-results {
            text-align: center;
            padding: 4rem 2rem;
            background: var(--white);
            border-radius: 20px;
            box-shadow: var(--shadow-md);
            display: none;
        }

        .no-results.visible {
            display: block;
        }

        .no-results-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }

        .no-results h3 {
            font-size: 1.25rem;
            color: var(--gray-800);
            margin-bottom: 0.5rem;
        }

        .no-results p {
            color: var(--gray-600);
        }

        /* Programme Page Styles */
        .programme-content {
            background: var(--white);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--gray-100);
            margin-bottom: 2rem;
        }

        .programme-meta {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--gray-600);
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--gray-200);
        }

        /* Markdown Content Styles */
        .article-content {
            line-height: 1.8;
            color: var(--gray-700);
            font-size: 1.05rem;
        }

        .article-content h1 {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--gray-800);
            margin: 2rem 0 1rem;
            line-height: 1.3;
        }

        .article-content h2 {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--gray-800);
            margin: 1.75rem 0 0.75rem;
            line-height: 1.3;
        }

        .article-content h3 {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--gray-800);
            margin: 1.5rem 0 0.5rem;
        }

        .article-content p {
            margin-bottom: 1rem;
        }

        .article-content ul, .article-content ol {
            margin: 1rem 0 1.5rem 1.5rem;
        }

        .article-content li {
            margin-bottom: 0.5rem;
        }

        .article-content strong {
            font-weight: 600;
            color: var(--gray-800);
        }

        .article-content em {
            font-style: italic;
        }

        .article-content blockquote {
            border-left: 4px solid var(--ymca-blue);
            padding-left: 1rem;
            margin: 1.5rem 0;
            color: var(--gray-600);
            font-style: italic;
        }

        .article-content code {
            background: var(--gray-100);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-size: 0.9em;
        }

        .article-content hr {
            border: none;
            border-top: 1px solid var(--gray-200);
            margin: 2rem 0;
        }

        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--ymca-blue);
            text-decoration: none;
            font-weight: 500;
            margin-bottom: 1.5rem;
            transition: color 0.2s;
        }

        .back-link:hover {
            color: var(--ymca-blue-dark);
        }

        /* Media Gallery */
        .gallery-section {
            margin-top: 2.5rem;
            padding-top: 2rem;
            border-top: 1px solid var(--gray-200);
        }

        .gallery-section h2 {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--gray-800);
            margin-bottom: 1.5rem;
        }

        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }

        .gallery-item {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: transform 0.3s ease;
            cursor: pointer;
            aspect-ratio: 1 / 1;
        }

        .gallery-item:hover {
            transform: scale(1.03);
        }

        .gallery-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .gallery-item video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            background: #000;
        }

        /* Modal/Lightbox Overlay */
        .viewer-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 9999;
            display: none;
            justify-content: center;
            align-items: center;
            touch-action: pinch-zoom;
        }

        .viewer-overlay.active {
            display: flex;
        }

        .viewer-content {
            max-width: 95vw;
            max-height: 95vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .viewer-content img {
            max-width: 95vw;
            max-height: 95vh;
            object-fit: contain;
            border-radius: 4px;
        }

        .viewer-content video {
            max-width: 95vw;
            max-height: 95vh;
            object-fit: contain;
            border-radius: 4px;
            background: #000;
        }

        .viewer-close {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.15);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            font-size: 28px;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: background 0.2s, transform 0.2s;
            z-index: 10000;
        }

        .viewer-close:hover {
            background: rgba(255, 255, 255, 0.25);
            transform: scale(1.1);
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            background: var(--white);
            border-radius: 20px;
            box-shadow: var(--shadow-md);
        }

        .empty-state-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }

        .empty-state h3 {
            font-size: 1.5rem;
            color: var(--gray-800);
            margin-bottom: 0.5rem;
        }

        .empty-state p {
            color: var(--gray-600);
        }

        /* Footer */
        .footer {
            background: var(--gray-800);
            color: var(--white);
            padding: 2rem 1.5rem;
            text-align: center;
            margin-top: auto;
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
        }

        .footer-text {
            opacity: 0.7;
            font-size: 0.85rem;
        }

        /* Mobile Menu Toggle */
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--white);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
        }

        @media (max-width: 768px) {
            .mobile-menu-btn {
                display: block;
            }

            .nav-links {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: var(--ymca-blue-dark);
                flex-direction: column;
                padding: 1rem;
                gap: 0.5rem;
            }

            .nav-links.active {
                display: flex;
            }

            .nav-links a {
                padding: 1rem;
                text-align: center;
            }

            .main-content {
                padding: 2rem 1rem;
            }

            .filter-row {
                flex-direction: column;
                align-items: stretch;
            }

            .filter-select {
                width: 100%;
            }

            .programme-content {
                padding: 1.5rem;
            }

            .gallery-grid {
                grid-template-columns: 1fr;
            }

            .news-grid {
                grid-template-columns: 1fr;
            }
        }
    '''


def format_date_display(date_str: str) -> str:
    """Format date string for display (e.g., '2024-12-15' -> 'December 15, 2024')"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str


def generate_news_html(programmes: list, years: list) -> str:
    """Generate the main news.html page listing all programmes with filters"""
    
    # Generate year options
    year_options = '<option value="all">All Years</option>\n'
    for year in years:
        year_options += f'                        <option value="{year}">{year}</option>\n'
    
    # Generate month options
    month_options = '<option value="all">All Months</option>\n'
    for i, month in enumerate(MONTH_NAMES, 1):
        month_options += f'                        <option value="{i}">{month}</option>\n'
    
    # Generate programme cards
    if programmes:
        cards_html = ""
        for prog in programmes:
            # Check for thumbnail
            thumbnail_file = prog.get('thumbnail_file')
            thumb_html = ""
            card_class = "news-card"
            
            if thumbnail_file:
                thumb_html = f'''
                <img src="news/{prog['folder']}/{thumbnail_file}" class="card-bg-thumb" alt="" loading="lazy">
                <div class="card-overlay"></div>
                '''
                card_class += " has-thumbnail"

            cards_html += f'''
            <a href="news/{prog['folder']}/index.html" class="{card_class}" data-year="{prog['year']}" data-month="{prog['month']}">
                {thumb_html}
                <div class="news-card-header">
                    <h3>{prog['title']}</h3>
                    <div class="news-card-date">
                        <span>{prog['date_display']}</span>
                    </div>
                </div>
                <div class="news-card-body">
                    <p>{prog['description']}</p>
                </div>
                <div class="news-card-footer">
                    {f'<span class="footer-btn">View Programme →</span>' if thumbnail_file else 'View Programme →'}
                </div>
            </a>
            '''
        
        content_html = f'''
        <!-- Filter Section -->
        <div class="filter-section">
            <div class="filter-row">
                <span class="filter-label">Filter by:</span>
                <select id="yearFilter" class="filter-select" onchange="filterProgrammes()">
                    {year_options}
                </select>
                <select id="monthFilter" class="filter-select" onchange="filterProgrammes()">
                    {month_options}
                </select>
            </div>
        </div>

        <!-- Programme Cards -->
        <div class="news-grid" id="newsGrid">
            {cards_html}
        </div>

        <!-- No Results Message -->
        <div class="no-results" id="noResults">
            <div class="no-results-icon">🔍</div>
            <h3>No programmes found</h3>
            <p>No programmes match the selected period. Try adjusting your filters.</p>
        </div>
        '''
    else:
        content_html = '''
        <div class="empty-state">
            <div class="empty-state-icon">📰</div>
            <h3>No Programmes Yet</h3>
            <p>Check back soon for updates on our latest programmes and activities!</p>
        </div>
        '''
    
    # JavaScript filter function
    filter_script = '''
        function toggleMenu() {
            document.getElementById('navLinks').classList.toggle('active');
        }

        function filterProgrammes() {
            const yearFilter = document.getElementById('yearFilter').value;
            const monthFilter = document.getElementById('monthFilter').value;
            const cards = document.querySelectorAll('.news-card');
            const noResults = document.getElementById('noResults');
            
            let visibleCount = 0;

            cards.forEach(card => {
                const cardYear = card.dataset.year;
                const cardMonth = card.dataset.month;
                
                const matchYear = yearFilter === 'all' || cardYear === yearFilter;
                const matchMonth = monthFilter === 'all' || cardMonth === monthFilter;

                if (matchYear && matchMonth) {
                    card.classList.remove('hidden');
                    visibleCount++;
                } else {
                    card.classList.add('hidden');
                }
            });

            // Show/hide no results message
            if (noResults) {
                if (visibleCount === 0) {
                    noResults.classList.add('visible');
                } else {
                    noResults.classList.remove('visible');
                }
            }
        }
    '''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Latest news and programmes from YMCA Matara, Sri Lanka.">
    <title>News & Programmes | YMCA Matara</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="icon" type="image/png" href="images/ymca.png">
    <style>{get_common_styles()}</style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="index.html" class="logo">
                <img src="images/ymca.png" class="logo-icon" alt="YMCA Logo">
                <div class="logo-text">
                    YMCA Matara
                    <span>Sri Lanka</span>
                </div>
            </a>
            <button class="mobile-menu-btn" onclick="toggleMenu()" aria-label="Toggle menu">☰</button>
            <ul class="nav-links" id="navLinks">
                <li><a href="index.html">About</a></li>
                <li><a href="news.html" class="active">News</a></li>
            </ul>
        </div>
    </nav>

    <!-- Page Header -->
    <header class="page-header">
        <div class="page-header-content">
            <h1>News & Programmes</h1>
            <p>Stay updated with our latest activities and completed programmes</p>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        {content_html}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <p class="footer-text">© 2024 YMCA Matara, Sri Lanka. Part of the World YMCA Movement.</p>
        </div>
    </footer>

    <script>
        {filter_script}
    </script>
</body>
</html>'''


def generate_programme_html(title: str, date_str: str, article_html: str, media_files: list) -> str:
    """Generate the programme detail page with Markdown content"""
    
    date_display = format_date_display(date_str)
    
    # Generate gallery items
    gallery_html = ""
    for media in media_files:
        ext = Path(media).suffix.lower()
        if ext in IMAGE_EXTENSIONS:
            alt_text = Path(media).stem.replace('-', ' ').replace('_', ' ').title()
            gallery_html += f'''
            <div class="gallery-item" onclick="openImageViewer('{media}')">
                <img src="{media}" alt="{alt_text}" loading="lazy">
            </div>
            '''
        elif ext in VIDEO_EXTENSIONS:
            gallery_html += f'''
            <div class="gallery-item" onclick="openVideoViewer('{media}')">
                <video src="{media}" preload="metadata" muted></video>
            </div>
            '''
    
    # Gallery section (only if there are media files)
    gallery_section = ""
    if gallery_html:
        gallery_section = f'''
        <section class="gallery-section">
            <h2>Photos & Videos</h2>
            <div class="gallery-grid">
                {gallery_html}
            </div>
        </section>
        '''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} - YMCA Matara Programme">
    <title>{title} | YMCA Matara</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="icon" type="image/png" href="../../images/ymca.png">
    <style>{get_common_styles()}</style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="../../index.html" class="logo">
                <img src="../../images/ymca.png" class="logo-icon" alt="YMCA Logo">
                <div class="logo-text">
                    YMCA Matara
                    <span>Sri Lanka</span>
                </div>
            </a>
            <button class="mobile-menu-btn" onclick="toggleMenu()" aria-label="Toggle menu">☰</button>
            <ul class="nav-links" id="navLinks">
                <li><a href="../../index.html">About</a></li>
                <li><a href="../../news.html" class="active">News</a></li>
            </ul>
        </div>
    </nav>

    <!-- Page Header -->
    <header class="page-header">
        <div class="page-header-content">
            <h1>{title}</h1>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        <a href="../../news.html" class="back-link">← Back to News</a>
        
        <article class="programme-content">
            <div class="programme-meta">
                <span>📅</span>
                <span>{date_display}</span>
            </div>
            <div class="article-content">
                {article_html}
            </div>
            {gallery_section}
        </article>
    </main>

    <!-- Media Viewer Modal -->
    <div id="viewerOverlay" class="viewer-overlay" onclick="closeViewer(event)">
        <button class="viewer-close" onclick="closeViewer(event)">&times;</button>
        <div class="viewer-content" id="viewerContent"></div>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <p class="footer-text">© 2024 YMCA Matara, Sri Lanka. Part of the World YMCA Movement.</p>
        </div>
    </footer>

    <script>
        function toggleMenu() {{
            document.getElementById('navLinks').classList.toggle('active');
        }}

        function openImageViewer(src) {{
            const overlay = document.getElementById('viewerOverlay');
            const content = document.getElementById('viewerContent');
            content.innerHTML = '<img src="' + src + '" alt="Full size image">';
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }}

        function openVideoViewer(src) {{
            const overlay = document.getElementById('viewerOverlay');
            const content = document.getElementById('viewerContent');
            content.innerHTML = '<video src="' + src + '" controls autoplay></video>';
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }}

        function closeViewer(event) {{
            if (event) {{
                const target = event.target;
                // Only close if clicking overlay background or close button
                if (!target.closest('.viewer-content') || target.closest('.viewer-close')) {{
                    const overlay = document.getElementById('viewerOverlay');
                    const content = document.getElementById('viewerContent');
                    overlay.classList.remove('active');
                    content.innerHTML = '';
                    document.body.style.overflow = '';
                }}
            }}
        }}

        // Close on Escape key
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                closeViewer({{ target: document.getElementById('viewerOverlay') }});
            }}
        }});
    </script>
</body>
</html>'''


def scan_programmes() -> list:
    """Scan the news directory for programme folders and read info.json"""
    programmes = []
    
    if not NEWS_DIR.exists():
        print(f"[*] Creating news directory: {NEWS_DIR}")
        NEWS_DIR.mkdir(parents=True, exist_ok=True)
        return programmes
    
    for item in NEWS_DIR.iterdir():
        # Skip hidden files/folders and non-directories
        if item.name.startswith('.') or not item.is_dir():
            continue
        
        info_file = item / "info.json"
        
        # Check for info.json
        if not info_file.exists():
            print(f"    [!] Skipping {item.name}: No info.json found")
            continue
        
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                info = json.load(f)
            
            # Validate required fields
            title = info.get('title', item.name.replace('-', ' ').title())
            date_str = info.get('date', '2024-01-01')
            description = info.get('description', 'Click to view details.')
            
            # Parse date to extract year and month
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                year = str(date_obj.year)
                month = str(date_obj.month)
            except:
                year = '2024'
                month = '1'
            
            # Detect thumbnail file (prefer png, then jpg, then jpeg)
            thumbnail_file = None
            for ext in ['.png', '.jpg', '.jpeg']:
                if (item / f"thumbnail{ext}").exists():
                    thumbnail_file = f"thumbnail{ext}"
                    break

            programmes.append({
                'folder': item.name,
                'title': title,
                'date': date_str,
                'date_display': format_date_display(date_str),
                'description': description,
                'year': year,
                'month': month,
                'path': item,
                'thumbnail_file': thumbnail_file
            })
            
        except json.JSONDecodeError as e:
            print(f"    [!] Error parsing {info_file}: {e}")
            continue
    
    # Sort by date descending (newest first)
    programmes.sort(key=lambda x: x['date'], reverse=True)
    
    return programmes


def get_media_files(folder_path: Path) -> list:
    """Get all media files in a programme folder"""
    media_files = []
    
    for item in folder_path.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            # Skip special files and thumbnails
            if item.name.lower() in ('info.json', 'article.md', 'description.txt', 'index.html') or item.stem.lower() == 'thumbnail':
                continue
            # Check if it's a media file
            if ext in IMAGE_EXTENSIONS or ext in VIDEO_EXTENSIONS:
                media_files.append(item.name)
    
    # Sort alphabetically
    media_files.sort()
    
    return media_files


def build_site():
    """Main function to build the site"""
    print("=" * 50)
    print("  YMCA Matara Website Builder v2.0")
    print("=" * 50)
    print()
    
    # Scan for programmes
    print("[*] Scanning for programmes...")
    programmes = scan_programmes()
    print(f"    Found {len(programmes)} programme(s)")
    print()
    
    # Extract unique years for filter
    years = sorted(set(prog['year'] for prog in programmes), reverse=True)
    
    # Generate news.html
    print("[*] Generating news.html with filters...")
    news_html = generate_news_html(programmes, years)
    with open(NEWS_HTML, 'w', encoding='utf-8') as f:
        f.write(news_html)
    print(f"    [OK] Created: {NEWS_HTML}")
    print()
    
    # Generate programme pages
    if programmes:
        print("[*] Generating programme pages...")
        md_converter = markdown.Markdown(extensions=['extra'])
        
        for prog in programmes:
            folder_path = prog['path']
            article_file = folder_path / "article.md"
            
            # Read article content
            article_html = ""
            if article_file.exists():
                with open(article_file, 'r', encoding='utf-8') as f:
                    article_md = f.read()
                article_html = md_converter.convert(article_md)
                md_converter.reset()
            else:
                article_html = "<p>No content available.</p>"
                print(f"    [!] No article.md found in {prog['folder']}")
            
            # Get media files
            media_files = get_media_files(folder_path)
            
            # Generate HTML
            programme_html = generate_programme_html(
                prog['title'],
                prog['date'],
                article_html,
                media_files
            )
            
            # Write to file
            output_file = folder_path / "index.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(programme_html)
            
            print(f"    [OK] Created: news/{prog['folder']}/index.html")
            if media_files:
                print(f"         {len(media_files)} media file(s) included")
        print()
    
    print("=" * 50)
    print("[+] Build complete!")
    print()
    print("Summary:")
    print(f"    - news.html updated with {len(programmes)} programme(s)")
    print(f"    - Year/Month filter enabled with {len(years)} year(s)")
    print(f"    - {len(programmes)} programme page(s) generated")
    print()
    print("Next steps:")
    print("    1. Run: python -m http.server 8000")
    print("    2. Open: http://localhost:8000")
    print("    3. Commit and push to GitHub")
    print("=" * 50)


if __name__ == "__main__":
    build_site()
