from app import app, db
from database.models import College, Career

def seed_data():
    with app.app_context():
        db.create_all()
        
        # Check if data exists
        if College.query.first():
            print("Data already exists. Skipping seed.")
            return

        print("Seeding Colleges...")
        colleges = [
            College(name="IIT Bombay", location="Mumbai", rating=4.9, fees="2.5 Lakhs/Year", courses="Engineering, Design"),
            College(name="St. Xavier's College", location="Mumbai", rating=4.7, fees="40,000/Year", courses="Arts, Science, Commerce"),
            College(name="Delhi University", location="Delhi", rating=4.6, fees="15,000/Year", courses="Arts, Commerce, Science"),
            College(name="IIM Ahmedabad", location="Ahmedabad", rating=4.9, fees="25 Lakhs/Total", courses="MBA, Management"),
            College(name="Christ University", location="Bangalore", rating=4.5, fees="1.8 Lakhs/Year", courses="BBA, BCA, Arts"),
            College(name="AIIMS Delhi", location="Delhi", rating=4.9, fees="2,000/Year", courses="Medical (MBBS)"),
            College(name="SRM University", location="Chennai", rating=4.2, fees="3 Lakhs/Year", courses="Engineering, Management"),
            College(name="National Institute of Design", location="Ahmedabad", rating=4.8, fees="3.5 Lakhs/Year", courses="Design"),
            College(name="NLSIU Bangalore", location="Bangalore", rating=4.9, fees="3 Lakhs/Year", courses="Law"),
        ]
        
        db.session.add_all(colleges)
        
        print("Seeding Careers...")
        careers = [
            Career(title="Data Scientist", description="Analyze complex data to help companies make decisions.", required_skills="Maths, Python, SQL, Statistics", recommended_stream="Science", avg_salary="10-15 LPA"),
            Career(title="Software Engineer", description="Build and maintain software systems.", required_skills="Coding (Java/C++), Problem Solving", recommended_stream="Science", avg_salary="8-20 LPA"),
            Career(title="Chartered Accountant", description="Manage finances, audit, and taxation.", required_skills="Accounting, Math, Law", recommended_stream="Commerce", avg_salary="7-12 LPA"),
            Career(title="Financial Analyst", description="Assess investment performance and economic trends.", required_skills="Finance, Excel, Analytical Thinking", recommended_stream="Commerce", avg_salary="6-10 LPA"),
            Career(title="Doctor", description="Diagnose and treat patients.", required_skills="Biology, Patience, Empathy", recommended_stream="Science (PCB)", avg_salary="10-25 LPA"),
            Career(title="Graphic Designer", description="Create visual concepts for brands.", required_skills="Creativity, Photoshop, Illustrator", recommended_stream="Arts/Design", avg_salary="4-8 LPA"),
            Career(title="Lawyer", description="Advise and represent clients in legal matters.", required_skills="Communication, Logic, Research", recommended_stream="humanities", avg_salary="5-15 LPA"),
        ]
        
        db.session.add_all(careers)
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
