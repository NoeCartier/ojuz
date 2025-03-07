import sqlite3
import db

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect("ojuz.db")
cursor = conn.cursor()

# Création de la table "problems"
cursor.execute("""
CREATE TABLE IF NOT EXISTS problems (
    problem_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Clé primaire avec auto-incrément
    problem_code TEXT NOT NULL UNIQUE,            -- Code du problème (chaîne de caractères)
    problem_title TEXT NOT NULL,                  -- Titre du problème (chaîne de caractères)
    problem_priority INTEGER NOT NULL,            -- Priorité du problème (entier)
    problem_proposer INT,                        -- Proposeur du problème (optionnel)
    problem_link TEXT                             -- Lien vers le problème (optionnel)
);
""")

# Création de la table "users"
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,                 -- Clé primaire avec auto-incrément
    ojuz_pseudo TEXT NOT NULL                    -- Pseudo OJ.UZ (chaîne de caractères)
);
""")

# Création de la table "user_problems"
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- Clé primaire avec auto-incrément
    submission_id INTEGER NOT NULL,             -- ID de la soumission
    score FLOAT NOT NULL,                       -- Score obtenu par l'utilisateur pour un problème
    user_id INTEGER NOT NULL,                -- Clé étrangère vers la table "users"
    problem_id INTEGER NOT NULL,                -- Clé étrangère vers la table "problems"
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (problem_id) REFERENCES problems(problem_id) ON DELETE CASCADE
);
""")

# Création de la table "problem_threads"
cursor.execute("""
CREATE TABLE IF NOT EXISTS problem_threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- Clé primaire avec auto-incrément
    problem_id INTEGER NOT NULL,                -- Clé étrangère vers la table "problems"
    thread_id INTEGER NOT NULL,                 -- ID du thread associé au problème
    FOREIGN KEY (problem_id) REFERENCES problems(problem_id) ON DELETE CASCADE
);
""")

# Création de la table "leaderboard"
cursor.execute("""
CREATE TABLE IF NOT EXISTS leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- Clé primaire avec auto-incrément
    user_id INTEGER NOT NULL,                   -- Clé étrangère vers la table "users"
    score FLOAT NOT NULL,                       -- Score de l'utilisateur
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
""")

# Création de la table "variables"
cursor.execute("CREATE TABLE IF NOT EXISTS variables (name TEXT, value INTEGER)")
cursor.execute("REPLACE INTO variables (name, value) VALUES (?, ?)", ("stop_id", 1163300))
cursor.execute("REPLACE INTO variables (name, value) VALUES (?, ?)", ("potw_problem_id", 1))
cursor.execute("REPLACE INTO variables (name, value) VALUES (?, ?)", ("potw_number", 0))


# Sauvegarde des modifications et fermeture de la connexion
conn.commit()
conn.close()


# Define the file paths
code_file_path = 'statements/problem_code.txt'
title_file_path = 'statements/problem_title.txt'
priority_file_path = 'statements/problem_priority.txt'
proposer_file_path = 'statements/problem_proposer.txt'
link_file_path = 'statements/problem_link.txt'

# Function to read the content of a file and return a list of lines
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return []

problem_codes = read_file(code_file_path)
problem_titles = read_file(title_file_path)
problem_priorities = read_file(priority_file_path)
problem_proposers = read_file(proposer_file_path)
problem_links = read_file(link_file_path)

# Add each problem to the database
for i in range(len(problem_codes)):
    code = problem_codes[i]
    title = problem_titles[i]
    priority = problem_priorities[i]
    proposer = problem_proposers[i]
    link = problem_links[i]
    db.add_problem(code, title, priority, proposer, link)
print("All problems processed.")




print("Base de données et tables créées avec succès.")
