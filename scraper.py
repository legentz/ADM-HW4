from requests import get
from bs4 import BeautifulSoup
import time, re, os

class Scraper:
	def __init__(self, base_url, query_params='', start_from=1, n_ads=100, sleep=0.5, onfile=False, verbose=False):

		# check url
		assert base_url is not None, 'Bad url'

		# props
		self.current_page = start_from - 1
		self.n_ads = n_ads

		# sleep after each request
		self.sleep = sleep
		self.base_url = base_url 

		# if query_params is not being formatted
		# then there's no pagination over url
		self.query_params = query_params

		# enable logs
		self.verbose = verbose

		# out
		self.onfile = onfile
		self.raw_description_ds = './description-dataset-raw_' + self.__get_timestamp() + '.tsv'
		self.information_ds = './information-dataset_' + self.__get_timestamp() + '.tsv'

		# check out
		assert not os.path.isfile(self.raw_description_ds), 'Out file already exists!'
		assert not os.path.isfile(self.information_ds), 'Out file already exists!'

	# start scraper
	def init(self):

		# container of scraped stuff
		scraped_ads = {}

		try:
			# scrape until we reached a no. of ads
			while self.n_ads > len(scraped_ads.keys()):

				# get next url
				url = self.__get_next_url()

				# get page html content
				page_content = self.__get_html(url)

				# 404
				if page_content is None: break

				# setting soup
				# todo: put in a function
				soup = BeautifulSoup(page_content, 'html.parser')

				# extract ul
				# todo: generalize
				ul_container = self.__extract_tag_with_props(soup, tag='ul', props={
					'id': 'listing-container'
				})

				# iterate over li
				for i, item in self.__iterate_over_tag(ul_container, tag='li'):

					# consider only valid ads
					if item.has_attr('data-id'):

						# extract data from item
						data = self.__extract_info(item)

						# skip if not valid data
						if not data: continue

						# make this customisable 

						if not self.onfile:
							scraped_ads[data['data-id']] = data
						else:
							self.__store_data(data)

					# check n_max
					if self.n_ads <= len(scraped_ads.keys()): break

				if self.verbose:
					print('Retrieved ' + str(len(scraped_ads.keys())) + ' items')

			return scraped_ads

		# catch system stop
		except (KeyboardInterrupt, ConnectionError) as e:
			print('Interrupting process...')
			print('Scraped: ' + str(len(scraped_ads.keys())))

			# return what we got instead of losing it
			return scraped_ads

	def __get_timestamp(self):
		return str(int(time.time()))

	def __store_data(self, data):

		# store on information dataset
		with open(self.information_ds, 'a') as out:
			out.write(
				data['data-id'] + '\t' +
				data['price'] + '\t' +
				data['rooms'] + '\t' +
				data['surface'] + '\t' +
				data['bathrooms'] + '\t' +
				data['floor'] + '\n'
			)

		# store on description dataset
		with open(self.raw_description_ds, 'a') as out:
			out.write(
				data['data-id'] + '\t' +
				data['description'] + '\n'
			)

	# todo: generalize
	def __extract_info(self, item):
		data_id = item['data-id']

		# link
		href = item.find('a', {'id': 'link_ad_' + data_id})['href']
		href = self.base_url[:-1] + href if not href.startswith('http') else href

		# other
		price = item.select_one('li.lif__item.lif__pricing')
		rooms = item.select_one('li:nth-of-type(2) > div.lif__data > span')
		bathrooms = item.select_one('li:nth-of-type(4) > div.lif__data > span')
		surface = item.select_one('li:nth-of-type(3) > div.lif__data > span')
		floor = item.select_one('li.lif__item.hidden-xs > div.lif__data > abbr')

		# from href link
		description = self.__get_full_description(href)

		# if something's missing, we have to discard this element
		if not all([data_id, href, price, rooms, bathrooms, surface, floor, description]):
			return False
		return {
			'data-id': data_id,
			'href': href,
			'price': price.get_text(strip=True).strip().replace('€', '').split(' ')[1],
			'rooms': rooms.get_text(strip=True).strip(),
			'bathrooms': bathrooms.get_text(strip=True).strip(),
			'surface': surface.get_text(strip=True).strip(),
			'floor': floor.get_text(strip=True).strip(),
			'description': description.strip().replace('\n', '')
		}

	def __get_full_description(self, href):
		page_content = self.__get_html(href)

		# 404
		if page_content is None: return False

		# parse
		# todo: put in a function
		soup_desc = BeautifulSoup(page_content, 'html.parser')

		# get description text
		description = self.__extract_tag_with_props(soup_desc, tag='div', props={
			'class': 'description-text',
			'role': 'contentinfo'
		}).text
		return self.__strip_html_from_string(description)

	def __strip_html_from_string(self, string):
		return re.sub(re.compile('<.*?>'), '', string)

	def __get_next_url(self):

		# no format needed, no pagination
		if '{}' not in self.query_params: 
			return self.base_url + self.query_params

		# next page
		self.current_page += 1

		# format query
		return self.base_url + self.query_params.format(self.current_page)

	# request: get html from URL
	def __get_html(self, url):

		# info
		if self.verbose:
			print('GET: ' + url)

		# performing the request
		req = get(url)

		# sleep for n seconds to avoid being blocked
		time.sleep(self.sleep)

		# check the status code
		if req.status_code == '404':
			return None
		return req.content

	def __iterate_over_tag(self, elem, tag=None):
		
		# tag has to be NOT None
		assert tag is not None

		for i, item in enumerate(elem.findAll(tag)):
			yield i, item

	def __extract_tag_with_props(self, soup, tag=None, props=None):

		# has to be dict
		assert isinstance(props, dict)

		# tag has to be NOT None
		assert tag is not None

		if props is not None:
			return soup.find(tag, props)
		return soup.find(tag)