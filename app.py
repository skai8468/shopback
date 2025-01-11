from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pymysql
from pymysql.err import IntegrityError

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session and flash messaging

# Database connection function
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="users"
    )

#################################################################################################################

# Home Route
@app.route("/")
def home():
    return render_template("home.html")  # Create a simple home page

#################################################################################################################

# User Registration Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        highestShopbackPercent = float(request.form["highestShopbackPercent"])
        numberOfVouchersUsed = int(request.form["numberOfVouchersUsed"])
        numberOfFriends = 0
        ranking = int(request.form["ranking"])
        username = request.form["username"]
        password = request.form["password"]

        try:
            db = connect_db()
            mycursor = db.cursor()
            mycursor.execute('''
                INSERT INTO users (name, highestShopbackPercent, numberOfVouchersUsed, numberOfFriends, ranking, username, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (name, highestShopbackPercent, numberOfVouchersUsed, numberOfFriends, ranking, username, password))
            db.commit()
            flash("Registration successful!", "success")
        except IntegrityError:
            flash("Username already exists. Please choose a different one.", "danger")
        finally:
            db.close()

        return redirect(url_for("home"))
    return render_template("register.html")

#################################################################################################################

# User Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    #if "user_id" in session:  # Check if user is already logged in
       #return redirect(url_for("profile"))  # Redirect to profile if logged in
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Authenticate user (same as above)

        # Connect to the database
        db = connect_db()
        cursor = db.cursor()

        # Query to check if the user exists
        cursor.execute(
            "SELECT user_id FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()
        db.close()

        if user:  # If the user exists
            session["user_id"] = user[0]  # Store the user_id in session
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")  # Show error on invalid login
        
    return render_template("login.html")

#################################################################################################################

# Dashboard Route (After Login)
@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        db = connect_db()
        cursor = db.cursor()
        user_id = session["user_id"]
        
        # Query to fetch the user's name
        cursor.execute(
            "SELECT name FROM users WHERE user_id = %s",  
            (user_id,)
        )
        user = cursor.fetchone()
        
        # Handle case where user is not found
        if user is None:
            flash("User not found. Please log in again.", "danger")
            session.pop("user_id", None)  # Clear invalid session
            return redirect(url_for("login"))
        
        # Extract the name from the result
        name = user[0]  # Assuming the query returns a single column
        
        # Query to fetch all deals
        cursor.execute("SELECT * FROM deals")  # Query to fetch all the deals
        deals = cursor.fetchall()
        print(deals)
        
        # Close the database connection
        cursor.close()
        db.close()
        
        # Pass both user name and deals to the template
        return render_template("dashboard.html", user=name, deals=deals)
    else:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("login"))

#################################################################################################################

# Logout Route
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    db.close()
    
    if not user:
        return "User not found"
    
    return render_template("profile.html", user=user)


#################################################################################################################

@app.route("/discover")
def discover():
    db = connect_db()
    cursor = db.cursor()

    # Get the current user's user_id from the session
    current_user_id = session.get("user_id")

    # Query to fetch all user_ids and usernames from the users table
    cursor.execute("SELECT user_id, username FROM users")
    users = cursor.fetchall()

    # Close the database connection
    cursor.close()
    db.close()

    # Exclude the current user's user_id from the list
    filtered_users = [
        {"user_id": user[0], "username": user[1]} for user in users if user[0] != current_user_id
    ]

    # Print the filtered usernames
    print(filtered_users)

    # Pass the filtered list of users (with user_id and username) to the template
    return render_template("discover.html", users=filtered_users)

#################################################################################################################

@app.route("/friendsprofile/<username>")
def friendsprofile(username):
    db = connect_db()
    cursor = db.cursor()
    print(username)
    # Query to fetch user details by username
    cursor.execute("""
        SELECT name, highestShopbackPercent, numberOfVouchersUsed, numberOfFriends, ranking, username
        FROM users WHERE username = %s
    """, (username,))
    user = cursor.fetchone()
    print(user)
    # Close the database connection
    cursor.close()
    db.close()

    if user:
        # Pass user details to the profile template
        return render_template("friendsprofile.html", user=user)
    else:
        return "User not found", 404

#################################################################################################################

@app.route("/add_friend/<username>", methods=["POST"])
def add_friend(username):
    # Get the current logged-in user's ID (from session)
    current_user_id = session.get("user_id")
    
    if not current_user_id:
        return "You need to log in first!", 401  # Return if the user is not logged in

    db = connect_db()
    cursor = db.cursor()

    # Get the current user's ID
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (current_user_id,))
    current_user = cursor.fetchone()
    if not current_user:
        return "Current user not found.", 404
    
    # Get the target friend's ID
    cursor.execute("SELECT user_id, username FROM users WHERE username = %s", (username,))
    friend_user = cursor.fetchone()
    if not friend_user:
        return "Friend user not found.", 404

    # Check if they're already friends
    cursor.execute("""
        SELECT 1 FROM friends 
        WHERE (user_id_1 = %s AND user_id_2 = %s) OR (user_id_1 = %s AND user_id_2 = %s)
    """, (current_user_id, friend_user[0], friend_user[0], current_user_id))
    if cursor.fetchone():
        return "You are already friends!", 400

    # Add the friendship to the table
    cursor.execute("""
        INSERT INTO friends (user_id_1, user_id_2)
        VALUES (%s, %s), (%s, %s)
    """, (current_user_id, friend_user[0], friend_user[0], current_user_id))

    # Update the numberOfFriends for both the current user and the friend
    cursor.execute("""
        UPDATE users 
        SET numberOfFriends = numberOfFriends + 1
        WHERE user_id = %s
    """, (current_user_id,))

    cursor.execute("""
        UPDATE users 
        SET numberOfFriends = numberOfFriends + 1
        WHERE user_id = %s
    """, (friend_user[0],))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('friendsprofile', username=username))  # Redirect to friend's profile

#################################################################################################################

@app.route("/my_friends")
def my_friends():
    # Get the current logged-in user's ID (from session)
    current_user_id = session.get("user_id")
    
    if not current_user_id:
        return "You need to log in first!", 401  # Return if the user is not logged in

    db = connect_db()
    cursor = db.cursor()

    # Get the list of distinct friends for the current user (both user_id_1 and user_id_2 can represent the current user in the friends table)
    cursor.execute("""
        SELECT DISTINCT u.username, u.name
        FROM users u
        JOIN friends f ON u.user_id = f.user_id_1 OR u.user_id = f.user_id_2
        WHERE (f.user_id_1 = %s OR f.user_id_2 = %s) AND u.user_id != %s
    """, (current_user_id, current_user_id, current_user_id))
    
    friends = cursor.fetchall()
    cursor.close()
    db.close()

    # Pass the list of friends to the template
    return render_template("my_friends.html", friends=friends)

#################################################################################################################

@app.route("/remove_friend/<username>", methods=["POST"])
def remove_friend(username):
    # Get the current logged-in user's ID (from session)
    current_user_id = session.get("user_id")
    
    if not current_user_id:
        return "You need to log in first!", 401  # Return if the user is not logged in

    db = connect_db()
    cursor = db.cursor()

    # Get the current user's ID
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (current_user_id,))
    current_user = cursor.fetchone()
    if not current_user:
        return "Current user not found.", 404
    
    # Get the friend's ID
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    friend_user = cursor.fetchone()
    if not friend_user:
        return "Friend user not found.", 404

    # Remove the friendship from the friends table
    cursor.execute("""
        DELETE FROM friends 
        WHERE (user_id_1 = %s AND user_id_2 = %s) OR (user_id_1 = %s AND user_id_2 = %s)
    """, (current_user_id, friend_user[0], friend_user[0], current_user_id))

    # Decrease the numberOfFriends for both users
    cursor.execute("""
        UPDATE users 
        SET numberOfFriends = numberOfFriends - 1
        WHERE user_id = %s
    """, (current_user_id,))

    cursor.execute("""
        UPDATE users 
        SET numberOfFriends = numberOfFriends - 1
        WHERE user_id = %s
    """, (friend_user[0],))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('my_friends'))  # Redirect back to the friends list page

#################################################################################################################

@app.route("/create_group/<int:deal_id>")
def create_group(deal_id):
    db = connect_db()
    cursor = db.cursor()
    deal_id = int(deal_id)
    
    # Create a new group for the deal
    cursor.execute("INSERT INTO `groups` (deal_id) VALUES (%s)", (deal_id,))
    db.commit()
    group_id = cursor.lastrowid
    
    # Generate a unique join link
    join_link = f"{request.host_url}join_group/{group_id}"
    
    cursor.close()
    db.close()
    
    return render_template("dashboard.html", join_link=join_link)

#################################################################################################################

@app.route("/join_group/<int:group_id>", methods=["POST"])
def join_group(group_id):
    if "user_id" not in session:
        flash("Please log in to join the group.", "warning")
        return redirect(url_for("login"))
    
    db = connect_db()
    cursor = db.cursor()
    
    user_id = session["user_id"]
    cursor.execute(
        "INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)",
        (group_id, user_id)
    )
    db.commit()
    
    # Calculate the current discount based on group size
    cursor.execute("SELECT COUNT(*) FROM group_members WHERE group_id = %s", (group_id,))
    group_size = cursor.fetchone()[0]
    
    # Get the base and max discounts
    cursor.execute(
        "SELECT d.base_discount, d.max_discount FROM groups g JOIN deals d ON g.deal_id = d.deal_id WHERE g.group_id = %s",
        (group_id,)
    )
    base_discount, max_discount = cursor.fetchone()
    
    # Calculate the discount as a linear increase
    discount = min(base_discount + (group_size * 5), max_discount)
    
    cursor.close()
    db.close()
    return jsonify({"message": "Joined group successfully!", "current_discount": discount})

#################################################################################################################

@app.route("/browse_store/<int:group_id>")
def browse_store(group_id):
    # Example route for group browsing (mockup)
    return render_template("browse_store.html", group_id=group_id)

#################################################################################################################

@app.route('/leaderboard')
def leaderboard():
    # Get the current logged-in user's ID (from session)
    current_user_id = session.get("user_id")
    # print("Current User ID:", current_user_id)
    if not current_user_id:
        return "You need to log in first!", 401  # Return if the user is not logged in

    db = connect_db()
    cursor = db.cursor()

    # Query to get the leaderboard sorted by ranking, highestShopbackPercentage, numberOfVouchersUsed, and numberOfFriends
    query = """
    SELECT u.user_id, u.name, u.highestShopbackPercent, u.numberOfVouchersUsed, u.numberOfFriends, u.ranking
    FROM users u
    ORDER BY u.numberOfVouchersUsed DESC
    """
    cursor.execute(query)
    leaderboard_data = cursor.fetchall()

    # Query to get the friends of the current user
    cursor.execute("""
        SELECT DISTINCT u.user_id, u.name
        FROM users u
        JOIN friends f ON u.user_id = f.user_id_1 OR u.user_id = f.user_id_2
        WHERE (f.user_id_1 = %s OR f.user_id_2 = %s) AND u.user_id != %s
    """, (current_user_id, current_user_id, current_user_id))
    
    friends = cursor.fetchall()
    print(friends)
    cursor.close()
    db.close()

    # Pass both leaderboard data and friends list to the template
    return render_template('leaderboard.html', leaderboard_data=leaderboard_data, friends=friends)

#################################################################################################################

@app.route("/friends_activity")
def friends_activity():
    current_user_id = session.get("user_id")

    if not current_user_id:
        return "You need to log in first!", 401  # Ensure the user is logged in

    db = connect_db()
    cursor = db.cursor()

    # Query to fetch friends' activity
    query = """
    SELECT u.name AS friend_name, a.store_name, a.voucher_used, a.item_bought, a.date
    FROM users u
    JOIN friends f ON (u.user_id = f.user_id_1 OR u.user_id = f.user_id_2)
    JOIN activities a ON u.user_id = a.user_id
    WHERE (f.user_id_1 = %s OR f.user_id_2 = %s) AND u.user_id != %s
    ORDER BY a.date DESC
    """
    cursor.execute(query, (current_user_id, current_user_id, current_user_id))
    friends_activity = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("friends_activity.html", friends_activity=friends_activity)

#################################################################################################################

def auto_update_vouchers(user_id, purchase_id):
    db = connect_db()
    try:
        with db.cursor() as cursor:
            # Fetch the user
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                raise ValueError(f"User with ID {user_id} not found.")
            
            # Fetch the purchase record
            cursor.execute("SELECT * FROM user_store_purchases WHERE id = %s", (purchase_id,))
            purchase = cursor.fetchone()
            if not purchase:
                raise ValueError(f"Purchase record with ID {purchase_id} not found.")
            
            # Calculate store-specific vouchers
            store_1_vouchers = purchase['store_1'] // 5
            store_2_vouchers = purchase['store_2'] // 5
            store_3_vouchers = purchase['store_3'] // 5

            # Deduct used stamps for each store
            new_store_1 = purchase['store_1'] - store_1_vouchers * 5
            new_store_2 = purchase['store_2'] - store_2_vouchers * 5
            new_store_3 = purchase['store_3'] - store_3_vouchers * 5

            cursor.execute("""
                UPDATE user_store_purchases 
                SET store_1 = %s, store_2 = %s, store_3 = %s 
                WHERE id = %s
            """, (new_store_1, new_store_2, new_store_3, purchase_id))
            
            # Calculate general vouchers
            shopback_vouchers = user['general_stamps'] // 10
            new_general_stamps = user['general_stamps'] - shopback_vouchers * 10

            cursor.execute("""
                UPDATE users 
                SET general_stamps = %s 
                WHERE id = %s
            """, (new_general_stamps, user_id))
            
            # Fetch or create a discount record
            cursor.execute("""
                SELECT * FROM discounts 
                WHERE user_store_purchase_id = %s
            """, (purchase_id,))
            discount = cursor.fetchone()

            if not discount:
                # Create a new discount record
                cursor.execute("""
                    INSERT INTO discounts (user_id, user_store_purchase_id, shopback_VoucherQty, store_1_VoucherQty, store_2_VoucherQty, store_3_VoucherQty)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, purchase_id, shopback_vouchers, store_1_vouchers, store_2_vouchers, store_3_vouchers))
            else:
                # Update the existing discount record
                cursor.execute("""
                    UPDATE discounts 
                    SET shopback_VoucherQty = shopback_VoucherQty + %s, 
                        store_1_VoucherQty = store_1_VoucherQty + %s, 
                        store_2_VoucherQty = store_2_VoucherQty + %s, 
                        store_3_VoucherQty = store_3_VoucherQty + %s 
                    WHERE user_store_purchase_id = %s
                """, (shopback_vouchers, store_1_vouchers, store_2_vouchers, store_3_vouchers, purchase_id))
            
            # Commit the transaction
            db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error updating vouchers for user_id {user_id} and purchase_id {purchase_id}: {e}")
    finally:
        db.close()

###########################################################################################################

def create_stampcard_display(user_id):
    db = connect_db()
    try:
        with db.cursor() as cursor:
            # Fetch the user record
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return {"error": "User not found."}

            # Fetch the user's purchase record
            cursor.execute("SELECT * FROM user_store_purchases WHERE user_id = %s", (user_id,))
            purchase = cursor.fetchone()
            if not purchase:
                return {"error": "Purchase record not found."}

            # Return the stamp counts for each store
            return {
                "store_1": purchase['store_1'],
                "store_2": purchase['store_2'],
                "store_3": purchase['store_3'],
                "Shopback": user['numberOfVouchersUsed']
            }

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

    finally:
        db.close()

###########################################################################################################

'''@app.route('/home')
def home():
    return render_template("homepage.html")'''

###########################################################################################################

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if request.method == 'GET':
        # Render the payment form template
        return render_template("payment.html")

    elif request.method == 'POST':
        # Get selected users and stores from the form
        selected_users = 'user1'  # Example user_id for demo purposes
        selected_stores = request.form.getlist('store')  # List of selected stores

        # Validate input to ensure only one user and one store are selected
        if len(selected_stores) != 1:
            return render_template("payment.html", error="Please select exactly one store.")

        # Extract the single user and store from the lists
        user_id = selected_users
        store_id = selected_stores[0]

        db = connect_db()
        try:
            with db.cursor() as cursor:
                # Fetch the user record
                cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()

                # Fetch the purchase record
                cursor.execute("SELECT * FROM user_store_purchases WHERE user_id = %s", (user['id'],))
                purchase = cursor.fetchone()

                if not user or not purchase:
                    return render_template("payment.html", error="User or purchase record not found.")

                # Increment stamps for the selected store
                if store_id == 'store_1':
                    purchase['store_1'] += 1
                    cursor.execute("UPDATE user_store_purchases SET store_1 = %s WHERE id = %s", (purchase['store_1'], purchase['id']))
                elif store_id == 'store_2':
                    purchase['store_2'] += 1
                    cursor.execute("UPDATE user_store_purchases SET store_2 = %s WHERE id = %s", (purchase['store_2'], purchase['id']))
                elif store_id == 'store_3':
                    purchase['store_3'] += 1
                    cursor.execute("UPDATE user_store_purchases SET store_3 = %s WHERE id = %s", (purchase['store_3'], purchase['id']))

                # Increment general stamps for the user
                user['numberOfVouchersUsed'] += 1
                cursor.execute("UPDATE users SET numberOfVouchersUsed = %s WHERE id = %s", (user['numberOfVouchersUsed'], user['id']))

                # Commit the transaction
                db.commit()

                # Automatically update vouchers after purchase
                auto_update_vouchers(user['id'], purchase['id'])

                return render_template("payment.html", success=f"Purchase successful! Stamps and vouchers updated for User {user_id} at {store_id}.")

        except Exception as e:
            db.rollback()
            return render_template("payment.html", error=f"An error occurred: {str(e)}")

        finally:
            db.close()

###########################################################################################################

@app.route('/stampcard')
def stampcard():
    selected_users = session.get("user_id")  # Use session.get to avoid KeyError if "user_id" is not set.

    if not selected_users:
        return render_template("stampcard.html", stamps="User not found or not logged in.")

    # Connect to the database
    db = connect_db()
    try:
        with db.cursor() as cursor:
            # Fetch user details
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (selected_users,))
            user = cursor.fetchone()

            if not user:
                return render_template("stampcard.html", stamps="User not found.")

            # Fetch purchase details
            cursor.execute("SELECT * FROM user_store_purchases WHERE user_id = %s", (user[0],))
            print(user[3])
            purchase = cursor.fetchone()

            if not purchase:
                return render_template("stampcard.html", stamps="Purchase record not found.")

            # Prepare the stamp card data
            stamp_data = {
                "store_1": purchase[2],  # Use .get to avoid KeyError if the field doesn't exist
                "store_2": purchase[3],
                "store_3": purchase[4],
                "Shopback": user[3]  # Default to 0 if the field is missing
            }
            print(stamp_data)
            return render_template("stampcard.html", stamps=stamp_data)

    except Exception as e:
        return render_template("stampcard.html", stamps=f"An error occurred: {str(e)}")

    finally:
        db.close()  # Ensure the database connection is closed


###########################################################################################################

@app.route('/add_sample_users', methods=['POST'])
def add_sample_users():
    # Sample data for three users
    sample_users = [
        {
            "user_id": "user1",
            "general_stamps": 10,
            "store_1": 3,
            "store_2": 4,
            "store_3": 3
        },
        {
            "user_id": "user2",
            "general_stamps": 15,
            "store_1": 5,
            "store_2": 5,
            "store_3": 5
        },
        {
            "user_id": "user3",
            "general_stamps": 20,
            "store_1": 8,
            "store_2": 6,
            "store_3": 6
        }
    ]

    db = connect_db()  # Establish database connection
    try:
        with db.cursor() as cursor:
            for user_data in sample_users:
                # Insert into users table
                cursor.execute(
                    "INSERT INTO users (user_id, general_stamps) VALUES (%s, %s)",
                    (user_data["user_id"], user_data["general_stamps"])
                )
                user_id = cursor.lastrowid  # Get the auto-generated user ID

                # Insert into user_store_purchases table
                cursor.execute(
                    """
                    INSERT INTO user_store_purchases (user_id, store_1, store_2, store_3)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user_id, user_data["store_1"], user_data["store_2"], user_data["store_3"])
                )

        # Commit all changes to the database
        db.commit()
        return jsonify({"message": "Sample users added successfully!"}), 201

    except Exception as e:
        db.rollback()  # Roll back the transaction in case of an error
        return jsonify({"error": str(e)}), 400

    finally:
        db.close()  # Ensure the database connection is closed

###########################################################################################################

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/dashboardnew')
def dashboardnew():
    return render_template('dashboardnew.html')

@app.route('/GroupBuy')
def GroupBuy():
    return render_template('GroupBuy.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/social')
def social():
    return render_template('social.html')

# Run the App
if __name__ == "__main__":
    app.run(debug=True)
