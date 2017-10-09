Udacity Fullstack Nanodegree Log Analysis

Author: Meya Gorbea

Report a site's user activity by connecting to a database and using SQL queries to analyze the log data. (Udacity Fullstack Nanodegree)

#### Example output:
![output_log](https://user-images.githubusercontent.com/11435794/31326547-313c096c-ac7d-11e7-92ac-376578efe193.png)

In order to use this program you must set up the database that is used for the queries and then compile the program.

#### Database setup:
 For this project I am using Vagrant, a linux-based virtual machine which gives me the PostgreSQL database.
 You can download Vagrant and bring it online using the command "vagrant up" and log in using "vagrant ssh"
 Next, download the data from this link: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
 The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.
 You'll need to load the site's data into your local database using this command:
 		psql -d news -f newsdata.sql
 -Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.
 Finally, you are ready to run the program.

#### To run:
  "python news.py"

'news.py' Description and Design:
This program connects to a news database using the module psycopg2 in order to output a report of the most popular articles/authors and on which days more than 1% of errors occurred. The program sends the queries in their own functions which are called and printed from the main. For query #3 I used multiple views in order to simplify my end query. I have created (1) a view to hold just the errors (2) a view to hold total requests and (3) a view to get final calculation


1. CREATE VIEW errors AS select date(time), count(status) as num_errrors from log where status like '%4%' or status like '%5%' group by date(time);

2. CREATE VIEW total AS select date(time), count(status) as total from log group by date(time);

3. CREATE VIEW calc AS SELECT num_errrors, e.date, total FROM errors e JOIN total t on e.date = t.date group by t.date, t.total, e.date, e.num_errrors;
