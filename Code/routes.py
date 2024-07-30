from flask import render_template,Blueprint,request,session,redirect,url_for
from app import app
from db.models import *
from markupsafe import escape 
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from datetime import datetime

main = Blueprint('main',__name__)



db.init_app(app)
#app.app_context().push()



@main.route("/")                                                    #Home page
def hello_world():
    return render_template("Front_Page.html")


@main.route("/register",methods=['GET','POST'])                     #Registration of all users
def register():
    msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        if request.form.get('influencer'):
            user = Influencer(name=name,password=password)
            db.session.add(user)
            db.session.commit()
            msg = "Profile successfully created!"
        elif request.form.get('sponsor'):
            user = Sponsor(name=name,password=password)
            db.session.add(user)
            db.session.commit()
            msg = "Profile successfully created!"
        elif request.form.get('admin'):
            user = Admin(name=name,password=password)
            db.session.add(user)
            db.session.commit()
            msg = "Profile successfully created!"
        else:
            msg = "Select an option above!"

    return render_template("Register.html",msg=msg)







############################## influencer routes start ###############################

@main.route("/influencer-login",methods=['GET','POST'])                     #Influencer login
def influencerLogin():
    msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        user = Influencer.query.filter_by(name=name,password=password).first()

        if user:
            session['influencer_id'] = user.id
            session['user_type'] = 'influencer'

            return redirect(url_for('main.influencer_page'))
        else:
            msg = "Wrong Credentials! Try again."
    return render_template('Login/InfluencerLogin.html',msg=msg)

@main.route("/influencer-page",methods=['GET'])
def influencer_page():
    if session['influencer_id']:
        influencer = Influencer.query.filter_by(id=session['influencer_id']).first()

        return render_template('InfluencerDashboard.html',influencer=influencer)
    

@main.route('/edit-influencer-profile',methods=['POST'])
def edit_influencer_profile():
    edit_name = request.form.get('edit-name')
    edit_industry = request.form.get('edit-industry')
    edit_followers = int(request.form.get('edit-followers'))

    influencer = Influencer.query.filter_by(id=session['influencer_id']).first()

    influencer.name = edit_name
    influencer.industry = edit_industry
    influencer.followers = edit_followers

    db.session.commit()

    return redirect(url_for('main.influencer_page'))


@main.route('/influencer-search-campaign',methods=['GET','POST'])
def influencer_search_campaign():
    if request.method == 'POST':
        search_term = request.form.get('search-term')
        if search_term == '':
            campaign_list = Campaign.query.filter_by(id).all()
        else:
            campaign_list = Campaign.query.filter_by(search_term).all()

    return render_template('InfluencerSearchCampaign.html')


@main.route('/influencer-send-request')

################################ Influencer routes end ###################################








################################ Sponsor routes start ###################################

@main.route("/sponsor-login",methods=['GET','POST'])                     #Sponsor login
def sponsorLogin():
    msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        user = Sponsor.query.filter_by(name=name,password=password).first()

        if user:
            session['sponsor_id'] = user.id
            session['user_type'] = 'sponsor'

            return redirect(url_for('main.sponsor_page'))
        else:
            msg = "Wrong Credentials! Try again."
    
    return render_template('Login/SponsorLogin.html',msg=msg)

@main.route('/sponsor-page',methods=['GET'])                            # sponsor page
def sponsor_page():
    if session['sponsor_id']:
        campaign_list = Campaign.query.filter_by(sponsor_id=session['sponsor_id'])
        return render_template('SponsorDashboard.html',campaign_list=campaign_list,sponsor_id=session['sponsor_id'])
    
    return redirect(url_for('sponsorLogin'))


@main.route("/new-campaign",methods=['POST'])                         # when sponsors click on new campaign
def new_campaign():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        industry = request.form.get('industry')

        start_date = request.form.get('startDate')
        (starting_year,starting_month,starting_date) = (int(start_date[:4]), int(start_date[5:7]), int(start_date[8:]))
        start_date = datetime(starting_year,starting_month,starting_date).date()

        end_date = request.form.get('endDate')
        (ending_year,ending_month,ending_date) = (int(end_date[:4]), int(end_date[5:7]), int(end_date[8:]))
        end_date = datetime(ending_year,ending_month,ending_date).date()

        budget = request.form.get('budget')
        private = request.form.get('private')
        sponsor_id = session['sponsor_id']

        campaign_obj = Campaign(title=title,description=description,industry=industry,start_date=start_date,end_date=end_date,budget=budget,private=private,sponsor_id=sponsor_id)
        db.session.add(campaign_obj)
        db.session.commit()

        return redirect(url_for('main.sponsor_page'))
    

@main.route('/edit-details',methods=['POST'])                           # edit details of a particular campaign
def edit_details():
    if request.method == 'POST':
        campaign_id = int(request.form.get('campaign-id'))
        campaign = Campaign.query.filter_by(id=campaign_id).first()
        campaign.title = request.form.get('title')
        campaign.description = request.form.get('description')
        campaign.industry = request.form.get('industry')

        start_date = request.form.get('startDate')
        (starting_year,starting_month,starting_date) = (int(start_date[:4]), int(start_date[5:7]), int(start_date[8:]))
        campaign.start_date = datetime(starting_year,starting_month,starting_date).date()

        end_date = request.form.get('endDate')
        (ending_year,ending_month,ending_date) = (int(end_date[:4]), int(end_date[5:7]), int(end_date[8:]))
        campaign.end_date = datetime(ending_year,ending_month,ending_date).date()

        campaign.budget = int(request.form.get('budget'))
        campaign.private = request.form.get('private')
        campaign.sponsor_id = int(session['sponsor_id'])
        
        db.session.commit()

        return redirect(url_for('main.sponsor_page'))
    
@main.route('/delete-campaign',methods=['POST'])                            # sponsor deletes a campaign
def delete_campaign():
    if request.method == 'POST':
        delete_campaign_id = int(request.form.get('delete-campaign-id'))
        campaign = Campaign.query.filter_by(id=delete_campaign_id).first()

        db.session.delete(campaign)
        db.session.commit()
    
        return redirect(url_for('main.sponsor_page'))
    
@main.route('/sponsor-search',methods=['GET','POST'])                      # sponsor searches for influencer
def sponsor_search():
    msg = ""
    influencer_list = []

    if request.method == 'POST':
        try:
            search_term = int(request.form.get('search-term'))

            all_influencer_list = Influencer.query.all()

            for influencer in all_influencer_list:
                if influencer.followers >= search_term:
                    influencer_list.append(influencer)

            msg = f"No influencers with at least {search_term} followers found."
            
        except:
            search_term = request.form.get('search-term')

            influencer_list = Influencer.query.filter_by(industry=search_term).all()
             
            msg = f"No influencer found in {search_term} industry."
        
    return render_template('SponsorSearchInfluencer.html',influencer_list=influencer_list,msg=msg)


@main.route('/select-campaign-for-influencer',methods=['GET','POST'])       # sponsor selects an influencer
def select_campaign_for_influencer():
    if request.method == 'POST':
        influencer_id = request.form.get('influencer_id')
        influencer_name = request.form.get('influencer_name')

        campaign_list = Campaign.query.filter_by(sponsor_id=session['sponsor_id']).all()
        ad_request_list = Ad_requests.query.filter_by(sponsor_id=session['sponsor_id'],influencer_id=influencer_id).all()
        
        new_campaign_list = []

        if len(ad_request_list) == 0:
            for campaign in campaign_list:
                new_campaign_list.append(campaign)
                
        else:
            
            for campaign in campaign_list:
                match = False
                for ad_request in ad_request_list:
                    if campaign.id == ad_request.campaign_id:
                        match = True
                        break
                if match == False:
                    new_campaign_list.append(campaign)

        return render_template('Sponsor_select_campaign_for_influencer.html',influencer_id=influencer_id,influencer_name=influencer_name,new_campaign_list=new_campaign_list,ad_request_list=ad_request_list)

@main.route('/add_ad_request',methods=['GET','POST'])                       # sponsor ad request added to database
def add_ad_request():
    if request.method == 'POST':
        sponsor_id = session['sponsor_id']
        sponsor_name = Sponsor.query.get(sponsor_id).name
        campaign_id = request.form.get('campaign-id')
        influencer_id = request.form.get('influencer-id')
        influencer_name = request.form.get('influencer-name')
        request_type = 'S'
        request_status = 'pending'

        ad_request = Ad_requests(sponsor_id=sponsor_id,sponsor_name=sponsor_name,campaign_id=campaign_id,influencer_id=influencer_id,influencer_name=influencer_name,request_type=request_type,request_status=request_status)
        
        db.session.add(ad_request)
        db.session.commit()

    return redirect(url_for('main.sponsor_ad_request_page'))


@main.route('/update_ad_request',methods=['GET','POST'])                    # sponsor takes action on sent request


@main.route('/sponsor_ad_request_page',methods=['GET','POST'])              # sponsor ad request page render
def sponsor_ad_request_page():

    ad_request_list = Ad_requests.query.filter_by(sponsor_id=session['sponsor_id']).all()

    campaign_list = Campaign.query.filter_by(sponsor_id=session['sponsor_id']).all()

    return render_template('SponsorAdRequest.html',ad_request_list=ad_request_list,campaign_list=campaign_list,user_type=session['user_type'])
    
########################### sponsor routes end ################################
 
    






########################### admin routes start ################################

@main.route("/admin-login",methods=['GET','POST'])                     #Admin login
def adminLogin():
    msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        user = Admin.query.filter_by(name=name,password=password).first()

        if user:
            return render_template('AdminDashboard.html')
        else:
            msg = "Wrong Credentials! Try again."
    return render_template('Login/AdminLogin.html',msg=msg)

############################# admin routes end ###################################







@main.route('/logout',methods=['POST'])                             #log out
def logout():
    if request.method == 'POST':
        if 'sponsor_id' in session:
            session.pop('sponsor_id')
            session.pop('user_type')
        elif 'influencer_id' in session:
            session.pop('influencer_id')
            session.pop('user_type')
        else:
            session.pop('admin_id')

        return redirect(url_for('main.hello_world'))



'''
#---- dynamic route ----#
@main.route("/<name>")
def hello_name(name):
    print(request.view_args)
    return f"Hello {escape(name)}"

#---- render template ----#

@app.route("/u/")
@app.route("/u/<name>")
def user_profile(name=None):
    return render_template('main.html',name=name)


#---- login ----#
@main.route("/login")


#---- submit ----#
@main.route("/submit", methods=['POST'])
def submit():
    return render_template("submit.html")
'''

app.register_blueprint(main)