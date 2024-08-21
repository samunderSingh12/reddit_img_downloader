import requests
import os
import atexit

def download_images(subreddit_name, num_images):
    # Reddit API endpoint
    url = f"https://www.reddit.com/r/{subreddit_name}/new.json?limit={num_images * 2}"
    # Make the HTTP request
    headers = {'User-Agent': 'python:myapp:v1.0 (by /u/yourusername)'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return
    data = response.json()
    # Create a directory to save images
    if not os.path.exists('images'):
        os.makedirs('images')
    count = 0
    total_posts_checked = 0
    for post in data['data']['children']:
        if count >= num_images:
            break
        total_posts_checked += 1
        # Check if the post contains an image URL
        image_url = post['data'].get('url', '')
        if image_url.endswith(('.jpg', '.jpeg', '.png')):
            try:
                img_response = requests.get(image_url, stream=True)
                img_response.raise_for_status()
                # Save image to directory
                with open(f'images/{count}.jpg', 'wb') as file:
                    file.write(img_response.content)
                count += 1
                print(f"Downloaded image {count}: {image_url}")
            except requests.RequestException as e:
                print(f"Error downloading image {image_url}: {e}")
    print(f"Downloaded {count} images out of {total_posts_checked} posts checked.")

@atexit.register
def delete_images():
    import shutil
    print("Deleting downloaded images...")
    shutil.rmtree('images')
    print("Images deleted.")

def show_images():
    os.system('sxiv images/*.jpg')
    delete_images()

if __name__ == "__main__":
    subreddit_name = input("Enter the subreddit name: ")
    num_images = int(input("Enter the number of images to download: "))
    download_images(subreddit_name, num_images)
    show_images()
