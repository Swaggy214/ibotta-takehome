# ibotta-takehome

## Setup Instructions

### Part 1 thought process:
My first step was to set up a new GitHub repository to manage the project efficiently. 
I then reviewed the existing Python code provided to identify gaps and determine which functions I could use versus what I needed to implement myself. 
This is where I added descriptive comments to the existing functions for clarity.

Using the utility functions in db_utils.py, I called them from main.py to accurately populate all four tables in the SQLite database:

  - offer_rewards
  - customer_offers
  - customer_offer_rewards
  - customer_offer_redemptions

### Prerequisites
- Python 3.8 or higher
- Git

### Installation & Setup

1. Clone the repository
```bash
   git clone https://github.com/Swaggy214/ibotta-takehome.git
   cd ibotta-takehome
```

2. Verify project structure
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

3. (Optional) Create virtual environment
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Run the ETL pipeline

    #### Running from the play button
    line 9:
    ```conn = create_connection("../Database/ibotta.db")```
    
    line 14:
    ```csv_folder = Path("../CSV_data")```
    
    
    #### Running from the terminal
    line 9:
    ```conn = create_connection("./Database/ibotta.db")```
    
    line 14:
    ```csv_folder = Path("./CSV_data")```
    
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

5. Verify the database
   The SQLite database will be created at `Database/ibotta.db`
```bash
   sqlite3 Database/ibotta.db "SELECT name FROM sqlite_master WHERE type='table';"
```


## Running SQL Queries
You can run SQL queries on the populated ibotta.db database in one of two ways:

### Option 1 Using your IDE (e.g., PyCharm, VSCode)

1. Open the Database tool window

2. Click + → Data Source → SQLite.

3. Select the database file: database/ibotta.db.

4. Open a SQL Console and run queries directly


### Option 2: Using the provided Python query script

1. Open Python/query.py in your editor.

2. Modify line 8 with the query you want

3. Run the script in the terminal from the project root


## SQL Queries to Run:

### Part 2 thought process:
The next phase was analyzing the data to answer the four questions provided. 
I first set up a query console to verify I could access all four tables. 
Then, I examined each table to understand its columns and relationships. 
Finally, I ensured that another user could query the database from the terminal, in case an IDE was not available.


#### Query 1: Total counts of offer activations per customer
I needed to count distinct customers with a timestamp in the `activated` column.
I selected `customer_id` and used `count(*)` with `group by customer_id`.
To exclude blank values, I added a `where activated != ''` clause, since empty strings are not considered SQL NULL.

#### QUERY 1
```
select customer_id, count(*)
from customer_offers
where activated != ''
group by customer_id
```


#### Query 2: Customers who haven't activated on an offer in last couple months
Similar to query 1, I am querying the `customer_offers` table.
First, I interpreted a couple of months as approximately 60 days.
Second, I examined the `activated` column, and noticed the available data only covers a small window,
`2021-03-18` to `2021-03-25` which limited the results

#### QUERY 2
This query applies a 2-month filter on the activated column. 
This would be appropriate if the dataset included more recent dates. 
This query returns customers who haven't activated an offer in the last 2 months, or ever, which happens to be all of them

```
select customer_id
from customer_offers
group by customer_id
having max(date(activated)) < date('now', '-2 months')
or max(activated) = ''
```


#### Query 3: Conversion rate of activated to completed offers per customer
This query built on the previous analysis, using the `customer_offers` table.
I calculated the conversion rate by dividing the total number of filled verified timestamps by the total number of activated timestamps per customer.
Multiplying by 1.0 ensured the result was a floating-point decimal rather than an integer.
Using NULLIF was essential because empty strings in the database were being interpreted as valid values, which could have skewed the conversion rate.

#### QUERY 3

```
select customer_id, 
       round(
       count(nullif(verified, '')) * 1.0 / nullif(count(nullif(activated, '')), 0), 2) 
       as conversion_rate
from customer_offers
group by customer_id
```


#### Query 4: Total redemption amount per customer
For this query, I needed to calculate the total number of offer redemptions per customer.
To do this, I joined the `customer_offer_redemptions` table to the `customer_offers` table using the `customer_offer_id` field, which links each redemption record to a specific customer.
After establishing that relationship, I used a `SUM` aggregation on the `verified_redemption_count` column and grouped the results by `customer_id`.
This produces the total number of verified redemptions attributed to each customer.

#### QUERY 4

```
select b.customer_id, sum(verified_redemption_count) as total_redemptions
from customer_offer_redemptions a
inner join customer_offers b
    on a.customer_offer_id = b.id
group by b.customer_id
```
