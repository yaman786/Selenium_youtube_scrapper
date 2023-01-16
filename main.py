from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'
def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options =chrome_options)
  return driver

def get_videos(driver):
  driver.get(YOUTUBE_TRENDING_URL)
  videos = driver.find_elements(By.TAG_NAME,'ytd-video-renderer')
  return videos
def parse_video(video):
  title_tag = video.find_element(By.ID,'video-title')
  title = title_tag.text
  URL = title_tag.get_attribute('href')
  
  thumbnail_tag = video.find_element(By.TAG_NAME,"img")
  thumnail_url = thumbnail_tag.get_attribute('src')
  
  channel_div = video.find_element(By.CLASS_NAME,'ytd-channel-name')
  channel_name = channel_div.text
  description =video.find_element(By.ID,'description-text').text
  
  return {
    'title':title,
    'url':URL,
    'channel':channel_name,
    'thumnail_url':thumnail_url,
    'description':description,
     } 
  
  
if __name__ == "__main__":
  print("creating driver")
  driver = get_driver()
  
  print('fetching trending videos')
  videos = get_videos(driver)
  
  print(f'found {len(videos)} videos')

  print("parsing the Top 10 videos")
  video_data = [parse_video(video) for video in videos[:10]]
  
  print(video_data)

  print('save the data into CSV')
  videos_df = pd.DataFrame(video_data)
  print(videos_df)

  videos_df.to_csv('trending.csv',index=None)