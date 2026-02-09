import os
from supabase import Client, create_client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get('SUPABASE_KEY')

SupabaseConnection: Client = create_client(url, key)