import feedparser
import csv

def get_post_link(client_website, description):
  links = []
  index = 0
  while True:
    link_start = description.find('href="', index) + len('href="')
    if link_start == 5:
      break
    link_end = description.find('"', link_start)
    link = description[link_start:link_end]
    links.append(link)
    index = link_end
  for link in links:
    client_website = client_website[client_website.find('//'):].strip('/')
    if client_website in link:
      return link

def get_blog_posts(client_name, client_website, blog_rss_url, month, seo_specialist):
  d = feedparser.parse(blog_rss_url)
  posts = [entry for entry in d.entries if month in entry.published]
  final_posts = []
  for post in posts:
    output_data = [client_name,"Active","Blog",post.title]
    try:
      post_content = post.content[0]["value"]
    except AttributeError:
      post_content = post.description
    output_data.append(get_post_link(client_website, post_content))
    output_data.append(client_website)
    output_data.append(post.link)
    #output_data.append(seo_specialist)
    final_posts.append(output_data)
  return final_posts

def get_num_posts(client_package):
  if "get started" in client_package.lower() or "bas" in client_package.lower():
    num_posts = 2
  elif client_package.lower() == "standard":
    num_posts = 3
  elif client_package.lower() == "advanced":
    num_posts = 4
  else:
    num_posts = 4
  return num_posts

with open('output.csv', 'w', newline='') as csvfile:
  output_writer = csv.writer(csvfile, delimiter=',')
  with open('input.csv') as csvfile:
    header_row = ['Client','Status','Link Type','Link Text','Link URL','Website Name','Website URL','SEO Specialist']
    output_writer.writerow(header_row)
    for row in csv.reader(csvfile, delimiter=','):
      client_name = row[0]
      client_website = row[1]
      blog_rss_url = row[2]
      month = row[3]
      seo_specialist = row[4]
      client_package = row[5]
      final_posts = get_blog_posts(client_name, client_website, blog_rss_url, month, seo_specialist)
      print(final_posts)

      if len(final_posts) > get_num_posts(client_package):
        for post in final_posts:
          post.append('POST COUNT DISCREPANCY. PLEASE CHECK BY HAND.')

      while len(final_posts) < get_num_posts(client_package):
        final_posts.append([client_name,"Active","Blog","" ,"" ,"" ,"" ,"COULD NOT PULL"])

      for post in final_posts:
        output_writer.writerow(post)       
      
      print(f'Finished for: {client_name}')
