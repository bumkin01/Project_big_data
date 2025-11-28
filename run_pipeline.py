import subprocess
import time

def run_script(script_name):
    print(f"\n🚀 Starting: {script_name}...")
    try:
        result = subprocess.run(["python", script_name], check=True)
        print(f"✅ Completed: {script_name}")
    except subprocess.CalledProcessError:
        print(f"❌ Error: {script_name} failed!")
        exit(1) 

if __name__ == "__main__":
    print("=== 🤖 STARTING AUTOMATION PIPELINE ===")
    

    run_script("ingest.py")
    time.sleep(2)
    

    run_script("transform.py")


    run_script("publish.py")
    
    print("\n=== ✨ PIPELINE FINISHED SUCCESSFULLY ✨ ===")