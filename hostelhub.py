# -*- coding: utf-8 -*-
"""
HostelHub - Premium Property & Smart Room Management System
Created as a single-file executable web application using Python Flask.
"""

import importlib.util
import sys
import subprocess

# Auto-installer logic for Flask dependency
if importlib.util.find_spec("flask") is None:
    print("Flask is not installed. Auto-installing Flask via pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("Flask successfully installed!")
    except Exception as e:
        print(f"Error installing Flask: {e}")
        sys.exit(1)

# Core imports
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "hostelhub_secret_key_luxury_gold_black_v2"

# Global System Settings (Fully Dynamic)
settings = {
    "property_name": "HostelHub Central",
    "currency": "₹",
    "default_capacity": 4
}

# Static rooms database (90 rooms across Block A/B/C, floors Ground/1st/2nd)
# 3 Blocks * 3 Floors * 10 Rooms = 90 Rooms total.
rooms_db = []
blocks = ["Block A", "Block B", "Block C"]
floors = ["Ground", "1st", "2nd"]
for b in blocks:
    for f in floors:
        # Determine room numbering: Ground (101-110), 1st (201-210), 2nd (301-310)
        room_start = 101 if f == "Ground" else (201 if f == "1st" else 301)
        for r_num in range(room_start, room_start + 10):
            # Assign specific rooms to maintenance for realistic data
            status = "Maintenance" if (b == "Block B" and r_num == 105) or (b == "Block C" and r_num == 208) else "Active"
            # Capacity: odd rooms have 2 beds, even rooms have 4 beds
            capacity = 4 if r_num % 2 == 0 else 2
            rooms_db.append({
                "block": b,
                "floor": f,
                "room_number": str(r_num),
                "capacity": capacity,
                "status": status
            })

# Mock database - 26 Preloaded Students assigned to structural blocks and rooms
students_db = [
    {"id": 1, "name": "Aarav Sharma", "mobile": "+91 98765 01001", "email": "aarav.sharma@hostelhub.co", "guardian_name": "Ramesh Sharma", "guardian_contact": "+91 98765 01002", "block": "Block A", "room": "201", "floor": "1st", "course": "Cyber Security", "admission_date": "2025-08-15", "rent": 12000, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 2, "name": "Priya Patel", "mobile": "+91 98765 01003", "email": "priya.patel@hostelhub.co", "guardian_name": "Kirit Patel", "guardian_contact": "+91 98765 01004", "block": "Block A", "room": "201", "floor": "1st", "course": "Artificial Intelligence", "admission_date": "2025-09-01", "rent": 15000, "payment_status": "Pending", "occupancy": "Active"},
    {"id": 3, "name": "Rohan Gupta", "mobile": "+91 98765 01005", "email": "rohan.gupta@hostelhub.co", "guardian_name": "Sunil Gupta", "guardian_contact": "+91 98765 01006", "block": "Block A", "room": "301", "floor": "2nd", "course": "Philosophy & Law", "admission_date": "2025-07-20", "rent": 11000, "payment_status": "Partial", "occupancy": "Active"},
    {"id": 4, "name": "Siddharth Mehta", "mobile": "+91 98765 43210", "email": "sid.mehta@hostelhub.co", "guardian_name": "Rajesh Mehta", "guardian_contact": "+91 98765 43211", "block": "Block A", "room": "102", "floor": "Ground", "course": "Data Analytics", "admission_date": "2025-09-10", "rent": 13000, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 5, "name": "Sneha Iyer", "mobile": "+91 98765 01007", "email": "sneha.iyer@hostelhub.co", "guardian_name": "Srinivasan Iyer", "guardian_contact": "+91 98765 01008", "block": "Block B", "room": "101", "floor": "Ground", "course": "Fintech & Finance", "admission_date": "2025-08-22", "rent": 16000, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 6, "name": "Vikram Rao", "mobile": "+91 98765 01009", "email": "vikram.rao@hostelhub.co", "guardian_name": "Venkat Rao", "guardian_contact": "+91 98765 01010", "block": "Block B", "room": "202", "floor": "1st", "course": "Robotics Engineering", "admission_date": "2025-09-05", "rent": 14500, "payment_status": "Pending", "occupancy": "Active"},
    {"id": 7, "name": "Ananya Sen", "mobile": "+91 98765 01011", "email": "ananya.sen@hostelhub.co", "guardian_name": "Debasish Sen", "guardian_contact": "+91 98765 01012", "block": "Block B", "room": "303", "floor": "2nd", "course": "International Relations", "admission_date": "2025-09-01", "rent": 12500, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 8, "name": "Devansh Joshi", "mobile": "+91 98765 01013", "email": "devansh.joshi@hostelhub.co", "guardian_name": "Harish Joshi", "guardian_contact": "+91 98765 01014", "block": "Block C", "room": "104", "floor": "Ground", "course": "Architecture", "admission_date": "2025-08-10", "rent": 13500, "payment_status": "Partial", "occupancy": "Active"},
    {"id": 9, "name": "Ishita Verma", "mobile": "+91 98765 01015", "email": "ishita.verma@hostelhub.co", "guardian_name": "Manoj Verma", "guardian_contact": "+91 98765 01016", "block": "Block C", "room": "205", "floor": "1st", "course": "Civil Engineering", "admission_date": "2025-08-25", "rent": 14000, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 10, "name": "Kabir Nair", "mobile": "+91 98765 01017", "email": "kabir.nair@hostelhub.co", "guardian_name": "Madhavan Nair", "guardian_contact": "+91 98765 01018", "block": "Block C", "room": "306", "floor": "2nd", "course": "Marine Biology", "admission_date": "2025-09-01", "rent": 12000, "payment_status": "Pending", "occupancy": "Active"},
    {"id": 11, "name": "Sofia Deshmukh", "mobile": "+91 98765 01019", "email": "sofia.d@hostelhub.co", "guardian_name": "Vijay Deshmukh", "guardian_contact": "+91 98765 01020", "block": "Block A", "room": "103", "floor": "Ground", "course": "Biotechnology", "admission_date": "2025-07-15", "rent": 15500, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 12, "name": "Arjun Kapoor", "mobile": "+91 98765 01021", "email": "arjun.kapoor@hostelhub.co", "guardian_name": "Anil Kapoor", "guardian_contact": "+91 98765 01022", "block": "Block A", "room": "202", "floor": "1st", "course": "Aerospace Engineering", "admission_date": "2025-09-03", "rent": 16500, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 13, "name": "Divya Reddy", "mobile": "+91 98765 01023", "email": "divya.reddy@hostelhub.co", "guardian_name": "Gopal Reddy", "guardian_contact": "+91 98765 01024", "block": "Block B", "room": "102", "floor": "Ground", "course": "Software Engineering", "admission_date": "2025-09-01", "rent": 13000, "payment_status": "Partial", "occupancy": "Active"},
    {"id": 14, "name": "Aditya Saxena", "mobile": "+91 98765 01025", "email": "aditya.saxena@hostelhub.co", "guardian_name": "Rajiv Saxena", "guardian_contact": "+91 98765 01026", "block": "Block B", "room": "203", "floor": "1st", "course": "Sports Science", "admission_date": "2025-08-18", "rent": 11500, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 15, "name": "Neha Bhatia", "mobile": "+91 98765 01027", "email": "neha.bhatia@hostelhub.co", "guardian_name": "Ashok Bhatia", "guardian_contact": "+91 98765 01028", "block": "Block C", "room": "105", "floor": "Ground", "course": "English Literature", "admission_date": "2025-09-01", "rent": 12500, "payment_status": "Pending", "occupancy": "Active"},
    {"id": 16, "name": "Harshvardhan Singh", "mobile": "+91 98765 01029", "email": "harshvardhan.singh@hostelhub.co", "guardian_name": "Rajendra Singh", "guardian_contact": "+91 98765 01030", "block": "Block C", "room": "206", "floor": "1st", "course": "Military Strategy", "admission_date": "2025-06-01", "rent": 18000, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 17, "name": "Nisha Patel", "mobile": "+91 91234 56789", "email": "nisha.patel@hostelhub.co", "guardian_name": "Devendra Patel", "guardian_contact": "+91 91234 56780", "block": "Block A", "room": "302", "floor": "2nd", "course": "Medicine", "admission_date": "2025-09-02", "rent": 15000, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 18, "name": "Nikhil Mishra", "mobile": "+91 98765 01031", "email": "nikhil.mishra@hostelhub.co", "guardian_name": "Suresh Mishra", "guardian_contact": "+91 98765 01032", "block": "Block B", "room": "304", "floor": "2nd", "course": "Mechanical Engineering", "admission_date": "2025-08-30", "rent": 13000, "payment_status": "Pending", "occupancy": "Active"},
    {"id": 19, "name": "Tanvi Singhal", "mobile": "+91 98765 01033", "email": "tanvi.singhal@hostelhub.co", "guardian_name": "Alok Singhal", "guardian_contact": "+91 98765 01034", "block": "Block C", "room": "307", "floor": "2nd", "course": "Economics", "admission_date": "2025-09-01", "rent": 14000, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 20, "name": "Yash Choudhary", "mobile": "+91 98765 01035", "email": "yash.choudhary@hostelhub.co", "guardian_name": "Sanjay Choudhary", "guardian_contact": "+91 98765 01036", "block": "Block A", "room": "104", "floor": "Ground", "course": "Fine Arts", "admission_date": "2025-05-01", "rent": 17000, "payment_status": "Partial", "occupancy": "Active"},
    {"id": 21, "name": "Gauri Trivedi", "mobile": "+91 98765 01037", "email": "gauri.trivedi@hostelhub.co", "guardian_name": "Pankaj Trivedi", "guardian_contact": "+91 98765 01038", "block": "Block B", "room": "103", "floor": "Ground", "course": "Computer Science", "admission_date": "2025-07-04", "rent": 16000, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 22, "name": "Ishaan Sharma", "mobile": "+91 98765 01039", "email": "ishaan.sharma@hostelhub.co", "guardian_name": "Vijay Sharma", "guardian_contact": "+91 98765 01040", "block": "Block C", "room": "106", "floor": "Ground", "course": "Physics & Mathematics", "admission_date": "2025-09-01", "rent": 15000, "payment_status": "Paid", "occupancy": "Checked Out"},
    {"id": 23, "name": "Mansi Shinde", "mobile": "+91 98765 01041", "email": "mansi.shinde@hostelhub.co", "guardian_name": "Prakash Shinde", "guardian_contact": "+91 98765 01042", "block": "Block A", "room": "203", "floor": "1st", "course": "Chemistry", "admission_date": "2025-08-01", "rent": 15500, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 24, "name": "Aman Saxena", "mobile": "+91 98765 01043", "email": "aman.saxena@hostelhub.co", "guardian_name": "Vineet Saxena", "guardian_contact": "+91 98765 01044", "block": "Block B", "room": "204", "floor": "1st", "course": "Theoretical Physics", "admission_date": "2025-09-01", "rent": 14000, "payment_status": "Pending", "occupancy": "Active"},
    {"id": 25, "name": "Aditi Banerjee", "mobile": "+91 98765 01045", "email": "aditi.banerjee@hostelhub.co", "guardian_name": "Pradip Banerjee", "guardian_contact": "+91 98765 01046", "block": "Block C", "room": "207", "floor": "1st", "course": "Mathematics & Computation", "admission_date": "2025-09-01", "rent": 16500, "payment_status": "Paid", "occupancy": "Active"},
    {"id": 26, "name": "Nilay Shah", "mobile": "+91 98765 01047", "email": "nilay.shah@hostelhub.co", "guardian_name": "Pankaj Shah", "guardian_contact": "+91 98765 01048", "block": "Block A", "room": "303", "floor": "2nd", "course": "Electrical Engineering", "admission_date": "2025-09-01", "rent": 13500, "payment_status": "Partial", "occupancy": "Active"}
]

def get_room_occupancy_data():
    """Calculates live occupancy, capacity, available beds, revenue, and status for all 90 rooms."""
    rooms_data = []
    
    # Group students by (block, room)
    occupied_map = {}
    for s in students_db:
        if s['occupancy'] == 'Active' and s['room'] and s['block']:
            key = (s['block'], s['room'])
            if key not in occupied_map:
                occupied_map[key] = []
            occupied_map[key].append(s)
            
    for r in rooms_db:
        key = (r['block'], r['room_number'])
        occupants = occupied_map.get(key, [])
        occupied_beds = len(occupants)
        available_beds = max(r['capacity'] - occupied_beds, 0)
        monthly_revenue = sum(s['rent'] for s in occupants)
        
        # Determine visual status: Available, Partially Occupied, Fully Occupied, Maintenance
        if r['status'] == 'Maintenance':
            status = 'Maintenance'
        elif occupied_beds == 0:
            status = 'Available'
        elif occupied_beds >= r['capacity']:
            status = 'Fully Occupied'
        else:
            status = 'Partially Occupied'
            
        rooms_data.append({
            "block": r['block'],
            "floor": r['floor'],
            "room_number": r['room_number'],
            "capacity": r['capacity'],
            "occupied_beds": occupied_beds,
            "available_beds": available_beds,
            "monthly_revenue": monthly_revenue,
            "status": status,
            "occupants": [{"id": s['id'], "name": s['name'], "mobile": s['mobile'], "course": s['course'], "rent": s['rent'], "payment_status": s['payment_status'], "admission_date": s['admission_date']} for s in occupants]
        })
    return rooms_data

def calculate_metrics():
    """Calculates all key metrics dynamically from in-memory students database and rooms config."""
    active_students = [s for s in students_db if s['occupancy'] == 'Active']
    total_beds = sum(r['capacity'] for r in rooms_db)
    
    # Active Rooms set
    active_rooms_set = set((s['block'], s['room']) for s in active_students if s['room'] and s['block'])
    active_rooms = len(active_rooms_set)
    
    # Occupied Beds
    occupied_beds = len(active_students)
    available_beds = max(total_beds - occupied_beds, 0)
    
    # Room statistics
    total_rooms = len(rooms_db)
    maintenance_rooms = len([r for r in rooms_db if r['status'] == 'Maintenance'])
    occupied_rooms_count = active_rooms
    vacant_rooms_count = len([r for r in rooms_db if r['status'] != 'Maintenance' and (r['block'], r['room_number']) not in active_rooms_set])
    
    # Registered Students count
    registered_students = len(active_students)
    
    # Financial Analytics
    total_revenue_generated = sum(s['rent'] for s in active_students)
    revenue_collected = 0
    pending_dues = 0
    
    for s in active_students:
        if s['payment_status'] == 'Paid':
            revenue_collected += s['rent']
        elif s['payment_status'] == 'Partial':
            half_rent = s['rent'] // 2
            revenue_collected += half_rent
            pending_dues += s['rent'] - half_rent
        elif s['payment_status'] == 'Pending':
            pending_dues += s['rent']
            
    occupancy_rate = round((occupied_beds / total_beds) * 100, 1) if total_beds > 0 else 0
    room_occupancy_rate = round((active_rooms / total_rooms) * 100, 1) if total_rooms > 0 else 0
    collection_rate = round((revenue_collected / total_revenue_generated) * 100, 1) if total_revenue_generated > 0 else 0
    
    return {
        "active_rooms": active_rooms,
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms_count,
        "vacant_rooms": vacant_rooms_count,
        "maintenance_rooms": maintenance_rooms,
        "registered_students": registered_students,
        "pending_dues": pending_dues,
        "occupancy_rate": occupancy_rate,
        "room_occupancy_rate": room_occupancy_rate,
        "revenue_collected": revenue_collected,
        "total_revenue_generated": total_revenue_generated,
        "total_beds": total_beds,
        "occupied_beds": occupied_beds,
        "available_beds": available_beds,
        "collection_rate": collection_rate
    }

# Embedded HTML main template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en" class="dark h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ settings.property_name }} - Property Layout Console</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
            background-color: #020617;
        }
        .gold-glow {
            box-shadow: 0 0 25px rgba(251, 191, 36, 0.06), 0 0 50px rgba(251, 191, 36, 0.03);
        }
        .gold-glow-hover:hover {
            box-shadow: 0 0 25px rgba(251, 191, 36, 0.18), 0 0 50px rgba(251, 191, 36, 0.08);
        }
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #090d16;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 9999px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #fbbf24;
        }
        .pulse-emerald { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); animation: pulse-emerald 2s infinite; }
        @keyframes pulse-emerald { 70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); } 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } }
        
        .pulse-amber { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); animation: pulse-amber 2s infinite; }
        @keyframes pulse-amber { 70% { box-shadow: 0 0 0 8px rgba(245, 158, 11, 0); } 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); } }
        
        .pulse-rose { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.4); animation: pulse-rose 2s infinite; }
        @keyframes pulse-rose { 70% { box-shadow: 0 0 0 8px rgba(244, 63, 94, 0); } 100% { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0); } }
        
        .pulse-purple { box-shadow: 0 0 0 0 rgba(168, 85, 247, 0.4); animation: pulse-purple 2s infinite; }
        @keyframes pulse-purple { 70% { box-shadow: 0 0 0 8px rgba(168, 85, 247, 0); } 100% { box-shadow: 0 0 0 0 rgba(168, 85, 247, 0); } }
    </style>
</head>
<body class="text-slate-100 h-screen overflow-hidden bg-slate-950">

    <!-- Screen Wrapper -->
    <div class="flex h-full w-full overflow-hidden">
        
        <!-- Sidebar Navigation -->
        <aside class="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between shrink-0 relative z-20">
            <!-- Sidebar Gold Accent line -->
            <div class="absolute top-0 bottom-0 left-0 w-[3px] bg-gradient-to-b from-amber-400 via-yellow-500 to-orange-500"></div>
            
            <div>
                <!-- Brand logo -->
                <div class="p-6 border-b border-slate-800/80 flex items-center space-x-3">
                    <div class="h-10 w-10 rounded-xl bg-gradient-to-br from-amber-400 via-yellow-500 to-orange-500 flex items-center justify-center shadow-lg shadow-amber-500/25">
                        <i data-lucide="hotel" class="text-slate-950 font-bold text-xl"></i>
                    </div>
                    <div>
                        <h1 class="text-base font-extrabold tracking-wider bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500 bg-clip-text text-transparent uppercase">HostelHub</h1>
                        <span class="block text-[9px] text-slate-500 font-bold tracking-widest uppercase">Enterprise Portal</span>
                    </div>
                </div>

                <!-- Navigation items -->
                <nav class="p-4 space-y-1.5">
                    <button onclick="switchTab('overview')" id="nav-overview" class="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-xs font-bold uppercase tracking-wider text-slate-400 hover:text-slate-200 transition-all duration-200">
                        <i data-lucide="layout-dashboard" class="w-4 h-4"></i>
                        <span>Dashboard</span>
                    </button>
                    
                    <button onclick="switchTab('directory')" id="nav-directory" class="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-xs font-bold uppercase tracking-wider text-slate-400 hover:text-slate-200 transition-all duration-200">
                        <i data-lucide="users" class="w-4 h-4"></i>
                        <span>Students</span>
                    </button>

                    <button onclick="switchTab('rooms')" id="nav-rooms" class="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-xs font-bold uppercase tracking-wider text-slate-400 hover:text-slate-200 transition-all duration-200">
                        <i data-lucide="grid" class="w-4 h-4"></i>
                        <span>Smart Rooms</span>
                    </button>

                    <button onclick="switchTab('analytics')" id="nav-analytics" class="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-xs font-bold uppercase tracking-wider text-slate-400 hover:text-slate-200 transition-all duration-200">
                        <i data-lucide="pie-chart" class="w-4 h-4"></i>
                        <span>Analytics</span>
                    </button>

                    <button onclick="switchTab('payments')" id="nav-payments" class="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-xs font-bold uppercase tracking-wider text-slate-400 hover:text-slate-200 transition-all duration-200">
                        <i data-lucide="credit-card" class="w-4 h-4"></i>
                        <span>Payments</span>
                    </button>

                    <button onclick="switchTab('settings')" id="nav-settings" class="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-xs font-bold uppercase tracking-wider text-slate-400 hover:text-slate-200 transition-all duration-200">
                        <i data-lucide="settings" class="w-4 h-4"></i>
                        <span>Settings</span>
                    </button>
                </nav>
            </div>

            <!-- Profile Info Footer -->
            <div class="p-4 border-t border-slate-800/80 flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <div class="h-9 w-9 rounded-full bg-gradient-to-tr from-amber-400 to-orange-500 p-0.5 shadow-sm shadow-amber-500/10">
                        <div class="h-full w-full rounded-full bg-slate-950 flex items-center justify-center">
                            <span class="text-xs font-bold text-amber-400">AD</span>
                        </div>
                    </div>
                    <div>
                        <h4 class="text-xs font-bold text-white">System Admin</h4>
                        <span class="text-[9px] text-slate-500 block font-semibold">Live Administrator</span>
                    </div>
                </div>
                <button onclick="switchTab('settings')" class="h-8 w-8 rounded-lg bg-slate-800 hover:bg-slate-750 flex items-center justify-center border border-slate-700 text-slate-400 hover:text-white transition-colors">
                    <i data-lucide="log-out" class="w-3.5 h-3.5"></i>
                </button>
            </div>
        </aside>

        <!-- Main Workspace Area -->
        <div class="flex-grow flex flex-col h-full overflow-hidden bg-slate-950">
            
            <!-- Global top bar header -->
            <header class="h-16 bg-slate-900 border-b border-slate-800/80 flex items-center justify-between px-6 shrink-0 relative z-10">
                <div class="flex items-center space-x-4">
                    <h2 id="page-title" class="text-base font-black text-white uppercase tracking-wider">Dashboard</h2>
                    <div class="h-4 w-[1px] bg-slate-800"></div>
                    <p id="page-subtitle" class="text-xs text-slate-400 hidden md:block">Real-time statistics & billing logs</p>
                </div>

                <div class="flex items-center space-x-4">
                    <!-- Live indicator -->
                    <div class="flex items-center space-x-2 bg-slate-950/80 px-3.5 py-1.5 rounded-full border border-amber-500/20">
                        <span class="relative flex h-2 w-2">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                        </span>
                        <span class="text-[9px] text-slate-300 font-bold uppercase tracking-wider">Live System</span>
                    </div>
                    
                    <!-- Date -->
                    <div class="text-[11px] text-slate-400 font-bold bg-slate-950/80 px-3.5 py-1.5 rounded-full border border-slate-800 flex items-center space-x-2">
                        <i data-lucide="calendar" class="w-3.5 h-3.5 text-amber-500"></i>
                        <span id="live-date"></span>
                    </div>
                </div>
            </header>

            <!-- Main Scrollable Dashboard Content -->
            <main class="flex-grow overflow-y-auto p-6 relative">
                
                <!-- Tab 1: Dashboard Overview -->
                <section id="tab-overview" class="space-y-8">
                    <!-- Statistics Grid -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
                        <!-- Active Rooms -->
                        <div class="relative overflow-hidden rounded-2xl bg-slate-900/60 backdrop-blur-xl border border-amber-500/10 p-5 transition-all duration-300 hover:scale-[1.02] hover:border-amber-500/30 gold-glow-hover">
                            <div class="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500"></div>
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-xs font-bold text-slate-400 tracking-wider uppercase">Active Rooms</span>
                                <div class="h-8 w-8 rounded-lg bg-amber-500/10 flex items-center justify-center border border-amber-500/20">
                                    <i data-lucide="key" class="w-4 h-4 text-amber-400"></i>
                                </div>
                            </div>
                            <div class="flex items-baseline space-x-2">
                                <span class="text-3xl font-extrabold tracking-tight text-white">{{ metrics.active_rooms }}</span>
                                <span class="text-xs text-slate-500">/ {{ metrics.total_rooms }}</span>
                            </div>
                            <p class="text-xs text-slate-400 mt-3 flex items-center">
                                <span class="inline-block w-1.5 h-1.5 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>
                                {{ metrics.vacant_rooms }} rooms fully vacant
                            </p>
                        </div>

                        <!-- Total Residents -->
                        <div class="relative overflow-hidden rounded-2xl bg-slate-900/60 backdrop-blur-xl border border-amber-500/10 p-5 transition-all duration-300 hover:scale-[1.02] hover:border-amber-500/30 gold-glow-hover">
                            <div class="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500"></div>
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-xs font-bold text-slate-400 tracking-wider uppercase">Active Residents</span>
                                <div class="h-8 w-8 rounded-lg bg-amber-500/10 flex items-center justify-center border border-amber-500/20">
                                    <i data-lucide="users" class="w-4 h-4 text-amber-400"></i>
                                </div>
                            </div>
                            <div class="flex items-baseline space-x-2">
                                <span class="text-3xl font-extrabold tracking-tight text-white">{{ metrics.registered_students }}</span>
                                <span class="text-xs text-slate-500">Beds Occupied</span>
                            </div>
                            <p class="text-xs text-slate-400 mt-3 flex items-center">
                                <i data-lucide="shield-check" class="w-3.5 h-3.5 text-emerald-400 mr-1"></i>
                                {{ metrics.total_beds }} beds total capacity
                            </p>
                        </div>

                        <!-- Pending Dues -->
                        <div class="relative overflow-hidden rounded-2xl bg-slate-900/60 backdrop-blur-xl border border-amber-500/10 p-5 transition-all duration-300 hover:scale-[1.02] hover:border-amber-500/30 gold-glow-hover">
                            <div class="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500"></div>
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-xs font-bold text-slate-400 tracking-wider uppercase">Pending Dues</span>
                                <div class="h-8 w-8 rounded-lg bg-rose-500/10 flex items-center justify-center border border-rose-500/20">
                                    <i data-lucide="alert-circle" class="w-4 h-4 text-rose-400"></i>
                                </div>
                            </div>
                            <div class="flex items-baseline space-x-2">
                                <span class="text-3xl font-extrabold tracking-tight text-white">{{ settings.currency }}{{ "{:,}".format(metrics.pending_dues) }}</span>
                            </div>
                            <p class="text-xs text-slate-400 mt-3 flex items-center">
                                <span class="inline-block w-1.5 h-1.5 rounded-full bg-rose-500 mr-2 animate-pulse"></span>
                                Outstanding receivables
                            </p>
                        </div>

                        <!-- Bed Occupancy Rate -->
                        <div class="relative overflow-hidden rounded-2xl bg-slate-900/60 backdrop-blur-xl border border-amber-500/10 p-5 transition-all duration-300 hover:scale-[1.02] hover:border-amber-500/30 gold-glow-hover">
                            <div class="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500"></div>
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-xs font-bold text-slate-400 tracking-wider uppercase">Bed Occupancy</span>
                                <div class="h-8 w-8 rounded-lg bg-amber-500/10 flex items-center justify-center border border-amber-500/20">
                                    <i data-lucide="pie-chart" class="w-4 h-4 text-amber-400"></i>
                                </div>
                            </div>
                            <div class="flex items-baseline space-x-2">
                                <span class="text-3xl font-extrabold tracking-tight text-white">{{ metrics.occupancy_rate }}%</span>
                            </div>
                            <div class="w-full bg-slate-800 h-1.5 rounded-full mt-4 overflow-hidden">
                                <div class="bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500 h-full rounded-full" style="width: {{ metrics.occupancy_rate }}%"></div>
                            </div>
                        </div>

                        <!-- Revenue Collected -->
                        <div class="relative overflow-hidden rounded-2xl bg-slate-900/60 backdrop-blur-xl border border-amber-500/10 p-5 transition-all duration-300 hover:scale-[1.02] hover:border-amber-500/30 gold-glow-hover">
                            <div class="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500"></div>
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-xs font-bold text-slate-400 tracking-wider uppercase">Collected Revenue</span>
                                <div class="h-8 w-8 rounded-lg bg-emerald-500/10 flex items-center justify-center border border-emerald-500/20">
                                    <i data-lucide="dollar-sign" class="w-4 h-4 text-emerald-400"></i>
                                </div>
                            </div>
                            <div class="flex items-baseline space-x-2">
                                <span class="text-3xl font-extrabold tracking-tight text-white">{{ settings.currency }}{{ "{:,}".format(metrics.revenue_collected) }}</span>
                            </div>
                            <p class="text-xs text-slate-400 mt-3 flex items-center">
                                <i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400 mr-1"></i>
                                {{ metrics.collection_rate }}% collection progress
                            </p>
                        </div>
                    </div>

                    <!-- Layout Sub-split: Quick charts & System Logs -->
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div class="lg:col-span-2 bg-slate-900/50 border border-amber-500/10 rounded-2xl p-6 gold-glow flex flex-col justify-between">
                            <div>
                                <h3 class="text-lg font-bold text-white mb-6 flex items-center space-x-2">
                                    <i data-lucide="trending-up" class="text-amber-500"></i>
                                    <span>Property Operational Metrics</span>
                                </h3>
                                
                                <div class="space-y-6">
                                    <div>
                                        <div class="flex justify-between items-center mb-2">
                                            <span class="text-xs font-bold text-slate-300">Room Occupancy Progress</span>
                                            <span class="text-xs font-bold text-amber-400">{{ metrics.occupied_rooms }} / {{ metrics.total_rooms }} Rooms</span>
                                        </div>
                                        <div class="w-full bg-slate-950 h-3.5 rounded-full overflow-hidden p-0.5 border border-slate-800">
                                            <div class="bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500 h-full rounded-full" style="width: {{ metrics.room_occupancy_rate }}%"></div>
                                        </div>
                                    </div>

                                    <div>
                                        <div class="flex justify-between items-center mb-2">
                                            <span class="text-xs font-bold text-slate-300">Bed Allocation Progress</span>
                                            <span class="text-xs font-bold text-emerald-400">{{ metrics.occupied_beds }} / {{ metrics.total_beds }} Beds</span>
                                        </div>
                                        <div class="w-full bg-slate-950 h-3.5 rounded-full overflow-hidden p-0.5 border border-slate-800">
                                            <div class="bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-400 h-full rounded-full" style="width: {{ metrics.occupancy_rate }}%"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-8 pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-500 font-semibold">
                                <span>HostelHub Realtime Sync Mode</span>
                                <a onclick="switchTab('rooms')" class="text-amber-500 hover:text-amber-400 cursor-pointer flex items-center space-x-1 font-bold">
                                    <span>Open Smart Rooms View</span>
                                    <i data-lucide="arrow-right" class="w-3 h-3"></i>
                                </a>
                            </div>
                        </div>

                        <!-- System Recommendation card -->
                        <div class="bg-slate-900/50 border border-amber-500/10 rounded-2xl p-6 gold-glow flex flex-col justify-between">
                            <div>
                                <h3 class="text-base font-bold text-white mb-4 flex items-center space-x-2">
                                    <i data-lucide="sparkles" class="text-amber-500"></i>
                                    <span>AI System Advisor</span>
                                </h3>
                                
                                <p class="text-xs text-slate-300 leading-relaxed">
                                    Currently, **{{ metrics.occupied_rooms }}** out of **{{ metrics.total_rooms }}** rooms are partially or fully occupied. There are **{{ metrics.maintenance_rooms }}** rooms marked for Maintenance.
                                    The remaining **{{ metrics.vacant_rooms }}** vacant rooms have **{{ metrics.available_beds }}** available beds, representing an potential monthly rent roll value of **{{ settings.currency }}{{ "{:,}".format(metrics.available_beds * 12000) }}**.
                                </p>
                            </div>
                            
                            <div class="mt-6 pt-4 border-t border-slate-800/80">
                                <button onclick="switchTab('rooms')" class="w-full py-2.5 bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500 text-slate-950 font-bold rounded-xl text-xs hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 shadow-md">
                                    View Occupancy Heat Map
                                </button>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Tab 2: Students Directory -->
                <section id="tab-directory" class="hidden space-y-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-lg font-bold text-white">Student Enrollment Console</h3>
                            <p class="text-xs text-slate-400">View active resident directory profiles, toggle billing states, and add new residents.</p>
                        </div>
                        
                        <div class="flex items-center space-x-3">
                            <button onclick="toggleRegisterForm()" id="register-toggle-btn" class="px-4 py-2 bg-gradient-to-r from-amber-400 to-orange-500 text-slate-950 font-bold rounded-xl text-xs flex items-center space-x-2 transition-all">
                                <i data-lucide="user-plus" class="w-4 h-4"></i>
                                <span>Register Resident</span>
                            </button>
                        </div>
                    </div>

                    <!-- Hidden Register Form Module (Toggled on button click) -->
                    <div id="register-form-module" class="hidden max-w-4xl mx-auto bg-slate-900/50 border border-amber-500/10 rounded-2xl p-8 gold-glow">
                        <div class="mb-6 border-b border-slate-800/80 pb-4">
                            <h4 class="text-base font-bold text-white flex items-center space-x-2">
                                <i data-lucide="user-plus" class="text-amber-500"></i>
                                <span>New Resident Registration Form</span>
                            </h4>
                        </div>

                        <form action="/register" method="POST" class="space-y-6">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <!-- Full Name -->
                                <div>
                                    <label for="name" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Full Name</label>
                                    <input type="text" id="name" name="name" required placeholder="Alex Mercer" class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white placeholder-slate-700">
                                </div>
                                
                                <!-- Mobile Number -->
                                <div>
                                    <label for="mobile" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Mobile Number</label>
                                    <input type="tel" id="mobile" name="mobile" required placeholder="+91 98765 43210" class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white placeholder-slate-700">
                                </div>

                                <!-- Email -->
                                <div>
                                    <label for="email" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Email Address</label>
                                    <input type="email" id="email" name="email" required placeholder="alex.mercer@apex.edu" class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white placeholder-slate-700">
                                </div>

                                <!-- Course -->
                                <div>
                                    <label for="course" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Course Name</label>
                                    <input type="text" id="course" name="course" required placeholder="Data Analytics" class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white placeholder-slate-700">
                                </div>

                                <!-- Room -->
                                <div>
                                    <label for="room" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Room Assignment</label>
                                    <input type="text" id="room" name="room" required placeholder="102" class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white placeholder-slate-700">
                                </div>

                                <!-- Floor -->
                                <div>
                                    <label for="floor" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Floor</label>
                                    <select id="floor" name="floor" required class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white">
                                        <option value="Ground">Ground Floor</option>
                                        <option value="1st">1st Floor</option>
                                        <option value="2nd">2nd Floor</option>
                                    </select>
                                </div>

                                <!-- Block -->
                                <div>
                                    <label for="block" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Block</label>
                                    <select id="block" name="block" required class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white">
                                        <option value="Block A">Block A</option>
                                        <option value="Block B">Block B</option>
                                        <option value="Block C">Block C</option>
                                    </select>
                                </div>

                                <!-- Rent -->
                                <div>
                                    <label for="rent" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Monthly Rent</label>
                                    <input type="number" id="rent" name="rent" required placeholder="12000" class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white placeholder-slate-700">
                                </div>

                                <!-- Payment Status -->
                                <div>
                                    <label for="payment_status" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Initial Payment Status</label>
                                    <select id="payment_status" name="payment_status" required class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white">
                                        <option value="Paid">Paid</option>
                                        <option value="Pending">Pending</option>
                                        <option value="Partial">Partial</option>
                                    </select>
                                </div>

                                <!-- Admission Date -->
                                <div>
                                    <label for="admission_date" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Admission Date</label>
                                    <input type="date" id="admission_date" name="admission_date" required class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white">
                                </div>

                                <div class="border-t border-slate-800 md:col-span-2 my-2"></div>

                                <!-- Guardian Name -->
                                <div>
                                    <label for="guardian_name" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Guardian Full Name</label>
                                    <input type="text" id="guardian_name" name="guardian_name" required placeholder="Richard Mercer" class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white placeholder-slate-700">
                                </div>

                                <!-- Guardian Mobile -->
                                <div>
                                    <label for="guardian_contact" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Guardian Contact</label>
                                    <input type="tel" id="guardian_contact" name="guardian_contact" required placeholder="+91 98765 43211" class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white placeholder-slate-700">
                                </div>
                            </div>

                            <div class="flex items-center justify-end space-x-4 border-t border-slate-800/80 pt-6">
                                <button type="reset" class="px-5 py-2.5 bg-slate-800 hover:bg-slate-750 text-slate-300 font-bold rounded-xl text-xs transition-all">
                                    Reset Form
                                </button>
                                <button type="submit" class="px-7 py-2.5 bg-gradient-to-r from-amber-400 to-orange-500 text-slate-950 font-extrabold rounded-xl text-xs hover:scale-[1.02] active:scale-[0.98] transition-all shadow-md shadow-amber-500/10">
                                    Register Student
                                </button>
                            </div>
                        </form>
                    </div>

                    <!-- Directory list table container -->
                    <div class="bg-slate-900/40 border border-amber-500/10 rounded-2xl p-6 gold-glow">
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                            <!-- Search -->
                            <div class="relative md:col-span-2">
                                <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                                    <i data-lucide="search" class="w-4 h-4"></i>
                                </span>
                                <input type="text" id="search-input" oninput="filterTable()" placeholder="Search directory..." class="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white placeholder-slate-600">
                            </div>
                            
                            <!-- Status filter -->
                            <div>
                                <select id="filter-status" onchange="filterTable()" class="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white">
                                    <option value="All">All Statuses</option>
                                    <option value="Paid">Paid</option>
                                    <option value="Pending">Pending</option>
                                    <option value="Partial">Partial</option>
                                    <option value="Checked Out">Checked Out</option>
                                </select>
                            </div>

                            <!-- Block filter -->
                            <div>
                                <select id="filter-block" onchange="filterTable()" class="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-amber-500/50 transition-all text-white">
                                    <option value="All">All Blocks</option>
                                    <option value="Block A">Block A</option>
                                    <option value="Block B">Block B</option>
                                    <option value="Block C">Block C</option>
                                </select>
                            </div>
                        </div>

                        <!-- Table -->
                        <div class="overflow-x-auto">
                            <table class="w-full border-collapse text-left">
                                <thead>
                                    <tr class="border-b border-slate-800 text-[10px] font-bold text-slate-400 uppercase tracking-wider bg-slate-950/40">
                                        <th class="px-6 py-4">ID</th>
                                        <th class="px-6 py-4">Resident</th>
                                        <th class="px-6 py-4">Location</th>
                                        <th class="px-6 py-4">Mobile & Guardian</th>
                                        <th class="px-6 py-4">Course</th>
                                        <th class="px-6 py-4">Rent</th>
                                        <th class="px-6 py-4">Payment</th>
                                        <th class="px-6 py-4">Occupancy</th>
                                        <th class="px-6 py-4 text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800/40" id="table-body">
                                    {% for student in students %}
                                    <tr class="student-row hover:bg-slate-900/20 transition-colors duration-200"
                                        data-name="{{ student.name }}"
                                        data-email="{{ student.email }}"
                                        data-course="{{ student.course }}"
                                        data-room="{{ student.room }}"
                                        data-block="{{ student.block }}"
                                        data-status="{{ student.payment_status }}"
                                        data-occupancy="{{ student.occupancy }}">
                                        
                                        <!-- ID -->
                                        <td class="px-6 py-4 text-xs font-mono text-slate-500">
                                            #HH-{{ "%03d"|format(student.id) }}
                                        </td>
                                        
                                        <!-- Profile details -->
                                        <td class="px-6 py-4">
                                            <div class="flex items-center space-x-3">
                                                <div class="h-9 w-9 rounded-xl bg-gradient-to-br from-amber-400/20 to-orange-500/20 flex items-center justify-center border border-amber-500/25 shadow-[0_0_10px_rgba(251,191,36,0.03)]">
                                                    <span class="text-xs font-black text-amber-400">
                                                        {{ student.name.split(' ')[0][0] if student.name.split(' ')|length > 0 else 'S' }}{{ student.name.split(' ')[1][0] if student.name.split(' ')|length > 1 else '' }}
                                                    </span>
                                                </div>
                                                <div>
                                                    <h4 class="text-sm font-semibold text-white">{{ student.name }}</h4>
                                                    <span class="text-[11px] text-slate-400 block">{{ student.email }}</span>
                                                </div>
                                            </div>
                                        </td>
                                        
                                        <!-- Location -->
                                        <td class="px-6 py-4">
                                            {% if student.occupancy == 'Active' %}
                                            <div class="flex items-center space-x-1.5">
                                                <i data-lucide="key" class="w-3.5 h-3.5 text-amber-500/50"></i>
                                                <span class="text-xs font-bold text-white">{{ student.block }} - Room {{ student.room }}</span>
                                            </div>
                                            <span class="text-[11px] text-slate-400 block ml-5">{{ student.floor }} Floor</span>
                                            {% else %}
                                            <span class="text-xs font-bold text-slate-500">Unassigned</span>
                                            {% endif %}
                                        </td>
                                        
                                        <!-- Contact details -->
                                        <td class="px-6 py-4">
                                            <span class="text-xs text-slate-300 block font-semibold">{{ student.mobile }}</span>
                                            <span class="text-[10px] text-slate-500 block">Guardian: {{ student.guardian_name }}</span>
                                        </td>
                                        
                                        <!-- Course -->
                                        <td class="px-6 py-4 text-xs font-semibold text-slate-300">
                                            {{ student.course }}
                                        </td>
                                        
                                        <!-- Rent -->
                                        <td class="px-6 py-4 text-xs font-bold text-white">
                                            {{ settings.currency }}{{ "{:,}".format(student.rent) }}
                                        </td>
                                        
                                        <!-- Payment Badges -->
                                        <td class="px-6 py-4">
                                            {% if student.payment_status == 'Paid' %}
                                            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.05)]">
                                                Paid
                                            </span>
                                            {% elif student.payment_status == 'Pending' %}
                                            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20 shadow-[0_0_15px_rgba(244,63,94,0.05)]">
                                                Pending
                                            </span>
                                            {% else %}
                                            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20 shadow-[0_0_15px_rgba(245,158,11,0.05)]">
                                                Partial
                                            </span>
                                            {% endif %}
                                        </td>
                                        
                                        <!-- Occupancy state -->
                                        <td class="px-6 py-4">
                                            {% if student.occupancy == 'Active' %}
                                            <span class="text-xs text-emerald-400 font-bold flex items-center space-x-1.5">
                                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block"></span>
                                                <span>Active</span>
                                            </span>
                                            {% else %}
                                            <span class="text-xs text-slate-500 font-semibold flex items-center space-x-1.5">
                                                <span class="w-1.5 h-1.5 rounded-full bg-slate-700 inline-block"></span>
                                                <span>Inactive</span>
                                            </span>
                                            {% endif %}
                                        </td>
                                        
                                        <!-- Action buttons -->
                                        <td class="px-6 py-4 text-right">
                                            <div class="flex items-center justify-end space-x-2">
                                                <!-- View Profile -->
                                                <a href="/student/{{ student.id }}" title="View Profile" class="h-8 w-8 rounded-lg bg-slate-950 hover:bg-slate-800 flex items-center justify-center border border-slate-800 hover:border-amber-500/30 text-amber-400 hover:text-amber-300 transition-colors">
                                                    <i data-lucide="eye" class="w-3.5 h-3.5"></i>
                                                </a>
                                                <!-- Toggle Payment -->
                                                <form action="/toggle_payment/{{ student.id }}" method="POST" class="inline">
                                                    <button type="submit" title="Toggle Payment Status" class="h-8 w-8 rounded-lg bg-slate-950 hover:bg-slate-800 flex items-center justify-center border border-slate-800 hover:border-amber-500/30 text-emerald-400 hover:text-emerald-300 transition-colors">
                                                        <i data-lucide="credit-card" class="w-3.5 h-3.5"></i>
                                                    </button>
                                                </form>
                                                <!-- Deallocate Room -->
                                                <form action="/deallocate/{{ student.id }}" method="POST" class="inline">
                                                    <button type="submit" title="Toggle Occupancy" class="h-8 w-8 rounded-lg bg-slate-950 hover:bg-slate-800 flex items-center justify-center border border-slate-800 hover:border-amber-500/30 text-sky-400 hover:text-sky-300 transition-colors">
                                                        <i data-lucide="log-out" class="w-3.5 h-3.5"></i>
                                                    </button>
                                                </form>
                                                <!-- Delete student -->
                                                <form action="/delete/{{ student.id }}" method="POST" class="inline" onsubmit="return confirm('Are you sure you want to delete this resident from the system registry?');">
                                                    <button type="submit" title="Delete Profile" class="h-8 w-8 rounded-lg bg-slate-950 hover:bg-rose-950/50 flex items-center justify-center border border-slate-800 hover:border-rose-900 text-rose-400 hover:text-rose-300 transition-colors">
                                                        <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                                                    </button>
                                                </form>
                                            </div>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </section>

                <!-- Tab 3: Smart Room Layout Floor Plan (NEW Centerpiece Module) -->
                <section id="tab-rooms" class="hidden space-y-6">
                    
                    <!-- Rooms Analytics ribbon -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div class="bg-slate-900/50 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
                            <div>
                                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block">Total Rooms</span>
                                <span class="text-xl font-extrabold text-white mt-1 block">{{ metrics.total_rooms }} Rooms</span>
                            </div>
                            <div class="h-9 w-9 rounded-lg bg-slate-950 flex items-center justify-center border border-slate-800 text-slate-400"><i data-lucide="key" class="w-4 h-4"></i></div>
                        </div>
                        <div class="bg-slate-900/50 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
                            <div>
                                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block">Allocated / Occupied</span>
                                <span class="text-xl font-extrabold text-amber-400 mt-1 block">{{ metrics.occupied_rooms }} Rooms</span>
                            </div>
                            <div class="h-9 w-9 rounded-lg bg-slate-950 flex items-center justify-center border border-slate-800 text-amber-400"><i data-lucide="user-check" class="w-4 h-4"></i></div>
                        </div>
                        <div class="bg-slate-900/50 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
                            <div>
                                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block">Fully Vacant</span>
                                <span class="text-xl font-extrabold text-emerald-400 mt-1 block">{{ metrics.vacant_rooms }} Rooms</span>
                            </div>
                            <div class="h-9 w-9 rounded-lg bg-slate-950 flex items-center justify-center border border-slate-800 text-emerald-400"><i data-lucide="door-open" class="w-4 h-4"></i></div>
                        </div>
                        <div class="bg-slate-900/50 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
                            <div>
                                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block">Maintenance Rooms</span>
                                <span class="text-xl font-extrabold text-purple-400 mt-1 block">{{ metrics.maintenance_rooms }} Rooms</span>
                            </div>
                            <div class="h-9 w-9 rounded-lg bg-slate-950 flex items-center justify-center border border-slate-800 text-purple-400"><i data-lucide="wrench" class="w-4 h-4"></i></div>
                        </div>
                    </div>

                    <!-- Occupancy Heat Map Grid -->
                    <div class="bg-slate-900/40 border border-amber-500/10 rounded-2xl p-6 gold-glow space-y-4">
                        <div class="flex justify-between items-center">
                            <div>
                                <h3 class="text-sm font-extrabold text-white uppercase tracking-wider">Property Occupancy Heat Map</h3>
                                <p class="text-[10px] text-slate-500 font-semibold mt-0.5">Quick building status visual grid (Hover cells to view info / Click to open Modal)</p>
                            </div>
                            
                            <!-- Legend indicators -->
                            <div class="flex items-center space-x-4 text-[10px] font-bold text-slate-400">
                                <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 bg-emerald-500/20 border border-emerald-500/40 rounded"></span><span>Available</span></span>
                                <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 bg-amber-500/20 border border-amber-500/40 rounded"></span><span>Partial</span></span>
                                <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 bg-rose-500/20 border border-rose-500/40 rounded"></span><span>Full</span></span>
                                <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 bg-purple-500/20 border border-purple-500/40 rounded"></span><span>Maint.</span></span>
                            </div>
                        </div>
                        
                        <!-- Heat map grid layout -->
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-2">
                            {% for blk in ["Block A", "Block B", "Block C"] %}
                            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
                                <h4 class="text-xs font-bold text-amber-500 uppercase tracking-widest mb-3 text-center">{{ blk }}</h4>
                                <div class="grid grid-cols-10 gap-1.5" id="heatmap-{{ blk.replace(' ', '') }}">
                                    <!-- Javascript will generate map boxes here -->
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                    <!-- Floor Plan building structure cards -->
                    <div class="bg-slate-900/40 border border-amber-500/10 rounded-2xl p-6 gold-glow space-y-6">
                        
                        <!-- Block layout filters -->
                        <div class="flex items-center justify-between border-b border-slate-800/80 pb-4">
                            <div>
                                <h3 class="text-base font-extrabold text-white">Interactive Floor Plans</h3>
                                <p class="text-xs text-slate-400">Filter layout layout view by building blocks.</p>
                            </div>
                            <div class="flex bg-slate-950 p-1 border border-slate-800 rounded-xl space-x-1">
                                <button onclick="switchBlock('Block A')" id="btn-block-a" class="px-4 py-1.5 text-xs font-bold uppercase rounded-lg transition-all">Block A</button>
                                <button onclick="switchBlock('Block B')" id="btn-block-b" class="px-4 py-1.5 text-xs font-bold uppercase rounded-lg transition-all">Block B</button>
                                <button onclick="switchBlock('Block C')" id="btn-block-c" class="px-4 py-1.5 text-xs font-bold uppercase rounded-lg transition-all">Block C</button>
                            </div>
                        </div>

                        <!-- Floors container -->
                        <div class="space-y-10" id="floors-container">
                            {% for fl in ["Ground", "1st", "2nd"] %}
                            <div class="space-y-4">
                                <div class="flex items-center space-x-3">
                                    <h4 class="text-sm font-extrabold text-white uppercase tracking-wider">{{ fl }} Floor</h4>
                                    <div class="flex-grow h-[1px] bg-slate-800/80"></div>
                                </div>
                                
                                <!-- Room grid -->
                                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                                    {% for room in rooms %}
                                        <!-- Filter rooms to match this floor and selected block in JS -->
                                        <div class="room-plan-card" data-block="{{ room.block }}" data-floor="{{ room.floor }}" data-room="{{ room.room_number }}">
                                            <!-- Dynamically render cards based on room state -->
                                            <div onclick="openRoomModal('{{ room.block }}', '{{ room.room_number }}')" 
                                                 class="relative cursor-pointer overflow-hidden rounded-2xl bg-slate-950/60 backdrop-blur-xl border p-4 transition-all duration-300 hover:scale-[1.03] hover:shadow-lg group
                                                 {% if room.status == 'Maintenance' %} border-purple-500/20 hover:border-purple-500/50 shadow-[0_0_15px_rgba(168,85,247,0.03)]
                                                 {% elif room.occupied_beds == 0 %} border-emerald-500/20 hover:border-emerald-500/50 shadow-[0_0_15px_rgba(16,185,129,0.03)]
                                                 {% elif room.occupied_beds >= room.capacity %} border-rose-500/20 hover:border-rose-500/50 shadow-[0_0_15px_rgba(244,63,94,0.03)]
                                                 {% else %} border-amber-500/20 hover:border-amber-500/50 shadow-[0_0_15px_rgba(245,158,11,0.03)]
                                                 {% endif %}">
                                                
                                                <!-- Pulse dot status badge -->
                                                <div class="absolute top-4 right-4 flex h-2.5 w-2.5">
                                                    {% if room.status == 'Maintenance' %}
                                                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
                                                    <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-purple-500 pulse-purple"></span>
                                                    {% elif room.occupied_beds == 0 %}
                                                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                                                    <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500 pulse-emerald"></span>
                                                    {% elif room.occupied_beds >= room.capacity %}
                                                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                                                    <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-500 pulse-rose"></span>
                                                    {% else %}
                                                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                                                    <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500 pulse-amber"></span>
                                                    {% endif %}
                                                </div>

                                                <!-- Room Header -->
                                                <div class="flex items-center justify-between mb-3">
                                                    <span class="text-sm font-extrabold text-white">Room {{ room.room_number }}</span>
                                                </div>

                                                <div class="space-y-1.5 text-[11px] text-slate-400">
                                                    <div class="flex justify-between">
                                                        <span>Capacity</span>
                                                        <span class="font-bold text-slate-200">{{ room.capacity }} beds</span>
                                                    </div>
                                                    <div class="flex justify-between">
                                                        <span>Occupied</span>
                                                        <span class="font-bold text-slate-200">{{ room.occupied_beds }} beds</span>
                                                    </div>
                                                    <div class="flex justify-between">
                                                        <span>Available</span>
                                                        <span class="font-bold {% if room.available_beds > 0 %}text-emerald-400{% else %}text-slate-500{% endif %}">{{ room.available_beds }} vacant</span>
                                                    </div>
                                                </div>

                                                <div class="border-t border-slate-900 my-3"></div>

                                                <div class="flex items-center justify-between text-[11px]">
                                                    <span class="text-[9px] text-slate-500 font-bold uppercase tracking-wider">Revenue</span>
                                                    <span class="font-black text-amber-400">{{ settings.currency }}{{ "{:,}".format(room.monthly_revenue) }}/mo</span>
                                                </div>
                                            </div>
                                        </div>
                                    {% endfor %}
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </section>

                <!-- Tab 4: Analytics View -->
                <section id="tab-analytics" class="hidden space-y-8">
                    <!-- Progress Card layout -->
                    <div class="bg-slate-900/40 border border-amber-500/10 rounded-2xl p-6 gold-glow space-y-8">
                        <h3 class="text-base font-extrabold text-white uppercase tracking-wider flex items-center space-x-2 border-b border-slate-800 pb-3">
                            <i data-lucide="line-chart" class="text-amber-500"></i>
                            <span>Detailed Utilization Analyses</span>
                        </h3>
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <!-- Utilization beds progress -->
                            <div class="space-y-3">
                                <div class="flex justify-between items-center text-xs font-bold text-slate-300">
                                    <span>Bed Occupancy Progress</span>
                                    <span class="text-amber-400">{{ metrics.occupied_beds }} / {{ metrics.total_beds }} Beds</span>
                                </div>
                                <div class="w-full bg-slate-950 h-5 rounded-full overflow-hidden p-0.5 border border-slate-800">
                                    <div class="bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500 h-full rounded-full transition-all duration-700" style="width: {{ metrics.occupancy_rate }}%"></div>
                                </div>
                                <span class="text-[10px] text-slate-500 font-semibold block">Total beds count assigned to active students.</span>
                            </div>

                            <!-- Utilization revenue collection progress -->
                            <div class="space-y-3">
                                <div class="flex justify-between items-center text-xs font-bold text-slate-300">
                                    <span>Revenue Collection Performance</span>
                                    <span class="text-emerald-400">{{ settings.currency }}{{ "{:,}".format(metrics.revenue_collected) }} / {{ settings.currency }}{{ "{:,}".format(metrics.total_revenue_generated) }}</span>
                                </div>
                                <div class="w-full bg-slate-950 h-5 rounded-full overflow-hidden p-0.5 border border-slate-800">
                                    <div class="bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-400 h-full rounded-full transition-all duration-700" style="width: {{ metrics.collection_rate }}%"></div>
                                </div>
                                <span class="text-[10px] text-slate-500 font-semibold block">Calculated collection rate of paid and partially paid records.</span>
                            </div>
                        </div>
                    </div>

                    <!-- Block-wise Utilization Analytics -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {% for blk in ["Block A", "Block B", "Block C"] %}
                        <div class="bg-slate-900/40 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
                            <div>
                                <h4 class="text-xs font-bold text-amber-500 uppercase tracking-widest mb-4 border-b border-slate-800 pb-2">{{ blk }} Performance</h4>
                                <div class="space-y-3">
                                    <!-- Calculate block metrics inside JS dynamically or render placeholders -->
                                    <div class="flex justify-between text-xs py-1 border-b border-slate-900">
                                        <span class="text-slate-400">Total Rooms</span>
                                        <span class="text-white font-bold">30 Rooms</span>
                                    </div>
                                    <div class="flex justify-between text-xs py-1 border-b border-slate-900">
                                        <span class="text-slate-400">Bed Capacity</span>
                                        <span class="text-white font-bold">90 Beds</span>
                                    </div>
                                    <div class="flex justify-between text-xs py-1">
                                        <span class="text-slate-400">Active Residents</span>
                                        <span class="text-amber-400 font-bold" id="resident-count-{{ blk.replace(' ', '') }}">0</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-6">
                                <div class="w-full bg-slate-950 h-2 rounded-full overflow-hidden p-0.5 border border-slate-800">
                                    <div class="bg-amber-400 h-full rounded-full" id="progress-bar-{{ blk.replace(' ', '') }}" style="width: 0%"></div>
                                </div>
                                <span class="text-[10px] text-slate-500 mt-1 block" id="progress-text-{{ blk.replace(' ', '') }}">0% Occupancy</span>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </section>

                <!-- Tab 5: Payments View -->
                <section id="tab-payments" class="hidden space-y-6">
                    
                    <!-- Billing Ribbon metrics -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="bg-slate-900/50 border border-slate-800 rounded-2xl p-5 flex items-center justify-between">
                            <div>
                                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block">Total Billing Roll</span>
                                <span class="text-2xl font-extrabold text-white mt-1 block">{{ settings.currency }}{{ "{:,}".format(metrics.total_revenue_generated) }}</span>
                            </div>
                            <div class="h-10 w-10 rounded-xl bg-slate-950 flex items-center justify-center border border-slate-800 text-slate-400"><i data-lucide="piggy-bank" class="w-5 h-5"></i></div>
                        </div>
                        <div class="bg-slate-900/50 border border-slate-800 rounded-2xl p-5 flex items-center justify-between">
                            <div>
                                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block">Collected Revenue</span>
                                <span class="text-2xl font-extrabold text-emerald-400 mt-1 block">{{ settings.currency }}{{ "{:,}".format(metrics.revenue_collected) }}</span>
                            </div>
                            <div class="h-10 w-10 rounded-xl bg-slate-950 flex items-center justify-center border border-slate-800 text-emerald-400"><i data-lucide="check-circle" class="w-5 h-5"></i></div>
                        </div>
                        <div class="bg-slate-900/50 border border-slate-800 rounded-2xl p-5 flex items-center justify-between">
                            <div>
                                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block">Pending Receivables</span>
                                <span class="text-2xl font-extrabold text-rose-400 mt-1 block">{{ settings.currency }}{{ "{:,}".format(metrics.pending_dues) }}</span>
                            </div>
                            <div class="h-10 w-10 rounded-xl bg-slate-950 flex items-center justify-center border border-slate-800 text-rose-400"><i data-lucide="help-circle" class="w-5 h-5"></i></div>
                        </div>
                    </div>

                    <!-- Outstanding Invoices List -->
                    <div class="bg-slate-900/40 border border-amber-500/10 rounded-2xl p-6 gold-glow">
                        <div class="mb-6 flex justify-between items-center">
                            <div>
                                <h3 class="text-sm font-extrabold text-white uppercase tracking-wider">Outstanding Payment Log</h3>
                                <p class="text-xs text-slate-400">Outstanding student balances requiring review.</p>
                            </div>
                        </div>
                        
                        <div class="overflow-x-auto">
                            <table class="w-full border-collapse text-left">
                                <thead>
                                    <tr class="border-b border-slate-800 text-[10px] font-bold text-slate-400 uppercase tracking-wider bg-slate-950/40">
                                        <th class="px-6 py-3">Resident</th>
                                        <th class="px-6 py-3">Location</th>
                                        <th class="px-6 py-3">Contact</th>
                                        <th class="px-6 py-3">Monthly Rent</th>
                                        <th class="px-6 py-3">Status</th>
                                        <th class="px-6 py-3 text-right">Invoice Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% set pending_count = namespace(value=0) %}
                                    {% for student in students %}
                                        {% if student.occupancy == 'Active' and (student.payment_status == 'Pending' or student.payment_status == 'Partial') %}
                                        {% set pending_count.value = pending_count.value + 1 %}
                                        <tr class="hover:bg-slate-900/20 border-b border-slate-800/40">
                                            <td class="px-6 py-3">
                                                <h4 class="text-xs font-semibold text-white">{{ student.name }}</h4>
                                                <span class="text-[10px] text-slate-500">{{ student.email }}</span>
                                            </td>
                                            <td class="px-6 py-3 text-xs font-semibold text-slate-300">
                                                {{ student.block }} - Room {{ student.room }}
                                            </td>
                                            <td class="px-6 py-3 text-xs text-slate-400">
                                                {{ student.mobile }}
                                            </td>
                                            <td class="px-6 py-3 text-xs font-bold text-white">
                                                {{ settings.currency }}{{ "{:,}".format(student.rent) }}
                                            </td>
                                            <td class="px-6 py-3">
                                                {% if student.payment_status == 'Pending' %}
                                                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[9px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20 animate-pulse">Pending</span>
                                                {% else %}
                                                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[9px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">Partial</span>
                                                {% endif %}
                                            </td>
                                            <td class="px-6 py-3 text-right">
                                                <form action="/toggle_payment/{{ student.id }}" method="POST" class="inline">
                                                    <button type="submit" class="px-3 py-1 bg-slate-950 border border-slate-800 hover:border-emerald-500/30 text-emerald-400 font-bold rounded-lg text-[10px] transition-all">
                                                        Mark Paid
                                                    </button>
                                                </form>
                                            </td>
                                        </tr>
                                        {% endif %}
                                    {% endfor %}
                                    
                                    {% if pending_count.value == 0 %}
                                    <tr>
                                        <td colspan="6" class="px-6 py-8 text-center text-xs text-slate-500 font-semibold">
                                            <i data-lucide="check-circle" class="w-8 h-8 text-emerald-500 mx-auto mb-2 opacity-50"></i>
                                            All accounts currently up-to-date. Zero outstanding dues.
                                        </td>
                                    </tr>
                                    {% endif %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </section>

                <!-- Tab 6: System Settings -->
                <section id="tab-settings" class="hidden max-w-4xl mx-auto space-y-6">
                    <div class="bg-slate-900/40 border border-amber-500/10 rounded-2xl p-6 gold-glow space-y-6">
                        <h3 class="text-base font-extrabold text-white uppercase tracking-wider flex items-center space-x-2 border-b border-slate-800 pb-3">
                            <i data-lucide="settings" class="text-amber-500"></i>
                            <span>System Configuration</span>
                        </h3>
                        
                        <form action="/update_settings" method="POST" class="space-y-6">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <label for="property_name" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Hostel / Hotel Name</label>
                                    <input type="text" id="property_name" name="property_name" value="{{ settings.property_name }}" required class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-amber-500/50 transition-all">
                                </div>
                                
                                <div>
                                    <label for="currency" class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Default Currency</label>
                                    <select id="currency" name="currency" class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-amber-500/50 transition-all">
                                        <option value="₹" {% if settings.currency == '₹' %}selected{% endif %}>₹ (Indian Rupee)</option>
                                        <option value="$" {% if settings.currency == '$' %}selected{% endif %}>$ (US Dollar)</option>
                                        <option value="€" {% if settings.currency == '€' %}selected{% endif %}>€ (Euro)</option>
                                        <option value="£" {% if settings.currency == '£' %}selected{% endif %}>£ (Pound Sterling)</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="flex justify-end border-t border-slate-800/80 pt-6">
                                <button type="submit" class="px-6 py-2.5 bg-gradient-to-r from-amber-400 to-orange-500 text-slate-950 font-extrabold rounded-xl text-xs hover:scale-[1.02] active:scale-[0.98] transition-all shadow-md shadow-amber-500/10">
                                    Save Configurations
                                </button>
                            </div>
                        </form>
                    </div>

                    <!-- Database Resets card -->
                    <div class="bg-slate-900/40 border border-slate-800 rounded-2xl p-6 space-y-4">
                        <h4 class="text-xs font-bold text-rose-500 uppercase tracking-wider">System Reset Options</h4>
                        <p class="text-xs text-slate-400">Restore all student allocations, payments, and configurations to preloaded factory defaults.</p>
                        
                        <form action="/reset_system" method="POST" onsubmit="return confirm('Warning: This will clear all changes and restore default database state!');">
                            <button type="submit" class="px-5 py-2.5 bg-slate-950 border border-rose-900 hover:bg-rose-950/40 text-rose-400 font-bold rounded-xl text-xs transition-all">
                                Restore Defaults
                            </button>
                        </form>
                    </div>
                </section>
            </main>
        </div>
    </div>

    <!-- Smart Room Action Modal (Hidden by default) -->
    <div id="room-modal" class="fixed inset-0 z-50 hidden flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm" onclick="closeRoomModal()"></div>
        
        <div class="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 z-10 max-h-[90vh] overflow-y-auto gold-glow">
            <button onclick="closeRoomModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors">
                <i data-lucide="x" class="w-5 h-5"></i>
            </button>
            
            <div class="mb-5 border-b border-slate-800/60 pb-3">
                <h3 class="text-base font-extrabold text-white flex items-center space-x-2">
                    <i data-lucide="key" class="text-amber-500"></i>
                    <span id="modal-room-title">Room 101</span>
                </h3>
                <p id="modal-room-subtitle" class="text-[11px] text-slate-500 font-bold uppercase tracking-wide mt-1">Block A - Ground Floor</p>
            </div>

            <!-- Current Occupants list -->
            <div class="mb-6">
                <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2.5">Current Occupants</h4>
                <div id="modal-occupants-list" class="space-y-3">
                    <!-- Javascript injected occupants -->
                </div>
            </div>

            <div class="border-t border-slate-800/80 my-5"></div>

            <!-- Modal Action inputs -->
            <div>
                <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Allocation & Operations</h4>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Form 1: Allocate -->
                    <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
                        <div>
                            <h5 class="text-xs font-bold text-white uppercase tracking-wide mb-1">Allocate Bed</h5>
                            <p class="text-[10px] text-slate-500 mb-3">Place a vacant student into this room.</p>
                        </div>
                        
                        <form action="/allocate_room" method="POST" class="space-y-3">
                            <input type="hidden" name="block" id="alloc-block">
                            <input type="hidden" name="room" id="alloc-room">
                            <input type="hidden" name="floor" id="alloc-floor">
                            
                            <select name="student_id" id="alloc-student-select" required class="w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-300 focus:outline-none focus:border-amber-500/50">
                                <!-- JS injected options -->
                            </select>
                            
                            <button type="submit" class="w-full py-2 bg-gradient-to-r from-amber-400 to-orange-500 text-slate-950 font-bold rounded-lg text-xs hover:scale-[1.01] transition-all">
                                Assign Student
                            </button>
                        </form>
                    </div>

                    <!-- Form 2: Transfer -->
                    <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
                        <div>
                            <h5 class="text-xs font-bold text-white uppercase tracking-wide mb-1">Transfer Occupant</h5>
                            <p class="text-[10px] text-slate-500 mb-3">Re-route occupant to another available room.</p>
                        </div>
                        
                        <form action="/transfer_student" method="POST" class="space-y-3">
                            <!-- Selected student to transfer -->
                            <select name="student_id" id="transfer-student-select" required class="w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-300 focus:outline-none focus:border-amber-500/50">
                                <!-- Occupants dropdown -->
                            </select>

                            <!-- Target rooms keys -->
                            <select name="target_room_key" id="transfer-target-select" required class="w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-300 focus:outline-none focus:border-amber-500/50">
                                <!-- Target vacant rooms -->
                            </select>
                            
                            <button type="submit" class="w-full py-2 bg-slate-850 hover:bg-slate-800 text-slate-300 border border-slate-700 font-bold rounded-lg text-xs hover:scale-[1.01] transition-all">
                                Relocate Resident
                            </button>
                        </form>
                    </div>
                </div>

                <!-- Footer quick actions -->
                <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <form action="/toggle_maintenance" method="POST" class="w-full">
                        <input type="hidden" name="block" id="maint-block">
                        <input type="hidden" name="room" id="maint-room">
                        <button type="submit" id="maint-btn-text" class="w-full py-2 bg-slate-950 border border-slate-800 hover:border-purple-500/30 text-purple-400 hover:text-purple-300 rounded-xl text-xs font-bold transition-all">
                            Mark Maintenance
                        </button>
                    </form>

                    <form action="/vacate_room" method="POST" class="w-full" onsubmit="return confirm('Confirm deallocation for all students in this room?');">
                        <input type="hidden" name="block" id="vacate-block">
                        <input type="hidden" name="room" id="vacate-room">
                        <button type="submit" class="w-full py-2 bg-slate-950 border border-slate-800 hover:border-rose-900 text-rose-400 hover:text-rose-300 rounded-xl text-xs font-bold transition-all">
                            Vacate Room (All)
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Client-Side Navigation & Layout scripts -->
    <script>
        // Core database references injected from Flask
        const studentsData = {{ students_json | safe }};
        const roomsData = {{ rooms_json | safe }};
        const currencySymbol = "{{ settings.currency }}";

        // Date layout
        const dateOptions = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
        document.getElementById('live-date').innerText = new Date().toLocaleDateString('en-US', dateOptions);
        
        const admissionInput = document.getElementById('admission_date');
        if (admissionInput && !admissionInput.value) {
            admissionInput.value = new Date().toISOString().split('T')[0];
        }

        // Active state selectors
        let activeTab = "overview";
        let activeBlock = "Block A";

        // Tab routing switcher
        function switchTab(tabId) {
            // Hide tabs
            ["overview", "directory", "rooms", "analytics", "payments", "settings"].forEach(tab => {
                const el = document.getElementById(`tab-${tab}`);
                if (el) el.classList.add('hidden');
                
                const navBtn = document.getElementById(`nav-${tab}`);
                if (navBtn) {
                    navBtn.className = "w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-xs font-bold uppercase tracking-wider text-slate-400 hover:text-slate-200 transition-all duration-200";
                }
            });

            // Show active tab
            const activeEl = document.getElementById(`tab-${tabId}`);
            if (activeEl) activeEl.classList.remove('hidden');

            const activeNav = document.getElementById(`nav-${tabId}`);
            if (activeNav) {
                activeNav.className = "w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-xs font-bold uppercase tracking-wider bg-gradient-to-r from-amber-400 to-orange-500 text-slate-950 shadow-md shadow-amber-500/15 transition-all duration-200";
            }

            // Update title
            const titlesMap = {
                overview: ["Dashboard", "Real-time statistics & capacity overview"],
                directory: ["Student Registry", "Enrolled profiles & database table"],
                rooms: ["Smart Room Plan", "Building structural layout & live bed allocation"],
                analytics: ["Utilization Analytics", "Structural occupancy & billing collection rate reports"],
                payments: ["Financial Ledger", "Collected balances & outstanding receivables"],
                settings: ["System Settings", "Configure defaults, resets & portal metrics"]
            };

            document.getElementById('page-title').innerText = titlesMap[tabId][0];
            document.getElementById('page-subtitle').innerText = titlesMap[tabId][1];

            // Push State
            const newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?tab=' + tabId;
            window.history.pushState({path:newurl}, '', newurl);
            activeTab = tabId;
        }

        // Toggles registration form drawer
        function toggleRegisterForm() {
            const formMod = document.getElementById('register-form-module');
            formMod.classList.toggle('hidden');
            if (!formMod.classList.contains('hidden')) {
                formMod.scrollIntoView({ behavior: 'smooth' });
            }
        }

        // Room Layout Block Filter switcher
        function switchBlock(blockName) {
            activeBlock = blockName;
            
            // Toggle active classes on tabs
            ["Block A", "Block B", "Block C"].forEach(blk => {
                const btn = document.getElementById(`btn-block-${blk.replace(' ', '').toLowerCase()}`);
                if (btn) {
                    if (blk === blockName) {
                        btn.className = "px-4 py-1.5 text-xs font-bold uppercase rounded-lg bg-gradient-to-r from-amber-400 to-orange-500 text-slate-950 transition-all";
                    } else {
                        btn.className = "px-4 py-1.5 text-xs font-bold uppercase rounded-lg text-slate-400 hover:text-slate-200 transition-all";
                    }
                }
            });

            // Toggle visibility on room plan cards
            const cards = document.querySelectorAll('.room-plan-card');
            cards.forEach(card => {
                if (card.getAttribute('data-block') === blockName) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        // Generates heat map grids dynamically
        function generateHeatMaps() {
            const blocksList = ["Block A", "Block B", "Block C"];
            
            blocksList.forEach(blk => {
                const blockRooms = roomsData.filter(r => r.block === blk);
                // Sort by Room Number numerical value
                blockRooms.sort((a,b) => parseInt(a.room_number) - parseInt(b.room_number));
                
                const container = document.getElementById(`heatmap-${blk.replace(' ', '')}`);
                if (!container) return;
                
                container.innerHTML = "";
                
                blockRooms.forEach(room => {
                    const cell = document.createElement('div');
                    cell.className = "h-5 rounded cursor-pointer transition-all duration-300 hover:scale-125 border ";
                    
                    // Colors
                    if (room.status === 'Maintenance') {
                        cell.className += "bg-purple-500/20 border-purple-500/40 hover:bg-purple-500/40";
                    } else if (room.occupied_beds === 0) {
                        cell.className += "bg-emerald-500/20 border-emerald-500/40 hover:bg-emerald-500/40";
                    } else if (room.occupied_beds >= room.capacity) {
                        cell.className += "bg-rose-500/20 border-rose-500/40 hover:bg-rose-500/40";
                    } else {
                        cell.className += "bg-amber-500/20 border-amber-500/40 hover:bg-amber-500/40";
                    }
                    
                    // Tooltip
                    let tipText = `Room ${room.room_number} (${room.occupied_beds}/${room.capacity} Beds)`;
                    if (room.status === 'Maintenance') tipText += " - Maintenance";
                    cell.title = tipText;
                    
                    cell.onclick = () => openRoomModal(room.block, room.room_number);
                    container.appendChild(cell);
                });
            });
        }

        // Open Room details modal
        function openRoomModal(block, roomNumber) {
            const room = roomsData.find(r => r.block === block && r.room_number === roomNumber);
            if (!room) return;
            
            // Modal header
            document.getElementById('modal-room-title').innerText = `Room ${room.room_number}`;
            document.getElementById('modal-room-subtitle').innerText = `${room.block} - ${room.floor} Floor`;
            
            // Hidden forms values
            document.getElementById('alloc-block').value = block;
            document.getElementById('alloc-room').value = roomNumber;
            document.getElementById('alloc-floor').value = room.floor;
            
            document.getElementById('transfer-src-block').value = block;
            document.getElementById('transfer-src-room').value = roomNumber;
            
            document.getElementById('maint-block').value = block;
            document.getElementById('maint-room').value = roomNumber;
            
            document.getElementById('vacate-block').value = block;
            document.getElementById('vacate-room').value = roomNumber;

            // Mark Maintenance toggle text
            const maintText = document.getElementById('maint-btn-text');
            if (room.status === 'Maintenance') {
                maintText.innerText = "Mark Room Active";
                maintText.className = "w-full py-2 bg-slate-950 border border-slate-800 hover:border-emerald-500/30 text-emerald-400 hover:text-emerald-300 rounded-xl text-xs font-bold transition-all";
            } else {
                maintText.innerText = "Mark Maintenance";
                maintText.className = "w-full py-2 bg-slate-950 border border-slate-800 hover:border-purple-500/30 text-purple-400 hover:text-purple-300 rounded-xl text-xs font-bold transition-all";
            }
            
            // Occupants list injection
            const listContainer = document.getElementById('modal-occupants-list');
            listContainer.innerHTML = "";
            
            if (room.occupants.length === 0) {
                listContainer.innerHTML = `
                    <div class="p-4 bg-slate-950 rounded-xl border border-slate-800/80 text-center text-xs text-slate-500 font-semibold">
                        Zero residents currently allocated in this room.
                    </div>
                `;
            } else {
                room.occupants.forEach(occ => {
                    const item = document.createElement('div');
                    item.className = "p-3.5 bg-slate-950 rounded-xl border border-slate-850 flex items-center justify-between";
                    
                    let statusBadge = "";
                    if (occ.payment_status === 'Paid') {
                        statusBadge = `<span class="px-2 py-0.5 rounded-full text-[9px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Paid</span>`;
                    } else if (occ.payment_status === 'Pending') {
                        statusBadge = `<span class="px-2 py-0.5 rounded-full text-[9px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20">Pending</span>`;
                    } else {
                        statusBadge = `<span class="px-2 py-0.5 rounded-full text-[9px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">Partial</span>`;
                    }

                    item.innerHTML = `
                        <div class="flex items-center space-x-3">
                            <div class="h-8 w-8 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center text-xs font-extrabold text-amber-500">
                                ${occ.name[0]}
                            </div>
                            <div>
                                <h5 class="text-xs font-bold text-white">${occ.name}</h5>
                                <span class="text-[10px] text-slate-500 block font-semibold">${occ.course} &middot; Admission: ${occ.admission_date}</span>
                            </div>
                        </div>
                        <div class="flex items-center space-x-3 text-right">
                            <div>
                                <span class="text-xs font-extrabold text-slate-200 block">${currencySymbol}${occ.rent.toLocaleString()}/mo</span>
                                <span class="text-[9px] text-slate-500 block font-bold">${occ.mobile}</span>
                            </div>
                            ${statusBadge}
                        </div>
                    `;
                    listContainer.appendChild(item);
                });
            }
            
            // Populate Allocation dropdown
            const allocSelect = document.getElementById('alloc-student-select');
            allocSelect.innerHTML = "<option value=''>-- Choose Student --</option>";
            // Find students who are not active, or unassigned
            const allocatableStudents = studentsData.filter(s => s.occupancy !== 'Active');
            allocatableStudents.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s.id;
                opt.innerText = `${s.name} (${s.course})`;
                allocSelect.appendChild(opt);
            });
            
            // Populate Transfer resident dropdown
            const transferSrcSelect = document.getElementById('transfer-student-select');
            transferSrcSelect.innerHTML = "<option value=''>-- Occupant to Transfer --</option>";
            room.occupants.forEach(occ => {
                const opt = document.createElement('option');
                opt.value = occ.id;
                opt.innerText = occ.name;
                transferSrcSelect.appendChild(opt);
            });

            // Populate Transfer Target Rooms dropdown
            const transferTargetSelect = document.getElementById('transfer-target-select');
            transferTargetSelect.innerHTML = "<option value=''>-- Target Room --</option>";
            // Find rooms in active state that have remaining capacity
            const eligibleRooms = roomsData.filter(r => r.status === 'Active' && r.available_beds > 0 && !(r.block === block && r.room_number === roomNumber));
            // Sort
            eligibleRooms.sort((a,b) => a.block.localeCompare(b.block) || parseInt(a.room_number) - parseInt(b.room_number));
            
            eligibleRooms.forEach(r => {
                const opt = document.createElement('option');
                opt.value = `${r.block}_${r.floor}_${r.room_number}`;
                opt.innerText = `${r.block} - Room ${r.room_number} (${r.available_beds} Vacant)`;
                transferTargetSelect.appendChild(opt);
            });

            // Open modal
            document.getElementById('room-modal').classList.remove('hidden');
        }

        function closeRoomModal() {
            document.getElementById('room-modal').classList.add('hidden');
        }

        // Directory Search & Filter Logic
        function filterTable() {
            const query = document.getElementById('search-input').value.toLowerCase();
            const status = document.getElementById('filter-status').value;
            const blockFilter = document.getElementById('filter-block').value;
            
            const rows = document.querySelectorAll('.student-row');
            let visibleCount = 0;
            
            rows.forEach(row => {
                const name = row.getAttribute('data-name').toLowerCase();
                const email = row.getAttribute('data-email').toLowerCase();
                const course = row.getAttribute('data-course').toLowerCase();
                const room = row.getAttribute('data-room').toLowerCase();
                const rowBlock = row.getAttribute('data-block');
                const rowStatus = row.getAttribute('data-status');
                const rowOccupancy = row.getAttribute('data-occupancy');
                
                const matchesQuery = name.includes(query) || email.includes(query) || course.includes(query) || room.includes(query);
                
                let matchesStatus = false;
                if (status === 'All') {
                    matchesStatus = true;
                } else if (status === 'Checked Out') {
                    matchesStatus = (rowOccupancy !== 'Active');
                } else {
                    matchesStatus = (rowStatus === status && rowOccupancy === 'Active');
                }

                const matchesBlock = (blockFilter === 'All') || (rowBlock === blockFilter);
                
                if (matchesQuery && matchesStatus && matchesBlock) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
        }

        // Calculates Block utilization metrics dynamically in JS
        function calculateBlockAnalytics() {
            const blocksList = ["Block A", "Block B", "Block C"];
            blocksList.forEach(blk => {
                const activeInBlock = studentsData.filter(s => s.block === blk && s.occupancy === 'Active');
                const totalBedsInBlock = roomsData.filter(r => r.block === blk).reduce((sum, r) => sum + r.capacity, 0);
                const count = activeInBlock.length;
                
                const occupancyRate = totalBedsInBlock > 0 ? Math.round((count / totalBedsInBlock) * 100) : 0;
                
                // Set text & progress
                const countBadge = document.getElementById(`resident-count-${blk.replace(' ', '')}`);
                if (countBadge) countBadge.innerText = `${count} Residents (${totalBedsInBlock} Beds)`;
                
                const progressText = document.getElementById(`progress-text-${blk.replace(' ', '')}`);
                if (progressText) progressText.innerText = `${occupancyRate}% Utilization`;
                
                const progressBar = document.getElementById(`progress-bar-${blk.replace(' ', '')}`);
                if (progressBar) progressBar.style.width = `${occupancyRate}%`;
            });
        }

        // On document ready
        document.addEventListener('DOMContentLoaded', () => {
            // Check query param tab
            const urlParams = new URLSearchParams(window.location.search);
            const activeUrlTab = urlParams.get('tab') || 'overview';
            
            switchTab(activeUrlTab);
            switchBlock('Block A');
            generateHeatMaps();
            calculateBlockAnalytics();
            
            lucide.createIcons();
        });
    </script>
</body>
</html>
"""

# Embedded Profile View HTML (matches currency setting & styling)
PROFILE_HTML = """
<!DOCTYPE html>
<html lang="en" class="dark h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ student.name }} - HostelHub Executive Profile</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
            background-color: #020617;
        }
        .gold-glow {
            box-shadow: 0 0 25px rgba(251, 191, 36, 0.08), 0 0 50px rgba(251, 191, 36, 0.04);
        }
    </style>
</head>
<body class="text-slate-100 flex flex-col min-h-screen">
    
    <!-- Header -->
    <nav class="sticky top-0 z-50 w-full bg-slate-900 border-b border-slate-800">
        <div class="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500"></div>
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="h-10 w-10 rounded-xl bg-gradient-to-br from-amber-400 via-yellow-500 to-orange-500 flex items-center justify-center shadow-lg shadow-amber-500/25">
                    <i data-lucide="hotel" class="text-slate-950 font-bold text-xl"></i>
                </div>
                <div>
                    <span class="text-xl font-extrabold tracking-wider bg-gradient-to-r from-amber-400 via-yellow-500 to-orange-500 bg-clip-text text-transparent uppercase">HOSTELHUB</span>
                    <span class="block text-[10px] text-slate-500 font-bold tracking-widest uppercase">Executive Profile</span>
                </div>
            </div>
            
            <a href="/?tab=directory" class="flex items-center space-x-2 bg-slate-950 border border-slate-800 hover:border-amber-500/50 px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider text-amber-400 transition-all duration-300">
                <i data-lucide="arrow-left" class="w-3.5 h-3.5"></i>
                <span>Back to Directory</span>
            </a>
        </div>
    </nav>

    <!-- Main -->
    <main class="flex-grow max-w-5xl w-full mx-auto px-6 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- Left card identity -->
            <div class="bg-slate-900/50 border border-amber-500/10 rounded-2xl p-6 gold-glow flex flex-col items-center text-center">
                <div class="relative mb-6">
                    <div class="h-24 w-24 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 p-1 shadow-lg shadow-amber-500/25">
                        <div class="h-full w-full rounded-full bg-slate-950 flex items-center justify-center">
                            <span class="text-3xl font-black text-amber-400">
                                {{ student.name.split(' ')[0][0] if student.name.split(' ')|length > 0 else 'S' }}{{ student.name.split(' ')[1][0] if student.name.split(' ')|length > 1 else '' }}
                            </span>
                        </div>
                    </div>
                    {% if student.occupancy == 'Active' %}
                    <span class="absolute bottom-0 right-1 block h-5 w-5 rounded-full ring-4 ring-slate-900 bg-emerald-500"></span>
                    {% else %}
                    <span class="absolute bottom-0 right-1 block h-5 w-5 rounded-full ring-4 ring-slate-900 bg-slate-500"></span>
                    {% endif %}
                </div>

                <h2 class="text-xl font-bold text-white">{{ student.name }}</h2>
                <p class="text-xs text-slate-400 mt-1">{{ student.email }}</p>
                
                <div class="mt-4 flex flex-wrap gap-2 justify-center">
                    {% if student.occupancy == 'Active' %}
                    <span class="px-3 py-1 rounded-full text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                        {{ student.block }} &middot; Room {{ student.room }}
                    </span>
                    <span class="px-3 py-1 rounded-full text-[10px] font-bold bg-slate-800 text-slate-300">
                        {{ student.floor }} Floor
                    </span>
                    {% else %}
                    <span class="px-3 py-1 rounded-full text-[10px] font-bold bg-slate-800 text-slate-500">
                        Unassigned
                    </span>
                    {% endif %}
                </div>

                <div class="border-t border-slate-850 w-full my-6"></div>

                <!-- Admin Action Controls -->
                <div class="w-full space-y-3">
                    <h4 class="text-xs font-bold text-slate-500 uppercase tracking-widest text-left mb-2">Controls</h4>
                    
                    <form action="/toggle_payment/{{ student.id }}" method="POST" class="w-full">
                        <button type="submit" class="w-full py-2.5 px-4 bg-slate-800 hover:bg-slate-750 border border-slate-700 hover:border-amber-500/30 rounded-xl text-xs font-bold text-amber-400 flex items-center justify-center space-x-2 transition-all">
                            <i data-lucide="credit-card" class="w-4 h-4"></i>
                            <span>Cycle Payment ({{ student.payment_status }})</span>
                        </button>
                    </form>

                    <form action="/deallocate/{{ student.id }}" method="POST" class="w-full">
                        <button type="submit" class="w-full py-2.5 px-4 bg-slate-800 hover:bg-slate-750 border border-slate-700 hover:border-amber-500/30 rounded-xl text-xs font-bold text-sky-400 flex items-center justify-center space-x-2 transition-all">
                            <i data-lucide="log-out" class="w-4 h-4"></i>
                            <span>{% if student.occupancy == 'Active' %}Deallocate Room{% else %}Allocate Room{% endif %}</span>
                        </button>
                    </form>

                    <form action="/delete/{{ student.id }}" method="POST" class="w-full" onsubmit="return confirm('Confirm deletion for this student profile?');">
                        <button type="submit" class="w-full py-2.5 px-4 bg-slate-950 hover:bg-rose-950 border border-slate-800 hover:border-rose-900 rounded-xl text-xs font-bold text-rose-400 flex items-center justify-center space-x-2 transition-all">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                            <span>Delete Resident Profile</span>
                        </button>
                    </form>
                </div>
            </div>

            <!-- Right Area details -->
            <div class="lg:col-span-2 space-y-6">
                <!-- Resident Profile Info -->
                <div class="bg-slate-900/50 border border-amber-500/10 rounded-2xl p-6 gold-glow">
                    <h3 class="text-base font-extrabold text-white mb-6 flex items-center space-x-2 border-b border-slate-800 pb-3">
                        <i data-lucide="info" class="text-amber-500"></i>
                        <span>Resident Profile Info</span>
                    </h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">Resident ID</span>
                            <span class="text-sm font-mono text-white block mt-1">#HH-{{ "%03d"|format(student.id) }}</span>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">Course / Program</span>
                            <span class="text-sm font-semibold text-white block mt-1">{{ student.course }}</span>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">Mobile Number</span>
                            <span class="text-sm font-semibold text-white block mt-1">{{ student.mobile }}</span>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">Admission Date</span>
                            <span class="text-sm font-semibold text-white block mt-1">{{ student.admission_date }}</span>
                        </div>
                    </div>
                </div>

                <!-- Billing status -->
                <div class="bg-slate-900/50 border border-amber-500/10 rounded-2xl p-6 gold-glow">
                    <h3 class="text-base font-extrabold text-white mb-6 flex items-center space-x-2 border-b border-slate-800 pb-3">
                        <i data-lucide="dollar-sign" class="text-amber-500"></i>
                        <span>Billing & Status</span>
                    </h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div>
                            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">Monthly Rent Rate</span>
                            <span class="text-xl font-extrabold text-white block mt-1">{{ settings.currency }}{{ "{:,}".format(student.rent) }} / month</span>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">Payment Status</span>
                            <div class="mt-1">
                                {% if student.payment_status == 'Paid' %}
                                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                                    Paid
                                </span>
                                {% elif student.payment_status == 'Pending' %}
                                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-rose-500/10 text-rose-400 border border-rose-500/30 animate-pulse">
                                    Pending
                                </span>
                                {% else %}
                                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30">
                                    Partial
                                </span>
                                {% endif %}
                            </div>
                        </div>
                    </div>

                    <div class="bg-slate-950 p-4 rounded-xl border border-slate-805/80 flex items-start space-x-3">
                        <i data-lucide="shield-alert" class="w-5 h-5 text-amber-400 shrink-0 mt-0.5 animate-pulse"></i>
                        <div class="text-xs text-slate-300 leading-relaxed">
                            <span class="font-bold text-white block mb-0.5">Automated Billing Notices</span>
                            Rents are billed on the 1st of every calendar month. System notices are automatically routed to the student and guardian when status is Pending or Partial.
                        </div>
                    </div>
                </div>

                <!-- Guardian details -->
                <div class="bg-slate-900/50 border border-amber-500/10 rounded-2xl p-6 gold-glow">
                    <h3 class="text-base font-extrabold text-white mb-6 flex items-center space-x-2 border-b border-slate-800 pb-3">
                        <i data-lucide="shield" class="text-amber-500"></i>
                        <span>Guardian & Emergency Contact</span>
                    </h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">Guardian Name</span>
                            <span class="text-sm font-semibold text-white block mt-1">{{ student.guardian_name }}</span>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">Guardian Contact</span>
                            <span class="text-sm font-semibold text-white block mt-1">{{ student.guardian_contact }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <p>&copy; 2026 HostelHub Enterprise Systems. All rights reserved.</p>
    </footer>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
"""

# --- SYSTEM CONTROLLERS ---

@app.route('/')
def dashboard():
    """Main route rendering the central executive dashboard with interactive JS datasets."""
    metrics = calculate_metrics()
    rooms_data = get_room_occupancy_data()
    
    # Sort students so Active ones appear first, then sorted by ID
    sorted_students = sorted(students_db, key=lambda s: (s['occupancy'] != 'Active', s['id']))
    
    # Serialize to JSON for interactive JavaScript in templates
    students_json = json.dumps(students_db)
    rooms_json = json.dumps(rooms_data)
    
    return render_template_string(DASHBOARD_HTML, 
                                  students=sorted_students, 
                                  metrics=metrics, 
                                  rooms=rooms_data,
                                  students_json=students_json,
                                  rooms_json=rooms_json,
                                  settings=settings)

@app.route('/student/<int:student_id>')
def view_profile(student_id):
    """View details of a specific student."""
    student = next((s for s in students_db if s['id'] == student_id), None)
    if not student:
        return "Student not found in registry", 404
    return render_template_string(PROFILE_HTML, student=student, settings=settings)

@app.route('/toggle_payment/<int:student_id>', methods=['GET', 'POST'])
def toggle_payment(student_id):
    """Cyclically toggles payment status (Paid -> Pending -> Partial -> Paid)."""
    for s in students_db:
        if s['id'] == student_id:
            status_cycle = ["Paid", "Pending", "Partial"]
            current_index = status_cycle.index(s['payment_status'])
            next_index = (current_index + 1) % len(status_cycle)
            s['payment_status'] = status_cycle[next_index]
            break
    
    referer = request.headers.get("Referer", "")
    if f"/student/{student_id}" in referer:
        return redirect(url_for('view_profile', student_id=student_id))
    return redirect(url_for('dashboard', tab='directory'))

@app.route('/deallocate/<int:student_id>', methods=['GET', 'POST'])
def deallocate(student_id):
    """Deallocates room by toggling occupancy status (Active <-> Checked Out)."""
    for s in students_db:
        if s['id'] == student_id:
            if s['occupancy'] == 'Active':
                s['occupancy'] = 'Checked Out'
            else:
                s['occupancy'] = 'Active'
            break
            
    referer = request.headers.get("Referer", "")
    if f"/student/{student_id}" in referer:
        return redirect(url_for('view_profile', student_id=student_id))
    return redirect(url_for('dashboard', tab='directory'))

@app.route('/delete/<int:student_id>', methods=['GET', 'POST'])
def delete_student(student_id):
    """Deletes student from in-memory state."""
    global students_db
    students_db = [s for s in students_db if s['id'] != student_id]
    return redirect(url_for('dashboard', tab='directory'))

@app.route('/register', methods=['POST'])
def register():
    """Form handler for student enrollment."""
    global students_db
    new_id = max(s['id'] for s in students_db) + 1 if students_db else 1
    
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    email = request.form.get('email')
    course = request.form.get('course')
    room = request.form.get('room')
    floor = request.form.get('floor')
    block = request.form.get('block')
    rent = int(request.form.get('rent', 0))
    payment_status = request.form.get('payment_status')
    admission_date = request.form.get('admission_date')
    guardian_name = request.form.get('guardian_name')
    guardian_contact = request.form.get('guardian_contact')
    
    new_student = {
        "id": new_id,
        "name": name,
        "mobile": mobile,
        "email": email,
        "guardian_name": guardian_name,
        "guardian_contact": guardian_contact,
        "block": block,
        "room": room,
        "floor": floor,
        "course": course,
        "admission_date": admission_date,
        "rent": rent,
        "payment_status": payment_status,
        "occupancy": "Active"
    }
    
    students_db.append(new_student)
    return redirect(url_for('dashboard', tab='directory'))

# --- SMART ROOM OPERATIONS (POST CONTROLLERS) ---

@app.route('/allocate_room', methods=['POST'])
def allocate_room():
    """Allocates a resident to a specific vacant room bed."""
    student_id = request.form.get('student_id')
    if not student_id:
        return redirect(url_for('dashboard', tab='rooms'))
        
    student_id = int(student_id)
    block = request.form.get('block')
    room = request.form.get('room')
    floor = request.form.get('floor')
    
    for s in students_db:
        if s['id'] == student_id:
            s['block'] = block
            s['room'] = room
            s['floor'] = floor
            s['occupancy'] = 'Active'
            break
    return redirect(url_for('dashboard', tab='rooms'))

@app.route('/transfer_student', methods=['POST'])
def transfer_student():
    """Transfers resident from their current room to another."""
    student_id = request.form.get('student_id')
    target_key = request.form.get('target_room_key') # Format: Block_Floor_RoomNumber
    
    if not student_id or not target_key:
        return redirect(url_for('dashboard', tab='rooms'))
        
    student_id = int(student_id)
    parts = target_key.split('_')
    if len(parts) == 3:
        target_block, target_floor, target_room = parts
        for s in students_db:
            if s['id'] == student_id:
                s['block'] = target_block
                s['floor'] = target_floor
                s['room'] = target_room
                break
    return redirect(url_for('dashboard', tab='rooms'))

@app.route('/toggle_maintenance', methods=['POST'])
def toggle_maintenance():
    """Toggles room state between Active and Maintenance."""
    block = request.form.get('block')
    room = request.form.get('room')
    
    for r in rooms_db:
        if r['block'] == block and r['room_number'] == room:
            r['status'] = 'Active' if r['status'] == 'Maintenance' else 'Maintenance'
            break
    return redirect(url_for('dashboard', tab='rooms'))

@app.route('/vacate_room', methods=['POST'])
def vacate_room():
    """Vacates all active students currently allocated to this room."""
    block = request.form.get('block')
    room = request.form.get('room')
    
    for s in students_db:
        if s['block'] == block and s['room'] == room and s['occupancy'] == 'Active':
            s['occupancy'] = 'Checked Out'
            
    return redirect(url_for('dashboard', tab='rooms'))

@app.route('/update_settings', methods=['POST'])
def update_settings():
    """Updates property branding & configurations dynamically."""
    global settings
    settings['property_name'] = request.form.get('property_name', 'HostelHub Central')
    settings['currency'] = request.form.get('currency', '₹')
    return redirect(url_for('dashboard', tab='settings'))

@app.route('/reset_system', methods=['POST'])
def reset_system():
    """Resets all data back to factory defaults."""
    global students_db, rooms_db
    # Reset students
    students_db = [
        {"id": 1, "name": "Aarav Sharma", "mobile": "+91 98765 01001", "email": "aarav.sharma@hostelhub.co", "guardian_name": "Ramesh Sharma", "guardian_contact": "+91 98765 01002", "block": "Block A", "room": "201", "floor": "1st", "course": "Cyber Security", "admission_date": "2025-08-15", "rent": 12000, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 2, "name": "Priya Patel", "mobile": "+91 98765 01003", "email": "priya.patel@hostelhub.co", "guardian_name": "Kirit Patel", "guardian_contact": "+91 98765 01004", "block": "Block A", "room": "201", "floor": "1st", "course": "Artificial Intelligence", "admission_date": "2025-09-01", "rent": 15000, "payment_status": "Pending", "occupancy": "Active"},
        {"id": 3, "name": "Rohan Gupta", "mobile": "+91 98765 01005", "email": "rohan.gupta@hostelhub.co", "guardian_name": "Sunil Gupta", "guardian_contact": "+91 98765 01006", "block": "Block A", "room": "301", "floor": "2nd", "course": "Philosophy & Law", "admission_date": "2025-07-20", "rent": 11000, "payment_status": "Partial", "occupancy": "Active"},
        {"id": 4, "name": "Siddharth Mehta", "mobile": "+91 98765 43210", "email": "sid.mehta@hostelhub.co", "guardian_name": "Rajesh Mehta", "guardian_contact": "+91 98765 43211", "block": "Block A", "room": "102", "floor": "Ground", "course": "Data Analytics", "admission_date": "2025-09-10", "rent": 13000, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 5, "name": "Sneha Iyer", "mobile": "+91 98765 01007", "email": "sneha.iyer@hostelhub.co", "guardian_name": "Srinivasan Iyer", "guardian_contact": "+91 98765 01008", "block": "Block B", "room": "101", "floor": "Ground", "course": "Fintech & Finance", "admission_date": "2025-08-22", "rent": 16000, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 6, "name": "Vikram Rao", "mobile": "+91 98765 01009", "email": "vikram.rao@hostelhub.co", "guardian_name": "Venkat Rao", "guardian_contact": "+91 98765 01010", "block": "Block B", "room": "202", "floor": "1st", "course": "Robotics Engineering", "admission_date": "2025-09-05", "rent": 14500, "payment_status": "Pending", "occupancy": "Active"},
        {"id": 7, "name": "Ananya Sen", "mobile": "+91 98765 01011", "email": "ananya.sen@hostelhub.co", "guardian_name": "Debasish Sen", "guardian_contact": "+91 98765 01012", "block": "Block B", "room": "303", "floor": "2nd", "course": "International Relations", "admission_date": "2025-09-01", "rent": 12500, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 8, "name": "Devansh Joshi", "mobile": "+91 98765 01013", "email": "devansh.joshi@hostelhub.co", "guardian_name": "Harish Joshi", "guardian_contact": "+91 98765 01014", "block": "Block C", "room": "104", "floor": "Ground", "course": "Architecture", "admission_date": "2025-08-10", "rent": 13500, "payment_status": "Partial", "occupancy": "Active"},
        {"id": 9, "name": "Ishita Verma", "mobile": "+91 98765 01015", "email": "ishita.verma@hostelhub.co", "guardian_name": "Manoj Verma", "guardian_contact": "+91 98765 01016", "block": "Block C", "room": "205", "floor": "1st", "course": "Civil Engineering", "admission_date": "2025-08-25", "rent": 14000, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 10, "name": "Kabir Nair", "mobile": "+91 98765 01017", "email": "kabir.nair@hostelhub.co", "guardian_name": "Madhavan Nair", "guardian_contact": "+91 98765 01018", "block": "Block C", "room": "306", "floor": "2nd", "course": "Marine Biology", "admission_date": "2025-09-01", "rent": 12000, "payment_status": "Pending", "occupancy": "Active"},
        {"id": 11, "name": "Sofia Deshmukh", "mobile": "+91 98765 01019", "email": "sofia.d@hostelhub.co", "guardian_name": "Vijay Deshmukh", "guardian_contact": "+91 98765 01020", "block": "Block A", "room": "103", "floor": "Ground", "course": "Biotechnology", "admission_date": "2025-07-15", "rent": 15500, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 12, "name": "Arjun Kapoor", "mobile": "+91 98765 01021", "email": "arjun.kapoor@hostelhub.co", "guardian_name": "Anil Kapoor", "guardian_contact": "+91 98765 01022", "block": "Block A", "room": "202", "floor": "1st", "course": "Aerospace Engineering", "admission_date": "2025-09-03", "rent": 16500, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 13, "name": "Divya Reddy", "mobile": "+91 98765 01023", "email": "divya.reddy@hostelhub.co", "guardian_name": "Gopal Reddy", "guardian_contact": "+91 98765 01024", "block": "Block B", "room": "102", "floor": "Ground", "course": "Software Engineering", "admission_date": "2025-09-01", "rent": 13000, "payment_status": "Partial", "occupancy": "Active"},
        {"id": 14, "name": "Aditya Saxena", "mobile": "+91 98765 01025", "email": "aditya.saxena@hostelhub.co", "guardian_name": "Rajiv Saxena", "guardian_contact": "+91 98765 01026", "block": "Block B", "room": "203", "floor": "1st", "course": "Sports Science", "admission_date": "2025-08-18", "rent": 11500, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 15, "name": "Neha Bhatia", "mobile": "+91 98765 01027", "email": "neha.bhatia@hostelhub.co", "guardian_name": "Ashok Bhatia", "guardian_contact": "+91 98765 01028", "block": "Block C", "room": "105", "floor": "Ground", "course": "English Literature", "admission_date": "2025-09-01", "rent": 12500, "payment_status": "Pending", "occupancy": "Active"},
        {"id": 16, "name": "Harshvardhan Singh", "mobile": "+91 98765 01029", "email": "harshvardhan.singh@hostelhub.co", "guardian_name": "Rajendra Singh", "guardian_contact": "+91 98765 01030", "block": "Block C", "room": "206", "floor": "1st", "course": "Military Strategy", "admission_date": "2025-06-01", "rent": 18000, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 17, "name": "Nisha Patel", "mobile": "+91 91234 56789", "email": "nisha.patel@hostelhub.co", "guardian_name": "Devendra Patel", "guardian_contact": "+91 91234 56780", "block": "Block A", "room": "302", "floor": "2nd", "course": "Medicine", "admission_date": "2025-09-02", "rent": 15000, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 18, "name": "Nikhil Mishra", "mobile": "+91 98765 01031", "email": "nikhil.mishra@hostelhub.co", "guardian_name": "Suresh Mishra", "guardian_contact": "+91 98765 01032", "block": "Block B", "room": "304", "floor": "2nd", "course": "Mechanical Engineering", "admission_date": "2025-08-30", "rent": 13000, "payment_status": "Pending", "occupancy": "Active"},
        {"id": 19, "name": "Tanvi Singhal", "mobile": "+91 98765 01033", "email": "tanvi.singhal@hostelhub.co", "guardian_name": "Alok Singhal", "guardian_contact": "+91 98765 01034", "block": "Block C", "room": "307", "floor": "2nd", "course": "Economics", "admission_date": "2025-09-01", "rent": 14000, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 20, "name": "Yash Choudhary", "mobile": "+91 98765 01035", "email": "yash.choudhary@hostelhub.co", "guardian_name": "Sanjay Choudhary", "guardian_contact": "+91 98765 01036", "block": "Block A", "room": "104", "floor": "Ground", "course": "Fine Arts", "admission_date": "2025-05-01", "rent": 17000, "payment_status": "Partial", "occupancy": "Active"},
        {"id": 21, "name": "Gauri Trivedi", "mobile": "+91 98765 01037", "email": "gauri.trivedi@hostelhub.co", "guardian_name": "Pankaj Trivedi", "guardian_contact": "+91 98765 01038", "block": "Block B", "room": "103", "floor": "Ground", "course": "Computer Science", "admission_date": "2025-07-04", "rent": 16000, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 22, "name": "Ishaan Sharma", "mobile": "+91 98765 01039", "email": "ishaan.sharma@hostelhub.co", "guardian_name": "Vijay Sharma", "guardian_contact": "+91 98765 01040", "block": "Block C", "room": "106", "floor": "Ground", "course": "Physics & Mathematics", "admission_date": "2025-09-01", "rent": 15000, "payment_status": "Paid", "occupancy": "Checked Out"},
        {"id": 23, "name": "Mansi Shinde", "mobile": "+91 98765 01041", "email": "mansi.shinde@hostelhub.co", "guardian_name": "Prakash Shinde", "guardian_contact": "+91 98765 01042", "block": "Block A", "room": "203", "floor": "1st", "course": "Chemistry", "admission_date": "2025-08-01", "rent": 15500, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 24, "name": "Aman Saxena", "mobile": "+91 98765 01043", "email": "aman.saxena@hostelhub.co", "guardian_name": "Vineet Saxena", "guardian_contact": "+91 98765 01044", "block": "Block B", "room": "204", "floor": "1st", "course": "Theoretical Physics", "admission_date": "2025-09-01", "rent": 14000, "payment_status": "Pending", "occupancy": "Active"},
        {"id": 25, "name": "Aditi Banerjee", "mobile": "+91 98765 01045", "email": "aditi.banerjee@hostelhub.co", "guardian_name": "Pradip Banerjee", "guardian_contact": "+91 98765 01046", "block": "Block C", "room": "207", "floor": "1st", "course": "Mathematics & Computation", "admission_date": "2025-09-01", "rent": 16500, "payment_status": "Paid", "occupancy": "Active"},
        {"id": 26, "name": "Nilay Shah", "mobile": "+91 98765 01047", "email": "nilay.shah@hostelhub.co", "guardian_name": "Pankaj Shah", "guardian_contact": "+91 98765 01048", "block": "Block A", "room": "303", "floor": "2nd", "course": "Electrical Engineering", "admission_date": "2025-09-01", "rent": 13500, "payment_status": "Partial", "occupancy": "Active"}
    ]
    
    # Reset rooms
    rooms_db.clear()
    for b in blocks:
        for f in floors:
            room_start = 101 if f == "Ground" else (201 if f == "1st" else 301)
            for r_num in range(room_start, room_start + 10):
                status = "Maintenance" if (b == "Block B" and r_num == 105) or (b == "Block C" and r_num == 208) else "Active"
                capacity = 4 if r_num % 2 == 0 else 2
                rooms_db.append({
                    "block": b,
                    "floor": f,
                    "room_number": str(r_num),
                    "capacity": capacity,
                    "status": status
                })
                
    global settings
    settings['property_name'] = "HostelHub Central"
    settings['currency'] = "₹"
    
    return redirect(url_for('dashboard', tab='settings'))

if __name__ == '__main__':
    print("HostelHub Premium Smart Layout system is launching...")
    print("Server URL: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
