from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connection import connection, Error

app = Flask(__name__)
ma = Marshmallow(app)

# Create the Customer table schema, to define the structure of our data
class CustomerSchema(ma.Schema):
    id = fields.Int(dump_only= True) # dump_only means we don't have to input data for this field
    customer_name = fields.String(required= True) # To be valid, this needs a value
    email = fields.String()
    phone = fields.String()

    class Meta:
        fields = ("customer_name", "email", "phone")

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many= True)


@app.route('/') # default landing page
def home():
    return "Hello, Flask!"

@app.route('/cool') # blahblah.com/cool
def cool():
    return "Whoa this is super awesome! Welcome to the Flask extravaganzaaaaaaaaaaaaaaaaa!!"

# Reads all customer data via a GET request
@app.route("/customers", methods = ['GET'])
def get_customers():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True) # returns us a dictionary of table data instead of a tuple, our schema meta class with cross check the contents of the dictionaries that are returned

            # Write our query to GET all users
            query = "SELECT * FROM customer;"

            cursor.execute(query)

            customers = cursor.fetchall()

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return customers_schema.jsonify(customers)
            

# Create a new customer with a POST request
@app.route("/customers", methods= ["POST"])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.message), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # New customer data
            new_customer = (customer_data["customer_name"], customer_data["email"], customer_data["phone"])

            # query
            query = "INSERT INTO customer (customer_name, email, phone) VALUES (%s, %s, %s)"

            # Execute the query with new_customer data
            cursor.execute(query, new_customer)
            conn.commit()

            return jsonify({'message': 'New customer added successfully!'}), 200
        
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Databse connection failed"}), 500

@app.route("/customers/<int:id>", methods= ["PUT"]) # dynamic route that will change based off of different query parameters
def update_customer(id):
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM customer WHERE id = %s"
            cursor.execute(check_query, (id,))
            customer = cursor.fetchone()
            if not customer:
                return jsonify({"error": "Customer was not found."}), 404
            
            # unpack customer info
            updated_customer = (customer_data['customer_name'], customer_data['email'], customer_data['phone'], id)

            query = "UPDATE customer SET customer_name = %s, email = %s, phone = %s WHERE id = %s"

            cursor.execute(query, updated_customer)
            conn.commit()

            return jsonify({'message': f"Successfully update user {id}"}), 200
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Databse connection failed"}), 500


@app.route("/customers/<int:id>", methods=['DELETE'])
def delete_customer(id):
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM customer WHERE id = %s"
            cursor.execute(check_query, (id,))
            customer = cursor.fetchone()
            if not customer:
                return jsonify({"error": "Customer not found"})
            
            query = "DELETE FROM customer WHERE id = %s"
            cursor.execute(query, (id,))
            conn.commit()

            return jsonify({"message": f"Customer {id} was successfully destroyed!"})
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Databse connection failed"}), 500
    
    

if __name__ == "__main__":
    app.run(debug=True)