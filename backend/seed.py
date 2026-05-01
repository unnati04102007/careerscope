import os
import sys
from app import app
from database.models.models import db, College

# College data: (name, type, city, state, rating, placement_pct, fees, description, established)
COLLEGES_DATA = [
    ("IIT Bombay", "Engineering", "Mumbai", "MH", 4.9, "95%", "₹2.2L", "Prestigious IIT with excellent placements and strong alumni network", 1958),
    ("IIT Delhi", "Engineering", "Delhi", "DL", 4.8, "94%", "₹2.1L", "Top-tier engineering institute with international collaborations", 1961),
    ("IIT Madras", "Engineering", "Chennai", "TN", 4.8, "93%", "₹2.0L", "Leading IIT known for research and innovation", 1959),
    ("AIIMS Delhi", "Medical", "Delhi", "DL", 4.9, "99%", "₹1.3K", "Premier medical institute with state-of-the-art facilities", 1956),
    ("NIT Trichy", "Engineering", "Tiruchirappalli", "TN", 4.5, "88%", "₹1.5L", "Highly respected NIT with strong industry connections", 1964),
    ("SRCC Delhi", "Commerce", "Delhi", "DL", 4.6, "90%", "₹25K", "Top commerce college with excellent faculty and placements", 1949),
    ("LSR Delhi", "Arts", "Delhi", "DL", 4.4, "82%", "₹22K", "Women's college known for arts and social sciences", 1956),
    ("IIM Ahmedabad", "Management", "Ahmedabad", "GJ", 4.9, "100%", "₹23L", "Leading management institute with global recognition", 1961),
    ("NLSIU Bangalore", "Law", "Bengaluru", "KA", 4.7, "92%", "₹2.5L", "Top law school with excellent legal education", 1987),
    ("NID Ahmedabad", "Design", "Ahmedabad", "GJ", 4.6, "89%", "₹3.5L", "Premier design institute with world-class facilities", 1969),
    ("Manipal Institute", "Engineering", "Manipal", "KA", 4.2, "82%", "₹4.8L", "Leading private engineering institute with good placements", 1953),
    ("VIT Vellore", "Engineering", "Vellore", "TN", 4.1, "84%", "₹3.8L", "Top private engineering college with strong industry ties", 1984),
    ("St. Xavier's Mumbai", "Arts", "Mumbai", "MH", 4.3, "78%", "₹15K", "Prestigious Jesuit college known for academics", 1869),
    ("Christ University", "Arts", "Bengaluru", "KA", 4.1, "80%", "₹1.2L", "Well-regarded multi-discipline institute", 1969),
    ("Jadavpur University", "Engineering", "Kolkata", "WB", 4.3, "85%", "₹22K", "Premier state engineering university with rich history", 1906),
    ("BITS Pilani", "Engineering", "Pilani", "RJ", 4.6, "91%", "₹5L", "Top private engineering institute with global outlook", 1972),
    ("Symbiosis Law School", "Law", "Pune", "MH", 4.2, "85%", "₹3.2L", "Well-known law institute with strong curriculum", 2003),
    ("NIFT Delhi", "Design", "Delhi", "DL", 4.4, "87%", "₹2.8L", "National Institute of Fashion Technology", 1986),
    ("MICA Ahmedabad", "Management", "Ahmedabad", "GJ", 4.3, "92%", "₹8.5L", "Specialized management school for media and communications", 1990),
    ("IIT Kharagpur", "Engineering", "Kharagpur", "WB", 4.7, "92%", "₹2.2L", "Oldest IIT with strong research programs", 1951),
    ("Amrita University", "Engineering", "Coimbatore", "TN", 4.0, "79%", "₹3.2L", "Good engineering institute with placement support", 1986),
    ("Hindu College Delhi", "Arts", "Delhi", "DL", 4.3, "76%", "₹14K", "Historic college known for excellence in academics", 1899),
    ("XLRI Jamshedpur", "Management", "Jamshedpur", "JH", 4.5, "98%", "₹24L", "Premier business school with excellent placements", 1949),
    ("Fergusson College", "Arts", "Pune", "MH", 4.0, "72%", "₹8K", "Prestigious college with strong academic tradition", 1885),
    ("NIT Warangal", "Engineering", "Warangal", "TS", 4.4, "87%", "₹1.4L", "Leading NIT with quality education", 1959),
    ("JIPMER Puducherry", "Medical", "Puducherry", "PY", 4.7, "98%", "₹1K", "Renowned medical institute with excellent healthcare facilities", 1964),
    ("Presidency University", "Arts", "Kolkata", "WB", 4.2, "74%", "₹6K", "Historic university with strong liberal arts program", 1817),
    ("SRM Institute", "Engineering", "Chennai", "TN", 3.9, "78%", "₹4.5L", "Well-established engineering college with good campus", 1985),
    ("TISS Mumbai", "Arts", "Mumbai", "MH", 4.5, "90%", "₹60K", "Premier social sciences institute with global perspective", 1936),
    ("Miranda House", "Arts", "Delhi", "DL", 4.6, "88%", "₹8K", "Top women's college in Delhi with excellent faculty", 1948),
]

NEW_COLLEGES = [
    { "name":"Delhi University", "city":"New Delhi", "state":"Delhi", "type":"Arts", "rating":4.3, "placement_pct":"75%", "fees":"₹20K/yr", "established":1922, "address":"University Rd, Delhi 110007", "courses":["BA","B.Sc","B.Com","MA"], "description":"One of India's largest universities with diverse programs." },
    { "name":"Pune University", "city":"Pune", "state":"Maharashtra", "type":"Arts", "rating":4.0, "placement_pct":"70%", "fees":"₹12K/yr", "established":1948, "address":"Ganeshkhind, Pune 411007", "courses":["BA","B.Sc","B.Com","LLB"], "description":"Major state university serving western Maharashtra." },
    { "name":"Anna University", "city":"Chennai", "state":"Tamil Nadu", "type":"Engineering", "rating":4.2, "placement_pct":"83%", "fees":"₹45K/yr", "established":1978, "address":"Sardar Patel Rd, Chennai 600025", "courses":["B.Tech","M.Tech","MBA"], "description":"Premier technical university of Tamil Nadu." },
    { "name":"Osmania University", "city":"Hyderabad", "state":"Telangana", "type":"Arts", "rating":3.9, "placement_pct":"68%", "fees":"₹10K/yr", "established":1918, "address":"Osmania University Rd, Hyderabad 500007", "courses":["BA","B.Sc","B.Com","LLB","MBA"], "description":"Historic university, one of oldest in India." },
    { "name":"Banaras Hindu University", "city":"Varanasi", "state":"Uttar Pradesh", "type":"Arts", "rating":4.1, "placement_pct":"74%", "fees":"₹15K/yr", "established":1916, "address":"BHU Campus, Varanasi 221005", "courses":["BA","B.Sc","B.Tech","MBBS","LLB"], "description":"One of Asia's largest residential universities." },
    { "name":"Aligarh Muslim University", "city":"Aligarh", "state":"Uttar Pradesh", "type":"Arts", "rating":4.0, "placement_pct":"72%", "fees":"₹18K/yr", "established":1875, "address":"AMU Campus, Aligarh 202002", "courses":["BA","B.Tech","MBBS","LLB","MBA"], "description":"Central university with strong humanities tradition." },
    { "name":"IIT Roorkee", "city":"Roorkee", "state":"Uttarakhand", "type":"Engineering", "rating":4.6, "placement_pct":"91%", "fees":"₹2.2L/yr", "established":1847, "address":"IIT Campus, Roorkee 247667", "courses":["B.Tech","M.Tech","MBA","PhD"], "description":"Oldest technical institute in Asia, excellent research." },
    { "name":"IIT Kanpur", "city":"Kanpur", "state":"Uttar Pradesh", "type":"Engineering", "rating":4.7, "placement_pct":"92%", "fees":"₹2.1L/yr", "established":1959, "address":"IIT Campus, Kanpur 208016", "courses":["B.Tech","M.Tech","MBA","PhD"], "description":"Known for strong CS and research programs." },
    { "name":"IIM Bangalore", "city":"Bengaluru", "state":"Karnataka", "type":"Management", "rating":4.8, "placement_pct":"100%", "fees":"₹24L/yr", "established":1973, "address":"Bannerghatta Rd, Bengaluru 560076", "courses":["MBA","PGPM","PhD","EMBA"], "description":"India's #2 B-school with global alumni network." },
    { "name":"IIM Calcutta", "city":"Kolkata", "state":"West Bengal", "type":"Management", "rating":4.7, "placement_pct":"100%", "fees":"₹25L/yr", "established":1961, "address":"Diamond Harbour Rd, Kolkata 700104", "courses":["MBA","PGPM","PhD"], "description":"One of Asia's oldest and top-ranked B-schools." },
    { "name":"NALSAR Hyderabad", "city":"Hyderabad", "state":"Telangana", "type":"Law", "rating":4.5, "placement_pct":"88%", "fees":"₹2.2L/yr", "established":1998, "address":"Justice City, Hyderabad 500101", "courses":["BA LLB","LLM","PhD"], "description":"Top-5 law school known for corporate law." },
    { "name":"NIFT Mumbai", "city":"Mumbai", "state":"Maharashtra", "type":"Design", "rating":4.3, "placement_pct":"85%", "fees":"₹2.6L/yr", "established":1995, "address":"Kharghar, Navi Mumbai 410210", "courses":["B.Des","M.Des","M.FM"], "description":"Leading fashion institute in western India." },
    { "name":"Symbiosis Institute of Business", "city":"Pune", "state":"Maharashtra", "type":"Management", "rating":4.1, "placement_pct":"88%", "fees":"₹9L/yr", "established":1978, "address":"Senapati Bapat Rd, Pune 411004", "courses":["MBA","PGDM"], "description":"Top private B-school with international exposure." },
    { "name":"Calcutta Medical College", "city":"Kolkata", "state":"West Bengal", "type":"Medical", "rating":4.2, "placement_pct":"90%", "fees":"₹25K/yr", "established":1835, "address":"88 College St, Kolkata 700073", "courses":["MBBS","MD","MS"], "description":"One of Asia's oldest medical colleges." },
    { "name":"Armed Forces Medical College", "city":"Pune", "state":"Maharashtra", "type":"Medical", "rating":4.4, "placement_pct":"95%", "fees":"₹0", "established":1962, "address":"Sholapur Rd, Pune 411040", "courses":["MBBS","MD","MS"], "description":"Premier medical college for armed forces personnel." },
    { "name":"IIT Hyderabad", "city":"Hyderabad", "state":"Telangana", "type":"Engineering", "rating":4.4, "placement_pct":"88%", "fees":"₹2.0L/yr", "established":2008, "address":"Kandi, Sangareddy 502284", "courses":["B.Tech","M.Tech","PhD"], "description":"New-gen IIT with focus on interdisciplinary research." },
    { "name":"IIIT Hyderabad", "city":"Hyderabad", "state":"Telangana", "type":"Engineering", "rating":4.5, "placement_pct":"92%", "fees":"₹3.5L/yr", "established":1998, "address":"Gachibowli, Hyderabad 500032", "courses":["B.Tech","M.Tech","PhD"], "description":"Top institute for CS and AI research in India." },
    { "name":"Nirma University", "city":"Ahmedabad", "state":"Gujarat", "type":"Engineering", "rating":4.0, "placement_pct":"80%", "fees":"₹2.8L/yr", "established":1994, "address":"Sarkhej-Gandhinagar Hwy, Ahmedabad 382481", "courses":["B.Tech","MBA","LLB","B.Pharm"], "description":"Comprehensive private university with strong industry links." },
    { "name":"Thapar Institute", "city":"Patiala", "state":"Punjab", "type":"Engineering", "rating":4.2, "placement_pct":"85%", "fees":"₹3.5L/yr", "established":1956, "address":"Bhadson Rd, Patiala 147004", "courses":["B.Tech","M.Tech","MBA"], "description":"Top private engineering institute in North India." },
    { "name":"Shiv Nadar University", "city":"Greater Noida", "state":"Uttar Pradesh", "type":"Engineering", "rating":4.1, "placement_pct":"82%", "fees":"₹4.2L/yr", "established":2011, "address":"Tehsil Dadri, Greater Noida 201314", "courses":["B.Tech","MBA","BA","B.Sc"], "description":"Modern research university with liberal arts integration." }
]

def seed_colleges():
    """Seed the database with college data"""
    with app.app_context():
        # Clear existing colleges
        existing_count = College.query.count()
        if existing_count > 0:
            print(f"Found {existing_count} existing colleges. Clearing...")
            db.session.query(College).delete()
            db.session.commit()
        
        colleges_to_add = []
        ALL_DATA = list(COLLEGES_DATA) + NEW_COLLEGES
        
        for data in ALL_DATA:
            if isinstance(data, dict):
                # Process the new dictionary format
                name = data.get("name")
                c_type = data.get("type")
                city = data.get("city")
                state = data.get("state")
                rating = data.get("rating")
                placement = data.get("placement_pct")
                fees = data.get("fees")
                established = data.get("established")
                description = data.get("description")
                address = data.get("address", f"{city}, {state}")
                courses = data.get("courses")
            else:
                # Process the old tuple format
                name, c_type, city, state, rating, placement, fees, description, established = data
                address = f"{city}, {state}"
                courses = None
                
            # Determine default courses based on type if not explicitly provided
            if not courses:
                if c_type == "Engineering": courses = ["B.Tech", "M.Tech", "PhD"]
                elif c_type == "Medical": courses = ["MBBS", "MD", "BDS"]
                elif c_type == "Management": courses = ["MBA", "PGDM", "Executive Programs"]
                elif c_type == "Law": courses = ["BA LLB", "LLM", "Diploma in Law"]
                elif c_type == "Design": courses = ["BDes", "MDes", "Diploma"]
                elif c_type == "Commerce": courses = ["B.Com", "M.Com", "CA", "CMA"]
                else: courses = ["BA", "MA", "BEd", "MEd"]
            
            college = College(
                name=name,
                type=c_type,
                city=city,
                state=state,
                rating=rating,
                placement_pct=placement,
                fees=fees,
                established=established,
                description=description,
                address=address
            )
            college.set_courses(courses)
            colleges_to_add.append(college)
        
        # Add all colleges to session and commit
        db.session.add_all(colleges_to_add)
        db.session.commit()
        
        print(f"✅ Successfully seeded {len(colleges_to_add)} colleges!")

if __name__ == '__main__':
    seed_colleges()
