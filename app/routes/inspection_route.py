from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.inspection import Inspection
from app import db
import logging

inspection_bp = Blueprint('inspection', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@inspection_bp.route('/inspection', methods=['POST'])
@jwt_required()
def create_inspection():
    """Create a new inspection entry"""
    try:
        current_user_id = get_jwt_identity()
        logger.info(f"User {current_user_id} creating new inspection")
        
        data = request.get_json()
        
        if not data or not data.get('vehicle_number') or not data.get('damage_report'):
            logger.warning("Inspection creation failed: Missing required fields")
            return jsonify({'message': 'Vehicle number and damage report are required'}), 400
        
        image_url = data.get('image_url')
        if image_url and not Inspection.validate_image_url(image_url):
            logger.warning(f"Inspection creation failed: Invalid image URL format: {image_url}")
            return jsonify({'message': 'Image URL must end with .jpg, .jpeg, or .png'}), 400
        
        new_inspection = Inspection(
            vehicle_number=data['vehicle_number'],
            inspected_by=current_user_id,
            damage_report=data['damage_report'],
            image_url=image_url,
            status='pending'
        )
        
        db.session.add(new_inspection)
        db.session.commit()
        
        logger.info(f"Inspection created successfully with ID: {new_inspection.id}")
        return jsonify({
            'message': 'Inspection created successfully',
            'inspection': new_inspection.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Database error during inspection creation: {str(e)}")
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500

@inspection_bp.route('/inspection/<int:inspection_id>', methods=['GET'])
@jwt_required()
def get_inspection(inspection_id):
    """Fetch inspection details (only if created by the logged-in user)"""
    try:
        current_user_id = get_jwt_identity()
        logger.info(f"User {current_user_id} requesting inspection {inspection_id}")
        
        inspection = Inspection.query.get(inspection_id)
        
        if not inspection:
            logger.warning(f"Inspection {inspection_id} not found")
            return jsonify({'message': 'Inspection not found'}), 404
        
        if inspection.inspected_by != current_user_id:
            logger.warning(f"User {current_user_id} unauthorized to access inspection {inspection_id}")
            return jsonify({'message': 'Unauthorized access to inspection'}), 403
        
        logger.info(f"Inspection {inspection_id} retrieved successfully")
        return jsonify({'inspection': inspection.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Database error during inspection retrieval: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@inspection_bp.route('/inspection/<int:inspection_id>', methods=['PATCH'])
@jwt_required()
def update_inspection(inspection_id):
    """Update the status to reviewed or completed"""
    try:
        current_user_id = get_jwt_identity()
        logger.info(f"User {current_user_id} updating inspection {inspection_id}")
        
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        inspection = Inspection.query.get(inspection_id)
        
        if not inspection:
            logger.warning(f"Inspection {inspection_id} not found")
            return jsonify({'message': 'Inspection not found'}), 404
        
        if inspection.inspected_by != current_user_id:
            logger.warning(f"User {current_user_id} unauthorized to update inspection {inspection_id}")
            return jsonify({'message': 'Unauthorized access to inspection'}), 403
        
        if 'status' in data:
            valid_statuses = ['pending', 'reviewed', 'completed']
            if data['status'] not in valid_statuses:
                return jsonify({'message': f'Status must be one of: {valid_statuses}'}), 400
            inspection.status = data['status']
        
        if 'damage_report' in data:
            inspection.damage_report = data['damage_report']
        
        if 'image_url' in data:
            if data['image_url'] and not Inspection.validate_image_url(data['image_url']):
                return jsonify({'message': 'Image URL must end with .jpg, .jpeg, or .png'}), 400
            inspection.image_url = data['image_url']
        
        db.session.commit()
        
        logger.info(f"Inspection {inspection_id} updated successfully")
        return jsonify({
            'message': 'Inspection updated successfully',
            'inspection': inspection.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Database error during inspection update: {str(e)}")
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500

@inspection_bp.route('/inspection', methods=['GET'])
@jwt_required()
def get_inspections():
    """Fetch all inspections with optional filtering by status"""
    try:
        current_user_id = get_jwt_identity()
        logger.info(f"User {current_user_id} requesting inspections list")
        
        status_filter = request.args.get('status')
        
        query = Inspection.query.filter_by(inspected_by=current_user_id)
        
        if status_filter:
            valid_statuses = ['pending', 'reviewed', 'completed']
            if status_filter not in valid_statuses:
                return jsonify({'message': f'Invalid status. Must be one of: {valid_statuses}'}), 400
            query = query.filter_by(status=status_filter)
        
        inspections = query.all()
        
        inspections_data = [inspection.to_dict() for inspection in inspections]
        
        logger.info(f"Retrieved {len(inspections_data)} inspections for user {current_user_id}")
        return jsonify({
            'inspections': inspections_data,
            'count': len(inspections_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Database error during inspections retrieval: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500
