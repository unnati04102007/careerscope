from flask import Blueprint, request, jsonify
from database.models.models import db, College
from sqlalchemy import or_, desc, asc

colleges_bp = Blueprint('colleges_bp', __name__)

@colleges_bp.route('/api/colleges/states', methods=['GET'])
def get_states():
    # Dedicated endpoint for fetching available states
    states = [s[0] for s in db.session.query(College.state).distinct().all() if s[0]]
    states.sort()
    return jsonify({
        "success": True,
        "states": states
    })

@colleges_bp.route('/api/colleges', methods=['GET'])
def get_colleges():
    search = request.args.get('search', '').strip()
    c_type = request.args.get('type', 'All').strip()
    state = request.args.get('state', '').strip()
    sort = request.args.get('sort', 'rating').strip()
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 9, type=int)
    
    query = College.query
    
    if search:
        query = query.filter(or_(
            College.name.ilike(f'%{search}%'),
            College.city.ilike(f'%{search}%'),
            College.description.ilike(f'%{search}%')
        ))
        
    if c_type and c_type.lower() not in ['all', 'undefined', 'null', '']:
        query = query.filter(College.type.ilike(f'%{c_type}%'))
        
    if state and state.lower() not in ['all', 'undefined', 'null', '']:
        query = query.filter(College.state.ilike(f'%{state}%'))
        
    # Sorting logic
    if sort == 'placements':
        query = query.order_by(desc(College.placement_pct))
    elif sort == 'fees':
        query = query.order_by(asc(College.fees))
    elif sort == 'name':
        query = query.order_by(asc(College.name))
    else:  # 'rating' is default
        query = query.order_by(desc(College.rating))
        
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    colleges = pagination.items
    
    college_list = [c.to_dict() for c in colleges]
    
    # Get unique states for the filter dropdown
    states = [s[0] for s in db.session.query(College.state).distinct().all() if s[0]]
    states.sort()
    
    return jsonify({
        "success": True,
        "colleges": college_list,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "available_states": states
    })

@colleges_bp.route('/api/colleges/<int:id>', methods=['GET'])
def get_college(id):
    c = College.query.get(id)
    if not c:
        return jsonify({"success": False, "message": "College not found"}), 404
    return jsonify({
        "success": True,
        "college": c.to_dict()
    })
