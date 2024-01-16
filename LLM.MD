# More detail of any AI tool used, including the name, URL, all the input given and all the output received.  

Agent used: ChatGPT
URL: https://chat.openai.com/

Agent: ChatGPT
Steps:
	Thought: Need a way to verify the registration inputs for name, email, city, timezone, and password. Make sure that all user inputs are valid and prompt them again if it is invalid. 
	Input: 
    
    def register_user():
    name_prompt = input("Please enter your name: ")
    email_prompt = input("Please enter your email: ")
    city_prompt = input("Please enter your city: ")
    time_zone_prompt = input("Please enter your timezone: ")
    pass_prompt = input("Please create your password: ")

    cursor.execute('SELECT COUNT(usr) FROM users')
    user_count = cursor.fetchone()[0]
    next_user_id = user_count + 1
    unique_usr = next_user_id

    cursor.execute('INSERT INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?)',
                   (unique_usr, str(pass_prompt), str(name_prompt), str(email_prompt), str(city_prompt), float(time_zone_prompt)))
    
    connection.commit()
    print("Registration successful.")

	can you revise def register_user() to check for invalid inputs?


Output: 
	import re

	def register_user():
    	print("User Registration:")
    
    # Validate and input user name
    while True:
        name_prompt = input("Please enter your name: ")
        if re.match(r"^[A-Za-z\s]+$", name_prompt):
            break
        else:
            print("Invalid name. Please use only letters and spaces.")
    
    # Validate and input user email
    while True:
        email_prompt = input("Please enter your email: ")
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_prompt):
            break
        else:
            print("Invalid email address. Please use a valid email format.")
    
    # Input user city
    city_prompt = input("Please enter your city: ")
    
    # Validate and input user timezone
    while True:
        time_zone_prompt = input("Please enter your timezone (e.g., -7.0 or 3.5): ")
        try:
            time_zone = float(time_zone_prompt)
            break
        except ValueError:
            print("Invalid timezone. Please enter a numeric value.")
    
    # Input user password
    pass_prompt = input("Please create your password: ")
    
    # Generate a unique user ID
    cursor.execute('SELECT COUNT(usr) FROM users')
    user_count = cursor.fetchone()[0]
    next_user_id = user_count + 1
    unique_usr = next_user_id
    
    # Insert user information into the database
    cursor.execute('INSERT INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?)',
                   (unique_usr, str(pass_prompt), name_prompt, email_prompt, city_prompt, time_zone))
    
    connection.commit()
    print("Registration successful.")

	Observation: Using the re library to verify if the correct characters are being used for the various inputs.


Agent: Chat GPT
Steps:
	Thought: The initial step for show tweets. Find the 5 tweets from users being followed by the current user order by date 
	Input: Can you give me a function to display 5 tweets from users being followed by current user? Write in sqlite3. 
Output:
	
 	def show_tweets(user_id):
    cursor.execute('''
        SELECT t.id, t.tweet_text, t.tweet_date, u.name
        FROM tweets t
        JOIN users u ON t.user_id = u.id
        WHERE t.user_id IN (SELECT followed_id FROM users_following WHERE follower_id = ?)
        ORDER BY t.tweet_date DESC
        LIMIT 5
    ''', (user_id,))
    tweets = cursor.fetchall()

    for tweet in tweets:
        print(f"{tweet[3]} tweeted on {tweet[2]}:\n{tweet[1]}\n")
	Observation: Some discrepancies from the syntax of the query, followed_id should be flwee, users_following should be follows, follower_id should be flwer for example

	Thought: Manuel changes to the query to fit the tables given for the project:
	Manuel Changes: 
	cursor.execute('''
            SELECT t.tid, t.text, t.tdate, u.name
            FROM tweets t
            JOIN users u ON t.writer = u.usr
            WHERE t.writer IN (SELECT flwee FROM follows WHERE flwer = ?)
            ORDER BY t.tdate DESC
            LIMIT 5
        ''', (user_id,))


Agent: Chat GPT
Steps:
	Thought: expand the function show_tweets that an option should be given to the user that they can see more tweets but 5 at a time, the user should be able to select tweet, see retweets, and number of replies. User should be able to reply to it or retweet it. 

Input: 
	
 	Given: 
	users_query=   '''
                        CREATE TABLE users (
                                usr         INTEGER,
                                pwd	        TEXT,
                                name        TEXT,
                                email       TEXT,
                                city        TEXT,
                                timezone    FLOAT,
                                PRIMARY KEY (usr)
                            );
                    '''

    follows_query=  '''
                        CREATE TABLE follows (
                                flwer       INTEGER,
                                flwee       INTEGER,
                                start_date  DATE,
                                PRIMARY KEY (flwer,flwee),
                                FOREIGN KEY (flwer) REFERENCES users,
                                FOREIGN KEY (flwee) REFERENCES users
                                );
                    '''

    tweets_query= '''
                        CREATE TABLE tweets (
                                tid	        INTEGER,
                                writer      INTEGER,
                                tdate       DATE,
                                text        TEXT,
                                replyto     INTEGER,
                                PRIMARY KEY (tid),
                                FOREIGN KEY (writer) REFERENCES users,
                                FOREIGN KEY (replyto) REFERENCES tweets
                            );
                    '''
    
Can you expand that function that after a registered user signs in, the system should list all tweets or retweets from users who are being followed; the tweets should be ordered based on date from the latest to the oldest. If there are more than 5 such tweets, only 5 would be shown and the user would be given an option to see more but again 5 at a time. The user should be able to select a tweet and see some statistics about the tweet including the number of retweets and the number of replies. Also the user should be able to compose a reply to it (see the section on composing a tweet), or retweet it (i.e. repost it to all people who follow the user).

Output:
	
 	def view_tweets_and_interact(user_id):
    while True:
        # Fetch the latest 5 tweets or retweets from users being followed
        cursor.execute('''
            SELECT t.tid, t.text, t.tdate, u.name
            FROM tweets t
            JOIN users u ON t.writer = u.usr
            WHERE t.writer IN (SELECT flwee FROM follows WHERE flwer = ?)
            ORDER BY t.tdate DESC
            LIMIT 5
        ''', (user_id,))
        tweets = cursor.fetchall()

        if not tweets:
            print("No tweets from users you follow.")
            break

        print("Latest tweets from users you follow:")
        for idx, tweet in enumerate(tweets, start=1):
            print(f"{idx}. {tweet[3]} tweeted on {tweet[2]}:\n{tweet[1]}\n")

        tweet_choice = input("Enter the number of the tweet you want to interact with (or 'more' to see more, or 'exit'): ")

        if tweet_choice.lower() == 'exit':
            break
        elif tweet_choice.lower() == 'more':
            continue
        elif tweet_choice.isdigit():
            tweet_idx = int(tweet_choice) - 1
            if 0 <= tweet_idx < len(tweets):
                selected_tweet = tweets[tweet_idx]
                tweet_id = selected_tweet[0]

                # Display statistics about the selected tweet
                cursor.execute('''
                    SELECT COUNT(*) FROM retweets WHERE tid = ?
                ''', (tweet_id,))
                retweet_count = cursor.fetchone()[0]

                cursor.execute('''
                    SELECT COUNT(*) FROM tweets WHERE replyto = ?
                ''', (tweet_id,))
                reply_count = cursor.fetchone()[0]

                print(f"Tweet by {selected_tweet[3]} on {selected_tweet[2]}:\n{selected_tweet[1]}")
                print(f"Retweets: {retweet_count} | Replies: {reply_count}")

                # Allow the user to compose a reply or retweet
                interaction_choice = input("Enter 'reply' to compose a reply, 'retweet' to retweet, or 'back' to return: ")

                if interaction_choice.lower() == 'reply':
                    reply_text = input("Enter your reply: ")
                    # Insert the reply into the database with appropriate details
                    cursor.execute('''
                        INSERT INTO tweets (writer, tdate, text, replyto)
                        VALUES (?, DATE('now'), ?, ?)
                    ''', (user_id, reply_text, tweet_id))
                    connection.commit()
                    print("Reply posted successfully!")

                elif interaction_choice.lower() == 'retweet':
                    # Insert the retweet into the database
                    cursor.execute('''
                        INSERT INTO retweets (usr, tid, rdate)
                        VALUES (?, ?, DATE('now'))
                    ''', (user_id, tweet_id))
                    connection.commit()
                    print("Retweet posted successfully!")

            else:
                print("Invalid tweet number.")
        else:
            print("Invalid input. Please enter 'more', 'exit', or a valid tweet number.")

# Usage:
# Provide the user_id of the logged-in user when calling this function.
# Example: view_tweets_and_interact(97)

 Observation: All functionalities seem to be working, any incorrect variables will be able to be adjusted.
