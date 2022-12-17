import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, check_password_format

# Configure applicationflash('You were successfully logged in')
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # User's current cash from db
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

    # User's stocks informations from db
    stocks = db.execute("SELECT symbol, name, SUM(shares) as shares, stock_price FROM transactions "\
                        "WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

    # Initial total with user's current cash
    total = user_cash

    for stock in stocks:
        # Update stock's price with current price
        stock['stock_price'] = lookup(stock['symbol'])["price"]
        # Sum each stock's total with total
        total += stock["shares"] * stock['stock_price']

    return render_template("index.html", cash=user_cash, stocks=stocks, total=total, usd_function=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("Please enter stock symbol", 400)

        # Ensure shares number was submitted
        if not request.form.get("shares"):
            return apology("must provide number of shares", 400)

        stock_symbol = request.form.get("symbol")
        num_shares = int(request.form.get("shares"))

        # Check stock symbol does exist
        stock_details = lookup(stock_symbol)
        if not stock_details:
            return apology("Stock Symbol doesn't exist.", 400)

        # Get stock's details from lookup function
        stock_price = stock_details["price"]
        stock_name = stock_details["name"]

        # Check user has enough cash
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

        if user_cash < num_shares * stock_price:
            return apology("You dont have enough cash", 400)

        # Update transactions db with new transaction
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, stock_price) VALUES (?, ?, ?, ?, ?)",
                    session["user_id"], stock_symbol, stock_name, num_shares, stock_price)

        # Update user's cash from users table
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                    user_cash - num_shares * stock_price, session["user_id"])

        flash('Bought!')
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute("SELECT symbol, name, shares, stock_price, date FROM transactions "\
                        "WHERE user_id = ? ORDER BY date DESC", session["user_id"])

    return render_template("history.html", stocks=stocks, usd_function=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("You have been logged in!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("You have been logged out!")
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        stock_symbol = request.form.get("symbol")

        # If lookup function return None, means that symbol doesnt exist
        if not lookup(stock_symbol):
            return apology("Stock Symbol doesn't exist.", 400)

        # Update stock value with usd function from helpers.py
        stock = lookup(stock_symbol)
        stock["price"] = usd(stock["price"])

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password is in correct format
        elif not check_password_format(password):
            return apology("Password should satify these:\n"\
                           "Uppercase characters (A-Z)\nLowercase characters (a-z)\nDigits (0-9)\n"\
                           "Special characters (~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/)", 400)

        # Ensure confirmation password was submitted
        elif not confirmation:
            return apology("must provide confirmation password", 400)

        # Ensure confirmation password and passwords are matched
        if confirmation != password:
            return apology("Passswords are not matched", 400)

        # Ensure username is not in database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 0:
            return apology("Username is already exist", 400)

        # Register user by updating db with user informations
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        flash("You have been registered!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("Please enter stock symbol", 400)

        # Ensure shares number was submitted
        if not request.form.get("shares"):
            return apology("must provide number of shares", 400)

        stock_symbol = request.form.get("symbol")
        num_shares = int(request.form.get("shares"))

        # Check stock symbol does exist
        stock_details = lookup(stock_symbol)
        if not stock_details:
            return apology("Stock Symbol doesn't exist.", 400)

        # Check user has that much share
        transaction_data = db.execute("SELECT SUM(shares) as shares, name FROM transactions WHERE "\
                                      "user_id = ? AND symbol = ?", session["user_id"], stock_symbol)[0]
        total_shares = transaction_data["shares"]
        stock_name = transaction_data["name"]

        if num_shares > total_shares:
            return apology("You dont have %d shares" % num_shares, 400)

        # Get user current cash from db
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

        # Get stock's current price from lookup function
        stock_current_price = stock_details["price"]

        # Update transactions db with new transaction
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, stock_price) VALUES (?, ?, ?, ?, ?)",
                    session["user_id"], stock_symbol, stock_name, -1 * num_shares, stock_current_price)

        # Update user's cash from users table
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   user_cash + num_shares * stock_current_price, session["user_id"])

        flash("Sold!")
        return redirect("/")
    else:
        return render_template("sell.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Ensure old password was submitted
        if not old_password:
            return apology("must provide old password", 400)

        # Ensure password is in correct format
        elif not check_password_format(new_password):
            return apology("Password should satify these:\n"\
                           "Uppercase characters (A-Z)\nLowercase characters (a-z)\nDigits (0-9)\n"\
                           "Special characters (~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/)", 400)

        # Ensure given old password is correct
        old_password_from_db = db.execute("SELECT hash FROM users WHERE id = ?",
                                          session["user_id"])[0]['hash']

        if not check_password_hash(old_password_from_db, old_password):
            return apology("Old password is not correct", 400)

        # Ensure new password was submitted
        elif not new_password:
            return apology("must provide new password", 400)

        # Ensure confirmation password was submitted
        elif not confirmation:
            return apology("must provide confirmation password", 400)

        # Ensure confirmation password and passwords are matched
        if confirmation != new_password:
            return apology("Passswords are not matched", 400)

        # Update user's password on db
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(new_password), session["user_id"])

        flash("Password has been changed!")
        return redirect("/")
    else:
        return render_template("change_password.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "POST":
        cash_amount = int(request.form.get("cash_amount"))

        # Ensure cash amount was submitted
        if not cash_amount:
            return apology("Please enter cash amount", 400)

        # Get current cash from db
        old_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

        # Update user's cash on db
        db.execute("UPDATE users SET cash = ? WHERE id = ?", old_cash + cash_amount, session["user_id"])

        flash("Cash added!")
        return redirect("/")
    else:
        return render_template("add_cash.html")


@app.route("/buy_from_index", methods=["GET", "POST"])
@login_required
def buy_from_index():
    # Ensure share amount was submitted
    if not request.form.get("shares"):
        return apology("Please enter share amount", 400)

    stock_symbol = request.form.get("symbol")
    num_shares = int(request.form.get("shares"))

    # Get stock's details by lookup function
    stock_details = lookup(stock_symbol)
    stock_price = stock_details["price"]
    stock_name = stock_details["name"]

    # Check user has enough cash
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

    if user_cash < num_shares * stock_price:
        return apology("You dont have enough cash", 400)

    # Update transactions db with new transaction
    db.execute("INSERT INTO transactions (user_id, symbol, name, shares, stock_price) VALUES (?, ?, ?, ?, ?)",
               session["user_id"], stock_symbol, stock_name, num_shares, stock_price)

    # Update user's cash from users table
    db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash - num_shares * stock_price, session["user_id"])

    flash("Bought!")
    return redirect("/")


@app.route("/sell_from_index", methods=["GET", "POST"])
@login_required
def sell_from_index():
    # Ensure share amount was submitted
    if not request.form.get("shares"):
        return apology("Please enter share amount", 400)

    stock_symbol = request.form.get("symbol")
    num_shares = int(request.form.get("shares"))

    # Check user has that much share
    transaction_data = db.execute("SELECT SUM(shares) as shares, name FROM transactions WHERE "\
                                  "user_id = ? AND symbol = ?", session["user_id"], stock_symbol)[0]
    total_shares = transaction_data["shares"]
    stock_name = transaction_data["name"]

    if num_shares > total_shares:
        return apology("You dont have %d shares" % num_shares, 400)

    # Get user current cash from db
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

    # Get stock's current price from lookup function
    stock_current_price = lookup(stock_symbol)["price"]

    # Update transactions db with new transaction
    db.execute("INSERT INTO transactions (user_id, symbol, name, shares, stock_price) VALUES (?, ?, ?, ?, ?)",
               session["user_id"], stock_symbol, stock_name, -1 * num_shares, stock_current_price)

    # Update user's cash from users table
    db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash + num_shares * stock_current_price, session["user_id"])

    flash("Sold!")
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
