from scrape import run_scraper


import schedule
import time
from datetime import datetime, timedelta

def task(search):
    run_scraper()

def schedule_tasks(searches):
    start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)  # Start time at 8:00 AM
    end_time = start_time + timedelta(hours=10)  # 10 hours from start time
    interval = (end_time - start_time) / 100  # Time interval between tasks
    for search in searches:
        schedule.every().day.at(start_time.strftime("%H:%M:%S")).do(run_scraper, text=search)
        start_time += interval
    # for i in range(100):
    #     task_time = start_time + i * interval
    #     schedule.every().day.at(task_time.strftime("%H:%M:%S")).do(task, job_id=i+1)


searches = [
    "Best cloud computing services for small businesses",
    "Top 10 AI tools for businesses in 2024",
    "Affordable cybersecurity solutions for enterprises",
    "5G technology providers in the US",
    "Best laptops for graphic designers 2024",
    "Top medications for treating anxiety",
    "Best health insurance plans for families",
    "Affordable prescription drugs online",
    "Benefits of telemedicine for chronic conditions",
    "Leading cancer treatment centers in the US",
    "Upcoming blockbuster movies 2024",
    "Top streaming services for documentaries",
    "Best performing arts schools in New York",
    "Broadway shows with ticket availability",
    "Top 10 music festivals in Europe",
    "Best credit cards for travel rewards",
    "Top-rated financial advisors near me",
    "How to invest in cryptocurrency in 2024",
    "Mortgage refinance rates comparison",
    "Best stock trading platforms for beginners",
    "Top meal delivery services for keto diet",
    "Best coffee shops in San Francisco",
    "Organic food delivery services in LA",
    "Top-rated restaurants for fine dining in NYC",
    "Best wine subscriptions for connoisseurs",
    "Best running shoes for marathon training",
    "Top-rated golf clubs for beginners",
    "Affordable gym memberships near me",
    "Best supplements for bodybuilding",
    "Top sports betting apps in 2024",
    "Leading research labs for genetic engineering",
    "Top universities for physics research",
    "Best online courses for data science",
    "NASA's upcoming space missions",
    "Cutting-edge advancements in renewable energy",
    "Best all-inclusive resorts in the Caribbean",
    "Top travel insurance providers for international trips",
    "Affordable luxury hotels in Paris",
    "Best cruises to Alaska",
    "Top-rated adventure travel companies",
    "Best CRM software for small businesses",
    "Top industrial automation companies",
    "Affordable bulk office supplies online",
    "Best B2B marketing strategies in 2024",
    "Top-rated commercial real estate firms",
    "Best internet providers in rural areas",
    "Top VoIP services for businesses",
    "Affordable international calling plans",
    "Best mobile data plans for travelers",
    "Top web hosting services for e-commerce",
    "Best gaming laptops under $1500",
    "Top-rated VR headsets in 2024",
    "Affordable gaming chairs for long sessions",
    "Best PC games for strategy lovers",
    "Top game development engines in 2024",
    "Best electric cars under $50,000",
    "Top-rated car insurance providers",
    "Affordable luxury SUVs in 2024",
    "Best car maintenance tips for winter",
    "Top tire brands for off-road driving",
    "Best smart home devices in 2024",
    "Affordable home security systems",
    "Top-rated lawn care services near me",
    "Best kitchen appliances for small spaces",
    "Affordable interior designers in NYC",
    "Best anti-aging skincare products",
    "Top-rated fitness apps for home workouts",
    "Affordable beauty salons near me",
    "Best organic makeup brands",
    "Top supplements for healthy hair",
    "Best online retailers for electronics",
    "Top-rated clothing stores for men",
    "Affordable furniture stores near me",
    "Best deals on home appliances",
    "Top-rated online shopping sites for kids' toys",
    "Top 10 luxury watches in 2024",
    "Best life insurance providers",
    "Top-rated real estate agents near me",
    "How to start a small business with $10,000",
    "Best investment strategies for retirement",
    "Best tools for remote work productivity",
    "Top-rated educational toys for toddlers",
    "Affordable organic skincare for sensitive skin",
    "Best luxury car rental services",
    "Top-rated industrial equipment suppliers",
    "Best online MBA programs",
    "Top cybersecurity certifications",
    "Best vegan restaurants in Los Angeles",
    "Top-rated pet insurance providers",
    "Affordable wedding venues near me",
    "Best real estate investment strategies",
    "Top-rated mortgage brokers in my area",
    "Affordable home renovation contractors",
    "Best places to buy rental property in 2024",
    "Top home warranty providers",
    "Best online coding bootcamps",
    "Top universities for business studies",
    "Affordable online tutoring services",
    "Best apps for language learning",
    "Top-rated test prep courses for GRE"
]

schedule_tasks(searches)

while True:
    schedule.run_pending()
    time.sleep(1)
