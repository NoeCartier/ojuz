import sqlite3

db_path = "ojuz.db"

def add_user(user_id, ojuz_pseudo):
    """
    Adds a user to the 'users' table in the database.

    Parameters:
        user_id (int): The Discord ID of the user.
        ojuz_pseudo (str): The OJ.UZ pseudo of the user.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        bool: True if the user was added successfully, False if an error occurred (e.g., duplicate Discord ID).
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (user_id, ojuz_pseudo)
            VALUES (?, ?);
        """, (user_id, ojuz_pseudo))

        conn.commit()
        conn.close()

        print(f"User with Discord ID {user_id} added successfully.")
        return True
    except sqlite3.IntegrityError:
        print(f"Error: A user with Discord ID {user_id} already exists.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def get_user_id_by_ojuz_handle(ojuz_handle):
    """
    Retrieves the user ID from the 'users' table based on their OJ.UZ handle.

    Parameters:
        ojuz_handle (str): The OJ.UZ handle (ojuz_pseudo) of the user to retrieve.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        int: The user ID if found, or None if no matching user is found.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to retrieve the user ID by OJ.UZ handle
        cursor.execute("""
            SELECT user_id
            FROM users
            WHERE ojuz_pseudo = ?;
        """, (ojuz_handle,))

        # Fetch the result
        result = cursor.fetchone()

        # Close the connection
        conn.close()

        # Return the user ID if found, otherwise None
        if result:
            return result[0]
        else:
            print(f"No user found with OJ.UZ handle '{ojuz_handle}'.")
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def list_all_users():
    """
    Retrieves all OJ.UZ handles from the 'users' table in the database.

    Parameters:
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        list: A list of all OJ.UZ handles (ojuz_pseudo) in the database.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to retrieve all OJ.UZ handles
        cursor.execute("""
            SELECT ojuz_pseudo
            FROM users;
        """)

        results = cursor.fetchall()
        conn.close()
        return [row[0] for row in results]
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
   

def add_problem(problem_code, problem_title, problem_priority, 
                problem_proposer=None, 
                problem_link=None):
    """
    Adds a problem to the 'problems' table in the database.

    Parameters:
        problem_code (str): The code of the problem.
        problem_title (str): The title of the problem.
        problem_priority (int): The priority of the problem.
        problem_proposer (int, optional): The proposer of the problem.
        problem_link (str, optional): A link to the problem.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        bool: True if the problem was added successfully, False if an error occurred.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(problem_code, problem_title, problem_priority, problem_proposer, problem_link)
        # Insert the new problem into the 'problems' table
        cursor.execute("""
            INSERT INTO problems (
                problem_code, 
                problem_title, 
                problem_priority, 
                problem_proposer, 
                problem_link
            )
            VALUES (?, ?, ?, ?, ?);
        """, (problem_code, problem_title, problem_priority, 
              problem_proposer, problem_link))

        # Commit changes and close connection
        conn.commit()
        conn.close()

        print(f"Problem '{problem_title}' added successfully.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def get_problem_id_by_code(problem_code):
    """
    Retrieves the ID of a problem from the 'problems' table based on its code.

    Parameters:
        problem_code (str): The code of the problem to retrieve.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        int: The ID of the problem if found, or None if no matching problem is found.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to retrieve the problem ID by code
        cursor.execute("""
            SELECT problem_id
            FROM problems
            WHERE problem_code = ?;
        """, (problem_code,))

        result = cursor.fetchone()
        conn.close()

        # Return the problem ID if found, otherwise None
        if result:
            return result[0]
        else:
            print(f"No problem found with code '{problem_code}'.")
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def update_problem_priority(problem_id, new_priority):
    """
    Updates the priority of a problem in the 'problems' table.

    Parameters:
        problem_id (int): The ID of the problem to update.
        new_priority (int): The new priority value to set.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Mise à jour de la priorité du problème
        cursor.execute("""
            UPDATE problems
            SET problem_priority = ?
            WHERE problem_id = ?;
        """, (new_priority, problem_id))

        # Vérification si une ligne a été modifiée
        if cursor.rowcount == 0:
            print(f"Error: No problem found with ID {problem_id}.")
            conn.close()
            return False

        # Sauvegarde des modifications et fermeture de la connexion
        conn.commit()
        conn.close()

        print(f"Priority of problem ID {problem_id} updated to {new_priority}.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    
def update_problem_proposer(problem_id, new_proposer):
    """
    Updates the proposer of a problem in the 'problems' table.

    Parameters:
        problem_id (int): The ID of the problem to update.
        new_proposer (int): The new proposer ID to set.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Update the proposer of the problem
        cursor.execute("""
            UPDATE problems
            SET problem_proposer = ?
            WHERE problem_id = ?;
        """, (new_proposer, problem_id))

        # Check if any row was updated
        if cursor.rowcount == 0:
            print(f"Error: No problem found with ID {problem_id}.")
            conn.close()
            return False

        conn.commit()
        conn.close()

        print(f"Proposer of problem ID {problem_id} updated to {new_proposer}.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def get_highest_priority_problem():
    """
    Retrieves the problem with the highest priority from the 'problems' table.

    Parameters:
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        list: A list containing the problem details (problem_id, problem_code, problem_title, problem_priority, 
              problem_proposer, problem_link)
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to get the problem with the highest priority
        cursor.execute("""
            SELECT problem_id, problem_code, problem_title, problem_priority, 
                   problem_proposer, problem_link
            FROM problems
            ORDER BY problem_priority DESC
            LIMIT 1;
        """)
        result = cursor.fetchone()
        conn.close()

        # If a result is found, return it as a list
        if result:
            return list(result)
        else:
            print("No problems found in the database.")
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def add_problem_thread(problem_id, thread_id):
    """
    Adds an entry to the 'problem_threads' table in the database.

    Parameters:
        problem_id (int): The ID of the problem.
        thread_id (int): The ID of the thread.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        bool: True if the entry was added successfully, False if an error occurred.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Insert the new entry into the 'problem_threads' table
        cursor.execute("""
            INSERT INTO problem_threads (problem_id, thread_id)
            VALUES (?, ?);
        """, (problem_id, thread_id))

        conn.commit()
        conn.close()

        print(f"Entry with problem ID {problem_id} and thread ID {thread_id} added successfully.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def get_thread_id_of_problem(problem_id):
    """
    Retrieves the thread ID associated with a specific problem ID from the 'problem_threads' table.

    Parameters:
        problem_id (int): The ID of the problem.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        int: The thread ID if found, or None if no matching entry is found.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to retrieve the thread ID for the given problem ID
        cursor.execute("""
            SELECT thread_id
            FROM problem_threads
            WHERE problem_id = ?;
        """, (problem_id,))

        result = cursor.fetchone()
        conn.close()

        # Return the thread ID if found, otherwise None
        if result:
            return result[0]
        else:
            print(f"No thread found for problem ID {problem_id}.")
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def add_submission(submission_id, score, user_id, problem_id):
    """
    Adds a submission to the 'user_problems' table in the database.

    Parameters:
        submission_id (int): The ID of the submission.
        score (int): The score of the submission.
        user_id (int): The ID of the user who made the submission.
        problem_id (int): The ID of the problem.
        submission_time (str): The time of the submission.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        bool: True if the submission was added successfully, False if an error occurred.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Insert the new submission into the 'user_problems' table
        cursor.execute("""
            INSERT INTO user_problems (submission_id, score, user_id, problem_id)
            VALUES (?, ?, ?, ?);
        """, (submission_id, score, user_id, problem_id))

        conn.commit()
        conn.close()

        print(f"Submission with ID {submission_id} added successfully.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def check_best_score_of_user(user_id, problem_id):
    """
    Checks the best score of a user for a specific problem.

    Parameters:
        user_id (int): The ID of the user.
        problem_id (int): The ID of the problem.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        int: The best score of the user for the problem, or None if no submission is found.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to get the best score of the user for the problem
        cursor.execute("""
            SELECT MAX(score)
            FROM user_problems
            WHERE user_id = ? AND problem_id = ?;
        """, (user_id, problem_id))

        result = cursor.fetchone()
        conn.close()

        # Return the best score if found, otherwise None
        if result and result[0] is not None:
            return result[0]
        else:
            print(f"No submissions found for user ID {user_id} and problem ID {problem_id}.")
            return -1.0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def update_variable_value(variable_name, new_value):
    """
    Updates the value of a specific variable in the table.

    Parameters:
        variable_name (str): The name of the variable to update.
        new_value (int): The new value to set for the variable.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Update the value of the variable
        cursor.execute("""
            UPDATE variables
            SET value = ?
            WHERE name = ?;
        """, (new_value, variable_name))

        # Check if any row was updated
        if cursor.rowcount == 0:
            print(f"No variable found with name '{variable_name}'.")
            conn.close()
            return False

        # Commit changes and close connection
        conn.commit()
        conn.close()

        print(f"Variable '{variable_name}' updated successfully to {new_value}.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 
    
import sqlite3

def get_variable_value(variable_name):
    """
    Retrieves the value of a specific variable from the 'variables' table.

    Parameters:
        variable_name (str): The name of the variable to retrieve.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        int: The value of the variable if found, or None if no matching variable is found.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to retrieve the value of the variable
        cursor.execute("""
            SELECT value
            FROM variables
            WHERE name = ?;
        """, (variable_name,))

        result = cursor.fetchone()
        conn.close()

        # Return the value if found, otherwise None
        if result:
            return result[0]  # Extract the value from the tuple
        else:
            print(f"No variable found with name '{variable_name}'.")
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    
def erase_leaderboard():
    """
    Erases all entries in the 'leaderboard' table, effectively resetting the leaderboard.

    Parameters:
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        bool: True if the leaderboard was erased successfully, False if an error occurred.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Delete all entries from the 'leaderboard' table
        cursor.execute("DELETE FROM leaderboard;")

        conn.commit()
        conn.close()

        print("Leaderboard erased successfully.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    
def add_to_leaderboard(user_id, score):
    """
    Adds a user and their score to the 'leaderboard' table in the database.
    If the user already exists in the leaderboard, their score is updated.

    Parameters:
        user_id (int): The ID of the user.
        score (int): The score of the user.
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        bool: True if the operation was successful, False if an error occurred.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if the user already exists in the leaderboard
        cursor.execute("""
            SELECT COUNT(*)
            FROM leaderboard
            WHERE user_id = ?;
        """, (user_id,))
        exists = cursor.fetchone()[0]

        if exists:
            # Update the user's score if they already exist
            cursor.execute("""
                UPDATE leaderboard
                SET score = ?
                WHERE user_id = ?;
            """, (score, user_id))
        else:
            # Insert a new entry if the user does not exist
            cursor.execute("""
                INSERT INTO leaderboard (user_id, score)
                VALUES (?, ?);
            """, (user_id, score))

        conn.commit()
        conn.close()

        print(f"User ID {user_id} added/updated in the leaderboard with score {score}.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    
def get_leaderboard():
    """
    Retrieves the leaderboard from the 'leaderboard' table in the database.

    Parameters:
        db_path (str): Path to the SQLite database file (default is 'ojuz.db').

    Returns:
        list: A list of tuples containing user_id and score, sorted by score in descending order.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to retrieve the leaderboard sorted by score in descending order
        cursor.execute("""
            SELECT user_id, score
            FROM leaderboard
            ORDER BY score DESC;
        """)

        results = cursor.fetchall()
        conn.close()

        return results
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []