from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_routes.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    routes = db.relationship('Route', backref='user', lazy=True)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_with = db.relationship('RouteShare', backref='route', lazy=True)

class RouteShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# API Endpoints
@app.route('/api/routes', methods=['GET'])
def get_routes():
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
