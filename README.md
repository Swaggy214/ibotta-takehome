# ibotta-takehome

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Git

### Installation & Setup

1. **Clone the repository**
```bash
   git clone https://github.com/Swaggy214/ibotta-takehome.git
   cd ibotta-takehome
```

2. **Verify project structure**
   Ensure your directory looks like this:
```
    ibotta-takehome/
    │
    ├── csv_data/
    │   ├── offer_rewards_168083.csv
    │   ├── customer_offers_296332.csv
    │   ├── customer_offer_rewards_144392.csv
    │   └── customer_offer_redemptions_31025.csv
    │
    ├── database/
    │   └── ibotta.db
    │
    ├── Python/
    │    ├── db_utils.py
    │    ├── main.py
    │    └── query.py
    │ 
    └── README.md    
```

3. **(Optional) Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Run the ETL pipeline**

## Running from the play button
# line 9
conn = create_connection("../Database/ibotta.db")

# line 14
csv_folder = Path("../CSV_data")


## Running from the terminal
# line 9
conn = create_connection("./Database/ibotta.db")

# line 14
csv_folder = Path("./CSV_data")

Then run:
```bash
   python Python/main.py
```
   
   Expected output:
```
   Loading CSV_data/offer_rewards_168083.csv into offer_rewards...
   Loading CSV_data/customer_offers_296332.csv into customer_offers...
   ...
   All tables have been loaded!
```

5. **Verify the database**
   The SQLite database will be created at `Database/ibotta.db`
```bash
   sqlite3 Database/ibotta.db "SELECT name FROM sqlite_master WHERE type='table';"
```

### Running SQL Queries
[Include your query instructions here]

Part 1:
My first steps were to set up a new GitHub repo, as I figured it would be easiest to work in
I then went over the existing code that was given to me to figure out what gaps I need to fill, and what I will need to write myself.
This is where I added the descriptions to the existing code.

Using the functions in db_utils, I called them in the main.py to accurately populate the tables

Part 2:
Time to query the tables. I had 4 questions to answer
The first thing I did was set up a query console, and verify I could query all 4 tables
After doing that, I examined each table to get a firm idea of all the columns and what each table represented

Query 1 thought process:
I need to gather counts of distinct members who have a timestamp in the "activated" column
The way I do this is select the column I care about, and an aggregate count(*). This requires a group by.
When I group by customer_id, it makes sure I am only looking at distinct IDs.
To make sure I wasn't including null values in these counts, I had to add an exclusion clause. 
Since they aren't true nulls, I had to do where activated != '' instead of not null

-- Query 1
select customer_id, count(*)
from customer_offers
where activated != ''
group by customer_id

Query 2 thought process:
Similar to query 1, I am querying the customer_offers table
First, I interpret a couple of months as 2 months, or 60 days.
Second, I check max(activated), and quickly see that the most recent is `2021-03-25 00:01:04.000` and min is `2021-03-18 01:11:14.000`
This means the window of available data is only in a week window?

Query 3 thought process:
This one continues to build off the last two, and utilizes customer_offers again
Since I am looking for a rate, I will need to do a little math. I will divide the total filled verified columns by activated per customer_id
Multiplying this by 1.0 will get me a floating integer, or rate of completion per customer as a decimal
Here, I adding a `nullif` aggregate was essential, since SQL was still perceiving empty columns as having data in it.

--Query 3
select customer_id, count(nullif(activated, '')), count(nullif(verified, '')),
       ROUND(
       count(nullif(verified, '')) * 1.0 / nullif(count(nullif(activated, '')), 0),
        2
       ) as conversion_rate
from customer_offers
group by customer_id

Query 4 thought process:
This one was a little weird. At first I had a hard time interpreting the question.
Then I figured it must mean, how much money (offer_amount) as each customer redeemed?
To do this, I would have to link two tables (customer_offer_redemptions) and then another one like customer_offers to get this.
However, there is no way to link customer_offer_redemptions to any other table! 
There are also no more than 1 row per id, or customer_offer_id. So this aggregation is more of just verified_redemption_count * offer_amount for each row
