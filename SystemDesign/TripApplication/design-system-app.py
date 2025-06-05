"""
Trip Sharing Application API

This Flask application provides a backend for a trip sharing platform.
Users can create (implicitly, not via API in this version), list, and share travel routes.

Key Components:
- Flask: Micro web framework for building the API.
- SQLAlchemy: ORM (Object Relational Mapper) for database interactions.
- SQLite: Lightweight disk-based database (`travel_routes.db`) for storing user,
          route, and sharing information.

Features Overview:
- List routes with pagination, optionally filtered by user.
- Share a specific route with another user.
- List routes that have been shared with a specific user, with pagination.

Database Models:
- User: Represents a user of the application.
- Route: Represents a travel route created by a user.
- RouteShare: Represents the sharing link between a route and a user it's shared with.

Note: User creation and authentication are not implemented in this example.
It's assumed users exist in the database for demonstration of sharing features.
"""
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_routes.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    """
    Represents a user in the application.
    Each user can own multiple travel routes.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    routes = db.relationship('Route', backref='user', lazy=True)

class Route(db.Model):
    """
    Represents a travel route created by a user.
    Routes have a title, description, creation timestamp, and an owner (user).
    They can be shared with other users via the RouteShare model.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # The user who created the route
    shared_with = db.relationship('RouteShare', backref='route', lazy=True)

class RouteShare(db.Model):
    """
    Represents the sharing relationship between a Route and a User.
    This table links a route to a user with whom it has been shared.
    """
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# API Endpoints
@app.route('/api/routes', methods=['GET'])
def get_routes():
    """
    Fetches a paginated list of travel routes.
    Can be filtered by user_id.

    Query Parameters:
        page (int, optional): The page number for pagination. Defaults to 1.
        per_page (int, optional): The number of items per page. Defaults to 10.
        user_id (int, optional): If provided, filters routes by this user ID (owner).

    Returns:
        JSON: A JSON object containing:
            - 'routes': A list of route objects.
            - 'total': Total number of routes matching the query.
            - 'pages': Total number of pages.
            - 'current_page': The current page number.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    user_id = request.args.get('user_id', type=int)
    
    query = Route.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    # Equivalent SQL:
    # SELECT * FROM route
    # WHERE user_id = :user_id  -- (if user_id filter is applied)
    # ORDER BY created_at DESC 
    # LIMIT :per_page
    # OFFSET (:page - 1) * :per_page
    routes = query.order_by(Route.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'routes': [{
            'id': route.id,
            'title': route.title,
            'description': route.description,
            'created_at': route.created_at.isoformat(),
            'user_id': route.user_id
        } for route in routes.items],
        'total': routes.total,
        'pages': routes.pages,
        'current_page': routes.page
    })

@app.route('/api/routes/<int:route_id>/share', methods=['POST'])
def share_route(route_id):
    """
    Shares a specific route with another user.

    Path Parameter:
        route_id (int): The ID of the route to be shared.

    Request Body (JSON):
        user_id (int): The ID of the user with whom the route should be shared.

    Returns:
        JSON: A success message if sharing is successful (201).
              An error message if the route or user is not found, if 'user_id'
              is missing in the request (400), or if the route is already
              shared with the user (400).
    """
    shared_with_user_id = request.json.get('user_id')
    
    if not shared_with_user_id:
        return jsonify({'error': 'User ID is required'}), 400
        
    route = Route.query.get_or_404(route_id)
    
    # Check if already shared
    existing_share = RouteShare.query.filter_by(
        route_id=route_id,
        shared_with_user_id=shared_with_user_id
    ).first()
    
    if existing_share:
        return jsonify({'error': 'Route already shared with this user'}), 400
        
    share = RouteShare(route_id=route_id, shared_with_user_id=shared_with_user_id)
    db.session.add(share)
    db.session.commit()
    
    return jsonify({'message': 'Route shared successfully'}), 201

@app.route('/api/routes/shared-with-me', methods=['GET'])
def get_shared_routes():
    """
    Fetches a paginated list of routes that have been shared with a specific user.

    Query Parameters:
        page (int, optional): The page number for pagination. Defaults to 1.
        per_page (int, optional): The number of items per page. Defaults to 10.
        user_id (int, required): The ID of the user for whom to retrieve shared routes.

    Returns:
        JSON: A JSON object containing:
            - 'routes': A list of route objects shared with the user.
                        Each route includes 'shared_by' indicating the owner's user ID.
            - 'total': Total number of routes shared with the user.
            - 'pages': Total number of pages.
            - 'current_page': The current page number.
              An error message if 'user_id' is missing (400).
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
        
    shared_routes = db.session.query(Route)\
        .join(RouteShare)\
        .filter(RouteShare.shared_with_user_id == user_id)\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'routes': [{
            'id': route.id,
            'title': route.title,
            'description': route.description,
            'created_at': route.created_at.isoformat(),
            'shared_by': route.user_id
        } for route in shared_routes.items],
        'total': shared_routes.total,
        'pages': shared_routes.pages,
        'current_page': shared_routes.page
    })

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
