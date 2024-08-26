from flask import Flask, jsonify, redirect, url_for
import requests
from bs4 import BeautifulSoup
from waitress import serve

app = Flask(__name__)

# def scrape_data():
#     url = 'https://indianexpress.com/article/cities/mumbai/plane-grounded-in-france-over-human-trafficking-lands-in-mumbai-9082765/'
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx and 5xx)
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Print the soup to see the HTML structure (for debugging)
#         print(soup.prettify())

#         # Adjust these based on actual HTML structure
#         title_tag = soup.find('h1')
#         content_tag = soup.find('div', {'class': 'article'})

#         # Check if the elements are found before trying to access their attributes
#         title = title_tag.text.strip() if title_tag else "Title not found"
#         content = content_tag.text.strip() if content_tag else "Content not found"

#         # Extracting images (optional)
#         images = [img['src'] for img in soup.find_all('img', src=True)]

#         return {
#             'title': title,
#             'content': content,
#             'images': images
#         }
#     except requests.exceptions.RequestException as e:
#         # Handle request-related errors
#         print(f"Request error: {e}")
#         return {
#             'error': 'Failed to retrieve data from the URL'
#         }
#     except Exception as e:
#         # Handle other errors
#         print(f"Error: {e}")
#         return {
#             'error': 'An error occurred during data processing'
#         }

def scrape_data():
    url = 'https://indianexpress.com/article/cities/mumbai/plane-grounded-in-france-over-human-trafficking-lands-in-mumbai-9082765/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx and 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Print the soup to see the HTML structure (for debugging)
        print(soup.prettify())

        # Adjust these based on actual HTML structure
        title_tag = soup.find('h1')
        content_tags = soup.find_all('p')

        # Check if the elements are found before trying to access their attributes
        title = title_tag.text.strip() if title_tag else "Title not found"
        
        # Extract text from all <p> tags into a list
        content = [p.text.strip() for p in content_tags] if content_tags else ["Content not found"]

        # Extracting images (optional)
        images = [img['src'] for img in soup.find_all('img', src=True)]

        return {
            'title': title,
            'content': content,
            'images': images
        }
    except requests.exceptions.RequestException as e:
        # Handle request-related errors
        print(f"Request error: {e}")
        return {
            'error': 'Failed to retrieve data from the URL'
        }
    except Exception as e:
        # Handle other errors
        print(f"Error: {e}")
        return {
            'error': 'An error occurred during data processing'
        }


@app.route('/')
def home():
    return redirect(url_for('scrape_endpoint'))

@app.route('/scrape', methods=['GET'])
def scrape_endpoint():
    data = scrape_data()
    return jsonify(data)

if __name__ == "__main__":
    # Use Waitress to serve the application (production)
    # serve(app, host='127.0.0.1', port=8081)
    app.run(debug=True, host='127.0.0.1', port=8080)
