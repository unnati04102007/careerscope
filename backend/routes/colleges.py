from flask import Blueprint, jsonify, request
from backend.utils.data_loader import load_colleges_data

colleges_bp = Blueprint('colleges', __name__)

# Load data once (for simplicity in this scale)
# ideally we might cache this or reload periodicallly
COLLEGES_DATA = load_colleges_data()

@colleges_bp.route('/api/colleges', methods=['GET'])
def get_colleges():
    """
    Fetch colleges with filtering and sorting.
    """
    try:
        # Get query parameters
        search_query = request.args.get('search', '').lower()
        state_filter = request.args.get('state', '')
        rating_min = request.args.get('rating', 0, type=float)
        sort_by = request.args.get('sort', '')
        limit = request.args.get('limit', 20, type=int)
        page = request.args.get('page', 1, type=int)

        # Start with all data
        results = COLLEGES_DATA

        # 1. Filter by Search (Name)
        if search_query:
            results = [c for c in results if search_query in str(c.get('College_Name', '')).lower()]

        # 2. Filter by State
        if state_filter:
            results = [c for c in results if state_filter.lower() == str(c.get('State', '')).lower()]

        # 3. Filter by Rating
        if rating_min > 0:
            results = [c for c in results if float(c.get('Rating', 0)) >= rating_min]

        # 4. Sorting
        if sort_by == 'rating_desc':
            results.sort(key=lambda x: float(x.get('Rating', 0)), reverse=True)
        elif sort_by == 'fees_asc':
            results.sort(key=lambda x: int(x.get('UG_fee', 0)))
        elif sort_by == 'placement_desc':
            results.sort(key=lambda x: float(x.get('Placement', 0)), reverse=True)

        # 5. Pagination
        total_count = len(results)
        start = (page - 1) * limit
        end = start + limit
        paginated_results = results[start:end]

        return jsonify({
            'colleges': paginated_results,
            'total': total_count,
            'page': page,
            'limit': limit
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@colleges_bp.route('/api/states', methods=['GET'])
def get_states():
    """
    Get unique list of states for the filter dropdown.
    """
    try:
        states = sorted(list(set(str(c.get('State', '')).strip().title() for c in COLLEGES_DATA if c.get('State'))))
        return jsonify({'states': states})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
