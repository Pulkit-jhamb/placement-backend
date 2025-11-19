from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB URI
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise EnvironmentError("MONGO_URI not found in environment variables. Check your .env file.")

print("📄 Connecting to MongoDB...")

try:
    # Simple connection with only tlsAllowInvalidCertificates (NOT tlsInsecure)
    client = MongoClient(
        MONGO_URI,
        tlsAllowInvalidCertificates=True,  # Only this one!
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000
    )
    
    # Test connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
except Exception as e:
    print(f"❌ Connection failed: {str(e)[:200]}")
    raise

# Database
db = client["carevo"]

# =====================================================
# 👤 USER & AUTH COLLECTIONS
# =====================================================
users_collection = db["users"]
otp_collection = db["otps"]  # For password reset OTPs

# =====================================================
# 💬 CHAT SYSTEM COLLECTIONS
# =====================================================
messages_collection = db["messages"]
conversations_collection = db["conversations"]

# =====================================================
# 📚 CONTENT COLLECTIONS
# =====================================================
notes_collection = db["notes"]
favorites_collection = db["favorites"]

# =====================================================
# 🆘 HELP / SUPPORT COLLECTIONS
# =====================================================
help_reports_collection = db["help_reports"]

# =====================================================
# 📝 QUIZ COLLECTIONS
# =====================================================
quizzes_collection = db["quizzes"]
quiz_answers_collection = db["quiz_answers"]
quiz_results_collection = db["quiz_results"]

# =====================================================
# 🏢 PLACEMENT & CAREER COLLECTIONS
# =====================================================
placement_collection = db["placement"]

# =====================================================
# 🎓 ADMIN OPPORTUNITY COLLECTIONS
# Admin creates these opportunities for students
# =====================================================
admin_projects_collection = db["admin_projects"]
admin_research_collection = db["admin_research"]
admin_patents_collection = db["admin_patents"]

# =====================================================
# 📋 STUDENT APPLICATIONS COLLECTION (NEW & CRITICAL)
# Students apply to admin opportunities here
# This is the bridge between students and opportunities
# =====================================================
student_applications_collection = db["student_applications"]

# =====================================================
# 📊 LEGACY COLLECTIONS (deprecated - for backward compatibility)
# These can be repurposed or removed in future
# =====================================================
project_collection = db["project"]  # OLD: unclear purpose
research_collection = db["research"]  # OLD: unclear purpose
student_collection = db["student"]
admin_collection = db["admin"]
placement_cell_collection = db["placement_cell"]
chat_collection = db["chat"]

# =====================================================
# 🎯 CREATE INDEXES FOR PERFORMANCE
# =====================================================
def create_indexes():
    """Create indexes for better query performance"""
    try:
        print("🔧 Creating database indexes...")
        
        # Users - for authentication and onboarding
        users_collection.create_index("email", unique=True)
        users_collection.create_index("userType")
        users_collection.create_index("onboardingCompleted")
        print("  ✓ Users indexes created")
        
        # Messages
        messages_collection.create_index("conversationId")
        messages_collection.create_index("senderId")
        messages_collection.create_index("timestamp")
        print("  ✓ Messages indexes created")
        
        # Conversations
        conversations_collection.create_index("participants")
        conversations_collection.create_index("lastMessageAt")
        print("  ✓ Conversations indexes created")
        
        # Notes
        notes_collection.create_index("userId")
        notes_collection.create_index("createdAt")
        print("  ✓ Notes indexes created")
        
        # Favorites
        favorites_collection.create_index("userId")
        favorites_collection.create_index("contentType")
        print("  ✓ Favorites indexes created")
        
        # Help reports
        help_reports_collection.create_index("userId")
        help_reports_collection.create_index("createdAt")
        print("  ✓ Help reports indexes created")
        
        # Placements
        placement_collection.create_index("userId")
        placement_collection.create_index("company")
        placement_collection.create_index("status")
        print("  ✓ Placement indexes created")
        
        # Admin Opportunities
        admin_projects_collection.create_index("createdBy")
        admin_projects_collection.create_index("deadline")
        admin_projects_collection.create_index("status")
        print("  ✓ Admin projects indexes created")
        
        admin_research_collection.create_index("createdBy")
        admin_research_collection.create_index("deadline")
        admin_research_collection.create_index("status")
        print("  ✓ Admin research indexes created")
        
        admin_patents_collection.create_index("createdBy")
        admin_patents_collection.create_index("deadline")
        admin_patents_collection.create_index("status")
        print("  ✓ Admin patents indexes created")
        
        # ⭐ NEW: Student Applications - CRITICAL for performance
        student_applications_collection.create_index("studentId")
        student_applications_collection.create_index("opportunityId")
        student_applications_collection.create_index("opportunityType")
        student_applications_collection.create_index("status")
        student_applications_collection.create_index("appliedAt")
        # Compound index for common queries
        student_applications_collection.create_index([
            ("opportunityId", 1),
            ("opportunityType", 1),
            ("status", 1)
        ])
        print("  ✓ Student applications indexes created")
        
        print("✅ All database indexes created successfully!")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not create some indexes: {e}")

# Create indexes when module is imported
create_indexes()

# Print confirmation
print("=" * 60)
print(f"✅ Database: {db.name}")
print(f"✅ Core collections: users, messages, conversations")
print(f"✅ Content collections: notes, favorites")
print(f"✅ Quiz collections: quizzes, quiz_answers, quiz_results")
print(f"✅ Career collections: placement")
print(f"✅ Admin opportunities: admin_projects, admin_research, admin_patents")
print(f"✅ Student applications: student_applications (NEW)")
print(f"✅ Chat system ready!")
print(f"✅ Onboarding system ready!")
print("=" * 60)