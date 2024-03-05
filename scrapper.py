import requests
from bs4 import BeautifulSoup

class Deal:
    def __init__(self, store, item, votes, username, timestamp, category, replies, views, url):
        self.store = store
        self.item = item
        self.votes = votes
        self.username = username
        self.timestamp = timestamp
        self.category = category
        self.replies = replies
        self.views = views
        self.url = url

    def __str__(self):
        return f"Store: {self.store}\nItem: {self.item}\nVotes: {self.votes}\nUsername: {self.username}\nTimestamp: {self.timestamp}\nCategory: {self.category}\nReplies: {self.replies}\nViews: {self.views}\nURL: {self.url}\n{'-'*50}"

class DealAnalyzer:
    def __init__(self, deals):
        self.deals = deals

    def display_latest_deals(self):
        print(f"Total deals found: {len(self.deals)}")
        for deal in self.deals:
            print(deal)

    def analyze_deals_by_category(self):
        categories = {}
        for deal in self.deals:
            category = deal.category
            categories[category] = categories.get(category, 0) + 1

        print("Deals by Category:")
        for category, count in categories.items():
            print(f"{category}: {count} deals")

    def find_top_stores(self):
        n = int(input("Enter the number of top stores to display: "))
        stores = {}
        for deal in self.deals:
            store = deal.store
            stores[store] = stores.get(store, 0) + 1

        top_stores = sorted(stores.items(), key=lambda x: x[1], reverse=True)[:n]
        print("Top Stores:")
        for store, count in top_stores:
            print(f"{store}: {count} deals")

    def log_deal_information(self):
        print("List of Categories:")
        categories = set(deal.category for deal in self.deals if deal.category != "N/A")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        if not categories:
            print("No valid categories found.")
            return

        while True:
            try:
                category_index = int(input("Enter the number corresponding to the category: "))
                selected_category = list(categories)[category_index - 1]
                break
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid number.")

        with open('log.txt', 'w') as file:
            for deal in self.deals:
                if deal.category == selected_category:
                    file.write(f"{deal.url}\n")

        print("All the links have been logged successfully.")
        
class WebScraper:
    @staticmethod
    def get_store(listing):
        store_element_retailer = listing.select_one('.topictitle_retailer')
        store_element = listing.select_one('.topictitle')

        if store_element_retailer:
            return store_element_retailer.text.strip()
        elif store_element:
            store_text = store_element.text.strip()
            return store_text.split(']')[0][1:].strip() if ']' in store_text else store_text
        else:
            return "N/A"

    def __init__(self, url):
        self.url = url

    def scrape(self):
        response = requests.get(self.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        deals = []
        base_url = "https://forums.redflagdeals.com/"

        for listing in soup.find_all("li", class_="row topic"):
            store = WebScraper.get_store(listing)
            item_element = listing.select_one('.topic_title_link')
            item = item_element.text.strip() if item_element else "N/A"

            votes_element = listing.select_one('.total_count_selector')
            votes = votes_element.text.strip() if votes_element else "N/A"

            username = listing.select_one('.thread_meta_author').text.strip()
            timestamp = listing.select_one('.first-post-time').text.strip()

            # Check if the element exists before accessing its text attribute
            category_element = listing.select_one('.thread_category a')
            category = category_element.text.strip() if category_element else "N/A"

            replies = listing.select_one('.posts').text.strip()
            views = listing.select_one('.views').text.strip()
            url_element = item_element['href'] if item_element else "N/A"
            url = base_url + url_element

            deal = Deal(store, item, votes, username, timestamp, category, replies, views, url)
            deals.append(deal)

        return deals
        
def main():
    url = "https://forums.redflagdeals.com/hot-deals-f9/"
    web_scraper = WebScraper(url)
    deals = web_scraper.scrape()

    deal_analyzer = DealAnalyzer(deals)

    while True:
        print("\n***** Web Scraping Adventure *****")
        print("1. Display Latest Deals")
        print("2. Analyze Deals by Category")
        print("3. Find Top Stores")
        print("4. Log Deal Information")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            deal_analyzer.display_latest_deals()
        elif choice == '2':
            deal_analyzer.analyze_deals_by_category()
        elif choice == '3':
            deal_analyzer.find_top_stores()
        elif choice == '4':
            deal_analyzer.log_deal_information()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
