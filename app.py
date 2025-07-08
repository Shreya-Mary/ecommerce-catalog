from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from service.auth_service import AuthService
from service.catalog_service import CatalogService
from dto.catalog import Catalog
from util.logger import logger
from flasgger import Swagger

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your-secret-key"

jwt = JWTManager(app)
CORS(app)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "E-Commerce Catalog API",
        "description": "API documentation for the Catalog Management System",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: Bearer {token}"
        }
    }
}
swagger = Swagger(app, template=swagger_template)

@app.route('/')
def login_page():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    """
    User Login
    ---
    tags:
      - Authentication
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              password:
                type: string
    responses:
      200:
        description: Login successful
        content:
          application/json:
            schema:
              type: object
              properties:
                token:
                  type: string
      401:
        description: Invalid credentials
      500:
        description: Internal server error
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    logger.info(f"Login attempt by user: {username}")
    try:
        auth_service = AuthService()
        user = auth_service.authenticate(username, password)

        if user:
            token = create_access_token(identity=username)
            logger.info(f"Login successful for user: {username}")
            return jsonify({"token": token})
        else:
            logger.warning(f"Invalid login credentials for user: {username}")
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/home')
def home_page():
    return render_template("home.html")


@app.route('/catalogs', methods=['GET'])
@jwt_required()
def get_all_catalogs():
    """
    Get All Catalogs
    ---
    tags:
      - Catalog
    parameters:
      - name: status
        in: query
        type: string
        required: false
      - name: sort_by
        in: query
        type: string
        required: false
        default: start_date
      - name: page
        in: query
        type: integer
        default: 1
      - name: size
        in: query
        type: integer
        default: 5
      - name: search
        in: query
        type: string
        required: false
    responses:
      200:
        description: Catalog list
      500:
        description: Failed to fetch catalogs
    """
    try:
        status = request.args.get("status")
        sort_by = request.args.get("sort_by", "start_date")
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 5))
        search = request.args.get("search")

        service = CatalogService()
        result, total = service.get_all_catalogs(status, sort_by, page, size, search)

        logger.info(f"Catalogs fetched. Count: {len(result)} Page: {page}")
        return jsonify({
            "data": result,
            "total_count": total,
            "message": "Catalogs fetched successfully"
        })
    except Exception as e:
        logger.error(f"Error fetching catalogs: {str(e)}")
        return jsonify({"message": "Failed to fetch catalogs"}), 500


@app.route('/catalogs', methods=['POST'])
@jwt_required()
def create_catalog():
    """
    Create Catalog
    ---
    tags:
      - Catalog
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              description:
                type: string
              start_date:
                type: string
              end_date:
                type: string
              status:
                type: string
    responses:
      200:
        description: Catalog created successfully
      500:
        description: Failed to create catalog
    """
    try:
        data = request.json
        catalog = Catalog(
            catalog_name=data['name'],
            catalog_description=data['description'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            status=data.get('status', 'Active')
        )
        service = CatalogService()
        created = service.create_catalog(catalog)

        logger.info(f"Catalog created: {created}")
        return jsonify({
            "status": "success",
            "message": "Catalog created successfully",
            "catalog": created
        })
    except Exception as e:
        logger.error(f"Error creating catalog: {str(e)}")
        return jsonify({"message": "Failed to create catalog"}), 500


@app.route('/catalogs/<int:catalog_id>', methods=['PUT'])
@jwt_required()
def update_catalog(catalog_id):
    """
    Update Catalog
    ---
    tags:
      - Catalog
    parameters:
      - name: catalog_id
        in: path
        type: integer
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              description:
                type: string
              start_date:
                type: string
              end_date:
                type: string
              status:
                type: string
    responses:
      200:
        description: Catalog updated
      500:
        description: Failed to update
    """
    try:
        data = request.json
        service = CatalogService()
        result = service.update_catalog_by_id(
            catalog_id,
            name=data['name'],
            description=data['description'],
            start_date=data['start_date'].replace('T', ' '),
            end_date=data['end_date'].replace('T', ' '),
            status=data['status']
        )
        logger.info(f"Catalog updated: ID {catalog_id}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error updating catalog ID {catalog_id}: {str(e)}")
        return jsonify({"message": "Failed to update catalog"}), 500


@app.route('/catalogs/<int:catalog_id>', methods=['DELETE'])
@jwt_required()
def delete_catalog(catalog_id):
    """
    Delete Catalog
    ---
    tags:
      - Catalog
    parameters:
      - name: catalog_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Catalog deleted
      500:
        description: Failed to delete
    """
    try:
        service = CatalogService()
        result = service.delete_catalog_by_id(catalog_id)
        logger.info(f"Catalog deleted: ID {catalog_id}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error deleting catalog ID {catalog_id}: {str(e)}")
        return jsonify({"message": "Failed to delete catalog"}), 500


if __name__ == '__main__':
    app.run(debug=True)
