# **SYSTEM SPECIFICATION: YMCA Matara Responsive CMS (V2)**

## **1\. Project Goal**

Create a static website for YMCA Matara where the **About page is the primary Landing Page (Home)**. The News section should be a secondary tab that is automatically updated by a Python script based on folder contents.

## **2\. Directory Structure**

* ymca-website/  
  * index.html (Home/About Page \- Permanent content)  
  * news.html (Generated/Updated by script \- The News list)  
  * build\_site.py (The Python Engine)  
  * news/  
    * \[programme-folder-name\]/  
      * description.txt (Content)  
      * \[media files\] (Images/Videos)  
      * index.html (Generated programme detail page)

## **3\. Technical Requirements (The Python Engine)**

Build a build\_site.py script that performs the following:

* **Automation:** Iterate through subdirectories in news/ (ignoring hidden files).  
* **Core Task 1 (News Feed):** Update news.html with a list of links to all detected programmes.  
* **Core Task 2 (Programme Pages):** Inside each programme folder, generate an index.html displaying description.txt (with white-space: pre-wrap;) and a responsive media gallery.  
* **Pathing:** \- Nav links on index.html and news.html use direct links (e.g., href="news.html").  
  * Nav links inside news/\[folder\]/index.html must use relative parent paths (e.g., ../../index.html) to work on GitHub Pages.

## **4\. Design & Navigation**

* **Home Page (index.html):** This is the "About YMCA Matara" page. It must be professional and mobile-responsive.  
* **Navigation Tabs:** A consistent top bar with: \[About\] | \[News\].  
  * On the Home page, \[About\] is active.  
  * On the News page/Programme pages, \[News\] is active.  
* **Mobile Support:** Full responsiveness using \<meta name="viewport"\> and CSS Flexbox/Grid.  
* **Branding:** \- YMCA Blue: \#004a99 | YMCA Red: \#cc0000.  
  * Gallery: Grid layout repeat(auto-fit, minmax(250px, 1fr)).

## **5\. Implementation Instructions for the AI**

1. Generate the index.html (About/Home) with high-quality placeholder text about YMCA.  
2. Generate the build\_site.py script that manages news.html and the sub-pages.  
3. Ensure the CSS is identical across all templates so the transition between "About" and "News" is seamless.  
4. The script should automatically "title-case" folder names (e.g., youth-camp becomes Youth Camp).