from flask import Blueprint, render_template, request, session, redirect
from app.models.user import User
from app.models.farm import Farm
import bcrypt

farmer_bp = Blueprint('farmer', __name__)

@farmer_bp.route('/', methods=['GET'])
def index():
    return redirect('/login')

@farmer_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.get_user_by_email(email)

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            return redirect('/dashboard')
        else:
            return render_template('farmer/login.html', error="Invalid email or password. Please try again.")
            
    return render_template('farmer/login.html')



@farmer_bp.route('/dashboard', methods=['GET'])
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    user_name = session['user_name']

    farms = Farm.get_farms_by_user(user_id)
    
    selected_farm_id = request.args.get('farm_id')
 
    if not selected_farm_id and len(farms) > 0:
        selected_farm_id = str(farms[0]['_id'])
        
    selected_farm = None
    for farm in farms:

        farm['_id'] = str(farm['_id'])
        if farm['_id'] == selected_farm_id:
            selected_farm = farm
            
    return render_template('farmer/dashboard.html', 
                           user_name=user_name, 
                           farms=farms, 
                           selected_farm=selected_farm)

@farmer_bp.route('/seed-recommendation', methods=['GET'])
def seed_recommendation():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    user_name = session['user_name']
    farms = Farm.get_farms_by_user(user_id)
    
    for farm in farms:
        farm['_id'] = str(farm['_id'])
        
    selected_farm_id = request.args.get('farm_id')
    return render_template('farmer/seed_recommendation.html',
                           user_name=user_name,
                           farms=farms,
                           selected_farm_id=selected_farm_id)


@farmer_bp.route('/guidance/<crop_name>', methods=['GET'])
def guidance(crop_name):
    if 'user_id' not in session:
        return redirect('/login')
    
    user_name = session.get('user_name', 'Farmer')
    from app.utils.crop_guidance import get_crop_guidance
    crop_info = get_crop_guidance(crop_name)
    
    confidence = request.args.get('confidence', '95.0')
    farm_name = request.args.get('farm_name', 'My Farm')

    return render_template('farmer/guidance.html',
                           user_name=user_name,
                           crop_name=crop_name,
                           crop_info=crop_info,
                           confidence=confidence,
                           farm_name=farm_name)


@farmer_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect('/login')